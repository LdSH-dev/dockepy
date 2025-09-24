# Docker CI/CD Manager Documentation

## Overview

Docker CI/CD Manager is a Python library that provides a simple and powerful interface for managing Docker containers, building images, and integrating with GitHub Actions for automated CI/CD pipelines.

## Features

- **Container Management**: Create, run, stop, and manage Docker containers
- **Image Operations**: Pull, build, and manage Docker images
- **Test Automation**: Create test containers for automated testing
- **CI/CD Integration**: GitHub Actions workflows for automated testing and deployment
- **Error Handling**: Comprehensive error handling and logging
- **Cleanup Utilities**: Automatic cleanup of test containers

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker installed and running
- pip package manager

### Install from source

```bash
git clone <repository-url>
cd docker-cicd-manager
pip install -r requirements.txt
pip install -e .
```

## Quick Start

### Basic Usage

```python
from docker_cicd_manager import DockerManager

# Initialize Docker Manager
docker_manager = DockerManager()

# Create a test container
container = docker_manager.create_test_container(
    image="ubuntu:latest",
    command="echo 'Hello from Docker!'",
    name="my-test-container"
)

# Get container logs
logs = docker_manager.get_container_logs(container.id)
print(logs)

# Stop the container
docker_manager.stop_container(container.id)

# Cleanup
docker_manager.close()
```

### Advanced Usage

```python
from docker_cicd_manager import DockerManager

docker_manager = DockerManager()

# Create multiple test containers
containers = []
for i in range(3):
    container = docker_manager.create_test_container(
        image="python:3.11-slim",
        command=f"python -c 'print(\"Container {i+1} is working!\")'",
        name=f"test-container-{i+1}"
    )
    containers.append(container)

# Wait for completion and check logs
import time
time.sleep(3)

for container in containers:
    logs = docker_manager.get_container_logs(container.id)
    print(f"Container {container.id}: {logs}")

# Cleanup all test containers
cleaned_count = docker_manager.cleanup_test_containers()
print(f"Cleaned up {cleaned_count} containers")

docker_manager.close()
```

## API Reference

### DockerManager Class

#### Constructor

```python
DockerManager(base_url=None)
```

- `base_url` (str, optional): Docker daemon URL. If None, uses default socket.

#### Methods

##### create_test_container(image, command, name=None, **kwargs)

Create a test container with the specified image.

**Parameters:**
- `image` (str): Docker image to use
- `command` (str): Command to run in the container
- `name` (str, optional): Container name
- `**kwargs`: Additional container configuration options

**Returns:** Container object

**Raises:**
- `ImageError`: If image not found
- `ContainerError`: If container creation fails

##### get_container_logs(container_id)

Get logs from a container.

**Parameters:**
- `container_id` (str): Container ID or name

**Returns:** Container logs as string

**Raises:**
- `ContainerError`: If container not found

##### stop_container(container_id)

Stop a running container.

**Parameters:**
- `container_id` (str): Container ID or name

**Returns:** True if successful

**Raises:**
- `ContainerError`: If container not found

##### list_containers(all_containers=False)

List Docker containers.

**Parameters:**
- `all_containers` (bool): If True, include stopped containers

**Returns:** List of container objects

##### pull_image(image, tag="latest")

Pull a Docker image.

**Parameters:**
- `image` (str): Image name
- `tag` (str): Image tag

**Returns:** Image object

**Raises:**
- `ImageError`: If image pull fails

##### build_image(path, tag, dockerfile="Dockerfile")

Build a Docker image from a Dockerfile.

**Parameters:**
- `path` (str): Path to build context
- `tag` (str): Image tag
- `dockerfile` (str): Dockerfile name

**Returns:** Image object

**Raises:**
- `ImageError`: If image build fails

##### cleanup_test_containers()

Clean up all test containers.

**Returns:** Number of containers cleaned up

##### get_docker_info()

Get Docker daemon information.

**Returns:** Dictionary with Docker daemon info

##### close()

Close the Docker client connection.

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_docker_manager.py::TestDockerManager::test_create_simple_test_container -v

# Run with coverage
python -m pytest tests/ -v --cov=docker_cicd_manager --cov-report=html

# Use the test runner script
python run_tests.py
```

### Test Categories

- **Unit Tests**: Test individual methods and functions
- **Integration Tests**: Test Docker integration
- **Error Handling Tests**: Test error scenarios

## CI/CD Integration

### GitHub Actions

The library includes GitHub Actions workflows for:

- **Continuous Integration**: Automated testing on push/PR
- **Code Quality**: Linting, formatting, type checking
- **Security Scanning**: Bandit and Safety checks
- **Docker Testing**: Integration tests with Docker
- **Release Management**: Automated releases

### Workflow Files

- `.github/workflows/ci.yml`: Main CI pipeline
- `.github/workflows/release.yml`: Release automation

## Examples

### Basic Examples

See `examples/basic_usage.py` for simple usage examples.

### Advanced Examples

See `examples/advanced_usage.py` for complex scenarios.

## Error Handling

The library provides comprehensive error handling:

- `DockerManagerError`: Base exception
- `ContainerError`: Container-related errors
- `ImageError`: Image-related errors

### Code Style

- Follow PEP 8
- Use Black for formatting
- Use Flake8 for linting
- Use MyPy for type checking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the examples