"""
Basic usage example of Docker CI/CD Manager.
"""

import time
import logging
from docker_cicd_manager import DockerManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main function demonstrating basic usage."""

    # Initialize Docker Manager
    logger.info("Initializing Docker Manager...")
    docker_manager = DockerManager()

    try:
        # Get Docker info
        info = docker_manager.get_docker_info()
        logger.info(f"Docker version: {info.get('ServerVersion', 'Unknown')}")
        logger.info(f"Total containers: {info.get('Containers', 0)}")

        # Create a simple test container
        logger.info("Creating a simple test container...")
        container = docker_manager.create_test_container(
            image="ubuntu:latest",
            command="echo 'Hello from Docker CI/CD Manager!'",
            name="basic-usage-test",
        )

        logger.info(f"Container created: {container.id}")

        # Wait for container to complete
        time.sleep(2)

        # Get container logs
        logs = docker_manager.get_container_logs(container.id)
        logger.info(f"Container logs: {logs}")

        # Create a Python test container
        logger.info("Creating a Python test container...")
        python_container = docker_manager.create_test_container(
            image="python:3.11-slim",
            command="python -c 'import sys; print(f\"Python {sys.version} is working!\")'",
            name="python-test",
        )

        logger.info(f"Python container created: {python_container.id}")

        # Wait for container to complete
        time.sleep(3)

        # Get Python container logs
        python_logs = docker_manager.get_container_logs(python_container.id)
        logger.info(f"Python container logs: {python_logs}")

        # List all containers
        logger.info("Listing all containers...")
        containers = docker_manager.list_containers(all_containers=True)
        logger.info(f"Found {len(containers)} containers")

        for container in containers:
            logger.info(
                f"  - {container.id[:12]}: {container.name} ({container.status})"
            )

        # Cleanup test containers
        logger.info("Cleaning up test containers...")
        cleaned_count = docker_manager.cleanup_test_containers()
        logger.info(f"Cleaned up {cleaned_count} test containers")

    except Exception as e:
        logger.error(f"Error: {e}")

    finally:
        # Close Docker client
        docker_manager.close()
        logger.info("Docker Manager closed")


if __name__ == "__main__":
    main()
