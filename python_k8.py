import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True, check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)


def main():
    # Login to Azure
    run_command("az login")

    # Login to Azure Container Registry
    run_command("az acr login --name mypythonapp01")

    # Tag the Docker image
    run_command(
        "docker tag mybucketlist mypythonapp01.azurecr.io/mybucketlist:latest")

    # Push the Docker image to the registry
    run_command("docker push mypythonapp01.azurecr.io/mybucketlist:latest")

    # Get AKS credentials
    run_command(
        "az aks get-credentials --resource-group K8s --name mypythonappKC")

    # Apply the Kubernetes deployment configuration
    run_command("kubectl apply -f deployment.yml")

    # Apply the Kubernetes service configuration
    run_command("kubectl apply -f service.yml")


if __name__ == "__main__":
    main()
