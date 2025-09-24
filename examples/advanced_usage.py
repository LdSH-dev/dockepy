"""
Advanced usage example of Docker CI/CD Manager.
"""

import time
import logging
from docker_cicd_manager import DockerManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_multiple_containers():
    """Test creating and managing multiple containers."""

    docker_manager = DockerManager()

    try:
        # Create multiple test containers with different images
        test_configs = [
            {
                "image": "alpine:latest",
                "command": "echo 'Alpine Linux test'",
                "name": "alpine-test",
            },
            {
                "image": "busybox:latest",
                "command": "echo 'BusyBox test'",
                "name": "busybox-test",
            },
            {
                "image": "python:3.11-slim",
                "command": "python -c 'print(\"Python container test\")'",
                "name": "python-test",
            },
        ]

        containers = []

        # Create all containers
        for config in test_configs:
            logger.info(f"Creating container: {config['name']}")
            container = docker_manager.create_test_container(**config)
            containers.append(container)
            logger.info(f"Created: {container.id}")

        # Wait for all containers to complete
        logger.info("Waiting for containers to complete...")
        time.sleep(5)

        # Check logs for each container
        for i, container in enumerate(containers):
            logs = docker_manager.get_container_logs(container.id)
            logger.info(f"Container {i+1} logs: {logs.strip()}")

        # Cleanup
        cleaned_count = docker_manager.cleanup_test_containers()
        logger.info(f"Cleaned up {cleaned_count} containers")

    except Exception as e:
        logger.error(f"Error in multiple containers test: {e}")

    finally:
        docker_manager.close()


def test_container_lifecycle():
    """Test complete container lifecycle management."""

    docker_manager = DockerManager()

    try:
        # Create a long-running container
        logger.info("Creating long-running container...")
        container = docker_manager.create_test_container(
            image="busybox:latest", command="sleep 30", name="lifecycle-test"
        )

        logger.info(f"Container created: {container.id}")

        # Check container status
        containers = docker_manager.list_containers(all_containers=False)
        running_containers = [c for c in containers if c.id == container.id]
        assert len(running_containers) == 1
        logger.info("Container is running")

        # Stop the container
        logger.info("Stopping container...")
        docker_manager.stop_container(container.id)

        # Check that container is stopped
        time.sleep(1)
        all_containers = docker_manager.list_containers(all_containers=True)
        stopped_containers = [
            c for c in all_containers if c.id == container.id and c.status == "exited"
        ]
        assert len(stopped_containers) == 1
        logger.info("Container stopped successfully")

    except Exception as e:
        logger.error(f"Error in lifecycle test: {e}")

    finally:
        docker_manager.close()


def test_error_handling():
    """Test error handling scenarios."""

    docker_manager = DockerManager()

    try:
        # Test invalid image
        logger.info("Testing invalid image handling...")
        try:
            docker_manager.create_test_container(
                image="non-existent-image:latest", command="echo 'This should fail'"
            )
        except Exception as e:
            logger.info(f"Expected error caught: {type(e).__name__}: {e}")

        # Test invalid container operations
        logger.info("Testing invalid container operations...")
        try:
            docker_manager.get_container_logs("non-existent-container")
        except Exception as e:
            logger.info(f"Expected error caught: {type(e).__name__}: {e}")

        try:
            docker_manager.stop_container("non-existent-container")
        except Exception as e:
            logger.info(f"Expected error caught: {type(e).__name__}: {e}")

        logger.info("Error handling tests completed successfully")

    except Exception as e:
        logger.error(f"Unexpected error in error handling test: {e}")

    finally:
        docker_manager.close()


def main():
    """Run all advanced usage examples."""

    logger.info("=== Advanced Docker CI/CD Manager Usage Examples ===")

    # Test multiple containers
    logger.info("\n1. Testing multiple containers...")
    test_multiple_containers()

    # Test container lifecycle
    logger.info("\n2. Testing container lifecycle...")
    test_container_lifecycle()

    # Test error handling
    logger.info("\n3. Testing error handling...")
    test_error_handling()

    logger.info("\n=== All advanced examples completed ===")


if __name__ == "__main__":
    main()
