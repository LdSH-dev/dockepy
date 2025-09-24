"""
Docker CI/CD Manager

A Python library for Docker container management and GitHub Actions CI/CD integration.
"""

from .docker_manager import DockerManager
from .exceptions import DockerManagerError, ContainerError, ImageError

__version__ = "0.1.0"
__author__ = "Leonardo Hemming"
__email__ = "leonardohemming@gmail.com"

__all__ = [
    "DockerManager",
    "DockerManagerError",
    "ContainerError",
    "ImageError",
]
