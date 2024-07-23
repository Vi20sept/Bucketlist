import docker
from kubernetes import client, config, utils
from azure.identity import AzureCliCredential
import time
import subprocess
import os

# Azure CLI Login


def azure_login():
    subprocess.run(["az", "login"], check=True)

# Login to Azure Container Registry (ACR)


def acr_login(acr_name):
    subprocess.run(["az", "acr", "login", "--name", acr_name], check=True)

# Tag and push Docker image to ACR


def push_docker_image(local_image, remote_image):
    docker_client = docker.from_env()
    docker_client.images.get(local_image).tag(remote_image)
    docker_client.images.push(remote_image)

# Get AKS credentials


def get_aks_credentials(resource_group, cluster_name):
    subprocess.run(["az", "aks", "get-credentials", "--resource-group",
                   resource_group, "--name", cluster_name], check=True)

# Apply Kubernetes manifests using CoreV1Api


def apply_k8s_manifest(manifest_file):
    utils.create_from_yaml(client.ApiClient(), manifest_file)


def main():
    # Azure Container Registry and Kubernetes Cluster details
    acr_name = "mypythonapp01"
    resource_group = "K8s"
    aks_cluster_name = "mypythonappKC"
    local_image = "mybucketlist"
    remote_image = f"{acr_name}.azurecr.io/mybucketlist:latest"
    deployment_file = "deployment.yml"
    service_file = "service.yml"

    # Perform Azure login
    azure_login()

    # Login to ACR and push Docker image
    acr_login(acr_name)
    push_docker_image(acr_name, local_image, remote_image)

    # Get AKS credentials
    get_aks_credentials(resource_group, aks_cluster_name)

    # Load kubeconfig
    config.load_kube_config()

    # Apply Kubernetes service manifest
    apply_k8s_manifest(deployment_file)
    apply_k8s_manifest(service_file)


if __name__ == "__main__":
    main()
