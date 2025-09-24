"""
Docker Manager for container and image operations.
"""

import docker
import logging
import os
import pathlib
from typing import Optional, Dict, Any, List
from .exceptions import ContainerError, ImageError, DockerManagerError

logger = logging.getLogger(__name__)


def _detect_docker_socket():
    """
    Detect the best Docker socket to use.

    Returns:
        str: Path to the Docker socket or None for default
    """
    # List of possible Docker sockets in order of preference
    possible_sockets = [
        # Docker Desktop (Linux)
        f"/home/{os.getenv('USER', 'user')}/.docker/desktop/docker.sock",
        # Docker Desktop (alternative path)
        f"{os.path.expanduser('~')}/.docker/desktop/docker.sock",
        # System Docker socket
        "/var/run/docker.sock",
        # Docker Desktop (macOS)
        f"{os.path.expanduser('~')}/.docker/run/docker.sock",
    ]

    for socket_path in possible_sockets:
        if os.path.exists(socket_path):
            try:
                # Test if socket is accessible
                stat_info = os.stat(socket_path)
                logger.info(f"Found Docker socket: {socket_path}")
                return f"unix://{socket_path}"
            except (OSError, PermissionError):
                logger.debug(f"Socket not accessible: {socket_path}")
                continue

    logger.info("No specific Docker socket found, using default")
    return None


class DockerManager:
    """
    A class to manage Docker containers and images.
    """

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize Docker Manager.

        Args:
            base_url: Docker daemon URL. If None, auto-detects best socket.
        """
        try:
            if base_url:
                self.client = docker.DockerClient(base_url=base_url)
                logger.info(f"Using provided Docker URL: {base_url}")
            else:
                # Auto-detect Docker socket
                detected_socket = _detect_docker_socket()
                if detected_socket:
                    # Set environment variable for the detected socket
                    os.environ["DOCKER_HOST"] = detected_socket
                    logger.info(f"Auto-detected Docker socket: {detected_socket}")
                else:
                    logger.info("Using default Docker configuration")

                self.client = docker.from_env()

            # Test connection
            self.client.ping()
            logger.info("Successfully connected to Docker daemon")

        except docker.errors.DockerException as e:
            if "Permission denied" in str(e):
                raise DockerManagerError(
                    f"Permission denied to access Docker. Try:\n"
                    f"1. Make sure Docker Desktop is running\n"
                    f"2. Run with sudo: sudo python script.py\n"
                    f"3. Or add user to docker group: sudo usermod -aG docker $USER\n"
                    f"Current socket: {os.environ.get('DOCKER_HOST', 'default')}"
                )
            else:
                raise DockerManagerError(f"Failed to connect to Docker daemon: {e}")

    def create_test_container(
        self,
        image: str,
        command: str = "echo 'Test container created successfully'",
        name: Optional[str] = None,
        **kwargs,
    ) -> docker.models.containers.Container:
        """
        Create a test container with the specified image.

        Args:
            image: Docker image to use
            command: Command to run in the container
            name: Optional container name
            **kwargs: Additional container configuration options

        Returns:
            Container object

        Raises:
            ContainerError: If container creation fails
        """
        try:
            logger.info(f"Creating test container with image: {image}")

            # Default configuration for test container
            container_config = {
                "image": image,
                "command": command,
                "detach": True,
                "remove": kwargs.get(
                    "remove", True
                ),  # Use kwargs value or True by default
                "stdout": True,
                "stderr": True,
            }

            # Add custom name if provided
            if name:
                container_config["name"] = name

            # Merge with any additional kwargs
            container_config.update(kwargs)

            # Create and start container
            container = self.client.containers.run(**container_config)

            logger.info(f"Test container created successfully: {container.id}")
            return container

        except docker.errors.ImageNotFound:
            raise ImageError(f"Docker image '{image}' not found")
        except docker.errors.APIError as e:
            raise ContainerError(f"Failed to create container: {e}")
        except Exception as e:
            raise ContainerError(f"Unexpected error creating container: {e}")

    def get_container_logs(self, container_id: str) -> str:
        """
        Get logs from a container.

        Args:
            container_id: Container ID or name

        Returns:
            Container logs as string

        Raises:
            ContainerError: If container not found or logs retrieval fails
        """
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs().decode("utf-8")
            return logs
        except docker.errors.NotFound:
            raise ContainerError(f"Container '{container_id}' not found")
        except Exception as e:
            raise ContainerError(f"Failed to get container logs: {e}")

    def stop_container(self, container_id: str) -> bool:
        """
        Stop a running container.

        Args:
            container_id: Container ID or name

        Returns:
            True if container was stopped successfully

        Raises:
            ContainerError: If container not found or stop fails
        """
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            logger.info(f"Container {container_id} stopped successfully")
            return True
        except docker.errors.NotFound:
            raise ContainerError(f"Container '{container_id}' not found")
        except Exception as e:
            raise ContainerError(f"Failed to stop container: {e}")

    def list_containers(
        self, all_containers: bool = False
    ) -> List[docker.models.containers.Container]:
        """
        List Docker containers.

        Args:
            all_containers: If True, include stopped containers

        Returns:
            List of container objects
        """
        try:
            containers = self.client.containers.list(all=all_containers)
            return containers
        except Exception as e:
            raise ContainerError(f"Failed to list containers: {e}")

    def pull_image(self, image: str, tag: str = "latest") -> docker.models.images.Image:
        """
        Pull a Docker image.

        Args:
            image: Image name
            tag: Image tag

        Returns:
            Image object

        Raises:
            ImageError: If image pull fails
        """
        try:
            full_image_name = f"{image}:{tag}"
            logger.info(f"Pulling image: {full_image_name}")

            image_obj = self.client.images.pull(full_image_name)
            logger.info(f"Successfully pulled image: {full_image_name}")
            return image_obj

        except docker.errors.APIError as e:
            raise ImageError(f"Failed to pull image '{full_image_name}': {e}")
        except Exception as e:
            raise ImageError(f"Unexpected error pulling image: {e}")

    def build_image(
        self, path: str, tag: str, dockerfile: str = "Dockerfile"
    ) -> docker.models.images.Image:
        """
        Build a Docker image from a Dockerfile.

        Args:
            path: Path to build context
            tag: Image tag
            dockerfile: Dockerfile name

        Returns:
            Image object

        Raises:
            ImageError: If image build fails
        """
        try:
            logger.info(f"Building image '{tag}' from {path}")

            image, build_logs = self.client.images.build(
                path=path, tag=tag, dockerfile=dockerfile
            )

            logger.info(f"Successfully built image: {tag}")
            return image

        except docker.errors.BuildError as e:
            raise ImageError(f"Failed to build image '{tag}': {e}")
        except Exception as e:
            raise ImageError(f"Unexpected error building image: {e}")

    def cleanup_test_containers(self) -> int:
        """
        Clean up all test containers (containers with 'test' in name or created by this manager).

        Returns:
            Number of containers cleaned up
        """
        try:
            containers = self.client.containers.list(all=True)
            cleaned_count = 0

            for container in containers:
                # Check if container name contains 'test' or has test labels
                if (container.name and "test" in container.name.lower()) or (
                    container.labels
                    and container.labels.get("test_container") == "true"
                ):

                    try:
                        if container.status == "running":
                            container.stop()
                        container.remove()
                        cleaned_count += 1
                        logger.info(f"Cleaned up test container: {container.id}")
                    except Exception as e:
                        logger.warning(
                            f"Failed to clean up container {container.id}: {e}"
                        )

            logger.info(f"Cleaned up {cleaned_count} test containers")
            return cleaned_count

        except Exception as e:
            raise ContainerError(f"Failed to cleanup test containers: {e}")

    def get_docker_info(self) -> Dict[str, Any]:
        """
        Get Docker daemon information.

        Returns:
            Dictionary with Docker daemon info
        """
        try:
            info = self.client.info()
            return info
        except Exception as e:
            raise DockerManagerError(f"Failed to get Docker info: {e}")

    def close(self):
        """Close the Docker client connection."""
        if hasattr(self, "client"):
            self.client.close()
            logger.info("Docker client connection closed")
