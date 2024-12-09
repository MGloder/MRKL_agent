"""Target entity class and parser for target templates"""
from typing import Optional, List

import yaml


class TargetTemplateParser:
    """Parser for target template files"""

    def __init__(self, template_path: str):
        self.template_path = template_path
        self.target: "Target" = None

    def parse(self) -> None:
        """Parse the YAML template file and populate the target"""
        with open(self.template_path, "r", encoding="utf-8") as f:
            template = yaml.safe_load(f)

        target_data = template["target"]
        self.target = Target(
            name=target_data["name"],
            description=target_data["description"],
        )

    def get_target(self) -> "Target":
        """Get the parsed target"""
        return self.target


class Target:
    """Data class representing a target with its name, description, and storage"""

    def __init__(
        self,
        name: str,
        description: str,
        storage: List = None,
        engagement_id: Optional[str] = None,
    ):
        """Initialize the target with its name, description, storage, and engagement ID"""
        self.name = name
        self.description = description
        self.storage = storage if storage else []
        self.engagement_id = engagement_id

    def add_storage(self, data):
        """Add data to the storage"""
        self.storage.append(data)

    def get_storage(self) -> Optional[str]:
        """Get the last item in the storage"""
        return self.storage[-1] if self.storage else None

    @classmethod
    def from_template(
        cls, target_template_path: str, engagement_id: Optional[str] = None
    ) -> "Target":
        """Create a Target instance from template files with an engagement ID."""
        target_parser = TargetTemplateParser(target_template_path)
        target_parser.parse()
        target_data = target_parser.get_target()

        return cls(
            name=target_data.name,
            description=target_data.description,
            storage=target_data.storage,
            engagement_id=engagement_id,
        )
