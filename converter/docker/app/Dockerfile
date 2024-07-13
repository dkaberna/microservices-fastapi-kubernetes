FROM python:3.10.14-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create log directory
RUN mkdir -p /var/log && chmod -R 777 /var/log

WORKDIR /app

# Install packages for virtual envitonment
RUN apt-get update -y \
  #&& apt-get install -y --no-install-recommends --no-install-suggests \
  && apt -y update && apt -y upgrade \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  && apt-get install -y build-essential ffmpeg \
  && apt-get install -y python3-virtualenv \
  && apt-get install -y netcat-traditional \
  && apt-get autoremove -y \
  && apt-get autoclean -y \
  && apt-get clean -y \
  && pip install --no-cache-dir --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3.10 -m venv /venv

# Enable venv
ENV PATH="/venv/bin:$PATH"

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade -r /app/requirements.txt

# Copy project
COPY . /app

# Add entrypoint file
COPY /docker/init_app.sh /
RUN chmod +x /init_app.sh

ENTRYPOINT ["/init_app.sh"]