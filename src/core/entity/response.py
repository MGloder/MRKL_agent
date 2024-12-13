"""Module to define the response entity for the agent."""

from enum import Enum


class TaskStatus(Enum):
    """Enum to represent the possible states of a task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskResponse:
    """Class to track the status and returned object from the task."""

    def __init__(self, status: TaskStatus, returned_object: dict):
        self.status = status
        self.returned_object = returned_object

    def __str__(self) -> str:
        """String representation of the task response.

        Returns:
            str: A formatted string showing the task status and returned object
        """
        result = self.returned_object.get("result", "")
        error = self.returned_object.get("error", "")
        if self.status == TaskStatus.FAILED:
            return f"Task Status: {self.status.value}, Error: {error}"
        return f"Task Status: {self.status.value}, Result: {result}"

    @property
    def get_status(self) -> TaskStatus:
        """Get the status of the task."""
        return self.status

    @property
    def get_returned_object(self) -> dict:
        """Get the returned object from the task.

        Returns:
            dict: The dictionary containing the task's returned data
        """
        return self.returned_object


class AgentResponse:
    """Class to represent an agent response."""

    def __init__(self, message: dict, success: bool = True, error: str = None):
        """Initialize an agent response.

        Args:
            message: The response message from the agent
            success: Whether the interaction was successful
            error: Error message if the interaction failed
        """
        self.message = message
        self.success = success
        self.error = error
        self.task_responses: list[TaskResponse] = []

    def __str__(self) -> str:
        """String representation of the response.

        Returns:
            str: A formatted string showing the agent response details
        """
        if self.error:
            return f"Agent Response (Failed) - Error: {self.error}"

        # Add message content
        if "llm_message" in self.message:
            return self.message["llm_message"]

        return ""

    def add_task_response(self, task_response: TaskResponse) -> None:
        """Add a task response to the agent response.

        Args:
            task_response: The task response to add
        """
        self.task_responses.append(task_response)

    @property
    def is_success(self) -> bool:
        """Check if the interaction was successful.

        Returns:
            True if successful, False otherwise
        """
        return self.success

    @property
    def get_message(self) -> dict:
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

    @property
    def get_task_responses(self) -> list[TaskResponse]:
        """Get all task responses.

        Returns:
            List of task responses
        """
        return self.task_responses
