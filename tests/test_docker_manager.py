"""
Tests for Docker Manager functionality.
"""

import pytest
import time
import logging
from docker_cicd_manager import DockerManager
from docker_cicd_manager.exceptions import (
    ContainerError,
    ImageError,
)

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDockerManager:
    """Test class for DockerManager."""

    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        """Setup method that runs before each test."""
        self.docker_manager = DockerManager()
        yield
        # Cleanup after each test
        try:
            self.docker_manager.cleanup_test_containers()
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")
        finally:
            self.docker_manager.close()

    def test_docker_connection(self) -> None:
        """Test that Docker daemon connection works."""
        info = self.docker_manager.get_docker_info()
        assert info is not None
        assert "Containers" in info
        assert "Images" in info
        logger.info("Docker connection test passed")

    def test_create_simple_test_container(self) -> None:
        """Test creating a simple test container with Ubuntu."""
        # Create a test container
        container = self.docker_manager.create_test_container(
            image="ubuntu:latest",
            command="echo 'Hello from test container!'",
            name="test-container-simple",
            remove=False,  # Keep container for log retrieval
        )

        # Verify container was created
        assert container is not None
        assert container.id is not None
        logger.info(f"Created test container: {container.id}")

        # Wait a moment for container to complete
        time.sleep(2)

        # Get container logs
        logs = self.docker_manager.get_container_logs(container.id)
        assert "Hello from test container!" in logs
        logger.info(f"Container logs: {logs}")

        # Stop the container
        self.docker_manager.stop_container(container.id)
        logger.info("Simple test container test passed")

    def test_create_python_test_container(self) -> None:
        """Test creating a Python test container."""
        # Create a Python test container
        container = self.docker_manager.create_test_container(
            image="python:3.11-slim",
            command="python -c 'print(\"Python test container working!\")'",
            name="test-container-python",
            remove=False,  # Keep container for log retrieval
        )

        # Verify container was created
        assert container is not None
        assert container.id is not None
        logger.info(f"Created Python test container: {container.id}")

        # Wait for container to complete
        time.sleep(3)

        # Get container logs
        logs = self.docker_manager.get_container_logs(container.id)
        assert "Python test container working!" in logs
        logger.info(f"Python container logs: {logs}")

        # Stop the container
        self.docker_manager.stop_container(container.id)
        logger.info("Python test container test passed")

    def test_create_multiple_test_containers(self) -> None:
        """Test creating multiple test containers."""
        containers = []

        # Create multiple test containers
        for i in range(3):
            container = self.docker_manager.create_test_container(
                image="alpine:latest",
                command=f"echo 'Test container {i + 1} is working!'",
                name=f"test-container-{i + 1}",
                remove=False,  # Keep container for log retrieval
            )
            containers.append(container)
            logger.info(f"Created test container {i + 1}: {container.id}")

        # Wait for all containers to complete
        time.sleep(3)

        # Verify all containers were created
        assert len(containers) == 3

        # Check logs for each container
        for i, container in enumerate(containers):
            logs = self.docker_manager.get_container_logs(container.id)
            assert f"Test container {i + 1} is working!" in logs
            logger.info(f"Container {i + 1} logs: {logs}")

            # Stop each container
            self.docker_manager.stop_container(container.id)

        logger.info("Multiple test containers test passed")

    def test_container_error_handling(self) -> None:
        """Test error handling for invalid container operations."""
        # Test getting logs from non-existent container
        with pytest.raises(ContainerError):
            self.docker_manager.get_container_logs("non-existent-container")

        # Test stopping non-existent container
        with pytest.raises(ContainerError):
            self.docker_manager.stop_container("non-existent-container")

        logger.info("Container error handling test passed")

    def test_image_error_handling(self) -> None:
        """Test error handling for invalid image operations."""
        # Test creating container with non-existent image
        with pytest.raises(ImageError):
            self.docker_manager.create_test_container(
                image="non-existent-image:latest",
                command="echo 'This should fail'",
            )

        logger.info("Image error handling test passed")

    def test_list_containers(self) -> None:
        """Test listing containers functionality."""
        # Create a test container
        container = self.docker_manager.create_test_container(
            image="busybox:latest",
            command="sleep 10",
            name="test-container-list",
            remove=False,  # Keep container for testing
        )

        # List running containers
        running_containers = self.docker_manager.list_containers(all_containers=False)
        container_ids = [c.id for c in running_containers]
        assert container.id in container_ids

        # List all containers (including stopped)
        all_containers = self.docker_manager.list_containers(all_containers=True)
        all_container_ids = [c.id for c in all_containers]
        assert container.id in all_container_ids

        # Stop the container
        self.docker_manager.stop_container(container.id)

        logger.info("List containers test passed")

    def test_cleanup_test_containers(self) -> None:
        """Test cleanup functionality for test containers."""
        # Create several test containers
        containers = []
        for i in range(2):
            container = self.docker_manager.create_test_container(
                image="alpine:latest",
                command="echo 'Cleanup test container'",
                name=f"cleanup-test-{i}",
                remove=False,  # Keep containers for cleanup testing
            )
            containers.append(container)

        # Wait for containers to complete
        time.sleep(2)

        # Cleanup test containers
        cleaned_count = self.docker_manager.cleanup_test_containers()
        # Should clean up at least our test containers
        assert cleaned_count >= 2

        logger.info(f"Cleaned up {cleaned_count} test containers")
        logger.info("Cleanup test containers test passed")


def test_docker_manager_initialization() -> None:
    """Test DockerManager initialization."""
    # Test with default connection
    manager = DockerManager()
    assert manager.client is not None

    # Test connection
    info = manager.get_docker_info()
    assert info is not None

    manager.close()
    logger.info("DockerManager initialization test passed")


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
