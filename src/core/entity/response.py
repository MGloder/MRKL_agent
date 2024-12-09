"""Module to define the response entity for the agent."""


class AgentResponse:
    """Class to represent an agent response."""

    def __init__(self, message: str, success: bool = True, error: str = None):
        """Initialize an agent response.

        Args:
            message: The response message from the agent
            success: Whether the interaction was successful
            error: Error message if the interaction failed
        """
        self.message = message
        self.success = success
        self.error = error

    def __str__(self) -> str:
        """String representation of the response.

        Returns:
            The response message or error message if present
        """
        if self.error:
            return f"Error: {self.error}"
        return self.message

    @property
    def is_success(self) -> bool:
        """Check if the interaction was successful.

        Returns:
            True if successful, False otherwise
        """
        return self.success

    @property
    def get_message(self) -> str:
        """Get the response message.

        Returns:
            The response message
        """
        return self.message

    @property
    def get_error(self) -> str:
        """Get the error message if present.

        Returns:
            The error message or None if no error
        """
        return self.error
