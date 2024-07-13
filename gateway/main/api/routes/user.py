from typing import Annotated
import json, requests, pika, gridfs, tempfile, shutil
from bson.objectid import ObjectId

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status, UploadFile, File, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse

from pymongo import MongoClient

from main.schemas.response import Response
from main.schemas.user import UserToken, UserRegistration
from main.core.exceptions import InvalidUserCredentialsException, BaseInternalException
from main.core.logger import logger
from main.core.config import get_app_settings
from main.core.rabbit_connection import rabbit_connection


router = APIRouter()
settings = get_app_settings()

client = MongoClient(str(settings.mongo_client_address))

# Check if videos/mp3s collection exists, create it if not
videos_db = client[settings.pymongo_videos_collection]
mp3s_db = client[settings.pymongo_mp3s_collection]

fs_videos = gridfs.GridFS(videos_db)
fs_mp3s = gridfs.GridFS(mp3s_db)


@router.post("/register")
def register(registration_data: UserRegistration)->Response:
    """
    Process user registration.
    """
    if not registration_data:
        raise BaseInternalException("Missing registration info - please re-enter.", status.HTTP_404_NOT_FOUND)


    url = f"http://{str(settings.auth_svc_address)}/api/v1/user/register"
    payload ={'username': registration_data.username, "email": registration_data.email, "password": registration_data.password}
    response = requests.post(url=url, json=payload)

    if response.status_code == status.HTTP_200_OK:
        return json.loads(response.text)
    else:
        raise InvalidUserCredentialsException("Invalid Registration Data", status.HTTP_404_NOT_FOUND)


@router.post("/login", response_model=Response[UserToken])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()])->Response:
    """
    Process user login. Returns JWT if valid
    """
    if not form_data:
        raise BaseInternalException("Missing credentials - please re-enter.", status.HTTP_404_NOT_FOUND)

    response = requests.post(f"http://{str(settings.auth_svc_address)}/api/v1/user/login", 
                        data={"username": form_data.username, "password": form_data.password, "grant_type": "password"},
                        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    if response.status_code == status.HTTP_200_OK:
        return json.loads(response.text)
    else:
        raise InvalidUserCredentialsException("Invalid Credentials.", status.HTTP_404_NOT_FOUND)


@router.post("/uploadfile", status_code=status.HTTP_201_CREATED, response_model=Response)
async def upload(file: Annotated[UploadFile, File(description="Some description")] = None, authorization: Annotated[str | None, Header()] = None)->Response:
    """
    Process file upload.
    """
    if not authorization:
        raise InvalidUserCredentialsException("Credentials missing. Please re-enter.", status.HTTP_401_UNAUTHORIZED)
    
    if not file:
        raise BaseInternalException("File missing. Please re-upload.", status.HTTP_404_NOT_FOUND)
    
    response = requests.get(
        f"http://{str(settings.auth_svc_address)}/api/v1/user/verify_current_user",
        headers={"content-type": "application/x-www-form-urlencoded", "Authorization": authorization},
    )

    if response.status_code == 200 or response.status_code == 201:
        current_user = response.json()['data']
    else:
        raise InvalidUserCredentialsException("Invalid credentials", status.HTTP_401_UNAUTHORIZED)

    if not current_user:
        raise InvalidUserCredentialsException("Invalid credentials", status.HTTP_401_UNAUTHORIZED)

    try:
        # Insert video file into GridFS
        fid = fs_videos.put(file.file, filename=file.filename)
        logger.info("Successfully added video to pymongo via GridFS")
    except Exception as err:
        logger.error("Internal error during mongo upload, %s", err)
        raise BaseInternalException("Internal server error during mongo upload", status.HTTP_500_INTERNAL_SERVER_ERROR)

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "email": current_user["email"],
    }

    try:
        await rabbit_connection.send_messages(message, routing_key=settings.rabbitmq_video_queue)
    except Exception as err:
        print(err)
        fs_videos.delete(fid)
        raise BaseInternalException("Internal server error during rabbitmq publish", status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(data={"video_fid": str(fid)}, message='PDF file uploaded successfully')

@router.get("/download/{file_id}", response_class=FileResponse)
def download(file_id: str, authorization: Annotated[str | None, Header()] = None):
    if not authorization:
        raise BaseInternalException("Internal server error during download", status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        # Convert file_id to ObjectId
        file_id = ObjectId(file_id)

        # Open the file from GridFS
        grid_out = fs_mp3s.get(file_id)

        # Create a temporary file to store the GridFS file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Copy the contents from the GridFS file object to the temporary file
            shutil.copyfileobj(grid_out, temp_file)
            temp_file_path = temp_file.name

        # Return the temporary file, setting the filename and media type appropriately.
        return FileResponse(temp_file_path, filename=grid_out.filename, media_type="application/octet-stream")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
