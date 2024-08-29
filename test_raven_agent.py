import os
import shutil
import subprocess
import time


def build_and_start_container():
    # Build the Docker image and start the container using Docker Compose
    subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
    print("Docker container started and running in the background.")


def stop_and_remove_container():
    # Stop and remove the container using Docker Compose
    subprocess.run(["docker-compose", "down"], check=True)
    print("Docker container stopped and removed.")
    subprocess.run(['docker', 'rmi', 'ravensproject_image'], check=True)
    print("Docker image Removed")


def copy_and_print_files(container_name, files):
    # Create a temporary directory to copy the files to
    temp_dir = "temp_docker_files"
    os.makedirs(temp_dir, exist_ok=True)

    for file in files:
        # Copy the file from the container to the host
        subprocess.run(["docker", "cp", f"{container_name}:/app/{file}", temp_dir], check=True)
        print(f"Copied {file} from container to {temp_dir}/{file}.")

        # Read and print the content of the file
        file_path = os.path.join(temp_dir, file)
        with open(file_path, 'r') as f:
            content = f.read()
            print(f"\nContents of {file}:\n")
            print(content)
            print("\n" + "="*40 + "\n")

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)
    print("Temporary files cleaned up.")


if __name__ == "__main__":
    try:
        # Build and start the container
        build_and_start_container()

        # Keep the container running for a while (e.g., 60 seconds)
        time.sleep(20)

        # List of files to copy and print
        files_to_print = ["AgentAnswers.csv", "ProblemResults.csv", "SetResults.csv"]
        copy_and_print_files("ravensproject_container", files_to_print)

    finally:
        # Stop and remove the container
        stop_and_remove_container()