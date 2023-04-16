# Final Project Group7
#Deployment of 2-tiered web application to managed K8s cluster on Amazon EKS, with pod auto-scaling and deployment automation.

# Create EKS Cluster
```sh
cd deployment_file

# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv -v /tmp/eksctl /usr/local/bin

# Enable eksctl bash completion
eksctl completion bash >> ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion
# create cluster
eksctl create cluster -f eks_config.yaml
```

## Configuring Kubernetes Service to Assune IAM Role
follow this document present in the project named Configuring Kubernetes Service to Assune IAM Role

## Commands to run the application
```sh
cd mainfest
kubectl create namespace final
kubectl apply -f role.yaml -n final 
kubectl apply -f pvc.yaml -n final
kubectl apply -f mysql_deployment -n final
kubectl apply -f myconfig -n final
kubectl apply -f mysql_service -n final
kubectl apply -f app_deployment-n final
kubectl apply -f myappservice -n final
```
