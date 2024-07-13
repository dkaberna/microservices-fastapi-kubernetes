#!/bin/bash

echo "Creating the RabbitMQ deployment.."
kubectl apply -f ./rabbit/manifests/pvc.yaml
kubectl apply -f ./rabbit/manifests/configmap.yaml
kubectl apply -f ./rabbit/manifests/ingress.yaml
kubectl apply -f ./rabbit/manifests/secret.yaml
kubectl apply -f ./rabbit/manifests/service.yaml
kubectl apply -f ./rabbit/manifests/statefulset.yaml


echo "Creating the Auth deployment.."
kubectl apply -f ./auth/manifests/auth-deploy.yaml
kubectl apply -f ./auth/manifests/auth-secret.yaml
kubectl apply -f ./auth/manifests/auth-service.yaml
kubectl apply -f ./auth/manifests/persistent-volume-claim.yaml
kubectl apply -f ./auth/manifests/persistent-volume.yaml
kubectl apply -f ./auth/manifests/postgres-deploy.yaml
kubectl apply -f ./auth/manifests/postgres-secret.yaml
kubectl apply -f ./auth/manifests/postgres-service.yaml

echo "Creating the Converter deployment.."
kubectl apply -f ./converter/manifests/configmap.yaml
kubectl apply -f ./converter/manifests/converter-deploy.yaml
kubectl apply -f ./converter/manifests/secret.yaml

echo "Creating the Gateway deployment.."
kubectl apply -f ./gateway/manifests/gateway-configmap.yaml
kubectl apply -f ./gateway/manifests/gateway-deploy.yaml
kubectl apply -f ./gateway/manifests/gateway-ingress.yaml
kubectl apply -f ./gateway/manifests/gateway-secret.yaml
kubectl apply -f ./gateway/manifests/gateway-service.yaml
kubectl apply -f ./gateway/manifests/mongodb-deploy.yaml
kubectl apply -f ./gateway/manifests/mongodb-secret.yaml
kubectl apply -f ./gateway/manifests/persistent-volume-claim.yaml
kubectl apply -f ./gateway/manifests/persistent-volume.yaml

echo "Creating the Notification deployment.."
kubectl apply -f ./notification/manifests/configmap.yaml
kubectl apply -f ./notification/manifests/notification-deploy.yaml
kubectl apply -f ./notification/manifests/secret.yaml