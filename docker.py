import subprocess


def deploy_app():
    try:
        # Pull the latest code from the repository
        subprocess.run(["git", "pull", "origin", "main"], check=True)

        # Build the application
        subprocess.run(
            ["docker", "build", "-t", "myapp:latest", "."], check=True)

        # Stop the running container
        # subprocess.run(["docker", "stop", "myapp"], check=True)

        # Remove the old container
        # subprocess.run(["docker", "rm", "myapp"], check=True)

        # Run the new container
        subprocess.run([
            "docker", "run", "-d", "--name", "myapp", "-p", "5000:5000", "myapp:latest"
        ], check=True)

        print("Deployment successful!")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    deploy_app()
