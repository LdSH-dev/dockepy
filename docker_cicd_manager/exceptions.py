"""
Custom exceptions for Docker CI/CD Manager.
"""


class DockerManagerError(Exception):
    """Base exception for Docker Manager errors."""

    pass


class ContainerError(DockerManagerError):
    """Exception raised for container-related errors."""

    pass


class ImageError(DockerManagerError):
    """Exception raised for image-related errors."""

    pass


class GitHubActionsError(DockerManagerError):
    """Exception raised for GitHub Actions-related errors."""

    pass
