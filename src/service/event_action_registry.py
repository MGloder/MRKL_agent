"""Event action registry module."""
from typing import Callable, Optional
import pkgutil
import importlib


class EventActionRegistry:
    """Registry to manage event actions and their execution with scope."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EventActionRegistry, cls).__new__(cls)
            cls._instance._registry = {}
        return cls._instance

    def __init__(self):
        """Initialize an empty event action registry."""
        self._registry = {}
        self.load_from_ext()

    def load_from_ext(self):
        """Load functions from all modules in the 'ext' package and register them with the module name as scope."""
        try:
            package = importlib.import_module("ext")
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                module = importlib.import_module(f"ext.{module_name}")
                scope = module_name

                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if callable(attr) and not attr_name.startswith("_"):
                        self.register(scope, attr_name, attr)

        except ImportError as e:
            raise ImportError(f"Failed to load extension modules: {str(e)}") from e

    def register(self, scope: str, action_name: str, function: callable):
        """Register an event action with its corresponding function under a specific scope."""
        if scope not in self._registry:
            self._registry[scope] = {}
        self._registry[scope][action_name] = function

    def get_action(self, scope: str, action_name: str) -> Optional[Callable]:
        """Get the action function registered under the given name and scope.

        Args:
            scope: The scope under which the action is registered
            action_name: Name of the action to retrieve

        Returns:
            The registered action function if found, None otherwise
        """
        if scope in self._registry:
            actions = self._registry[scope]
            return actions.get(action_name)
        return None

    def unregister(self, scope: str, action_name: str) -> None:
        """Remove an action from the registry.

        Args:
            scope: The scope under which the action is registered
            action_name: Name of the action to remove

        Raises:
            KeyError: If action_name is not registered under the given scope
        """
        if scope in self._registry:
            actions = self._registry[scope]
            if action_name in actions:
                del actions[action_name]
                return
        raise KeyError(
            f"No action registered for name: {action_name} under scope: {scope}"
        )
