from typing import Optional, List

import yaml


class TargetTemplateParser:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.target: "Target" = None

    def parse(self) -> None:
        """Parse the YAML template file and populate the target"""
        with open(self.template_path, "r") as f:
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
    def __init__(self, name: str, description: str, storage: List = []):
        self.name = name
        self.description = description
        self.storage = storage

    def add_storage(self, data):
        self.storage.append(data)

    def get_storage(self) -> Optional[str]:
        return self.storage[-1] if self.storage else None

    @classmethod
    def from_template(cls, target_template_path: str) -> "Target":
        """Create an Agent instance from template files.

        Args:
            target_template_path: Path to the target template YAML file

        Returns:
            Target: Initialized agent with goal, role, and initial state from templates
        """
        # Parse agent template
        target_parser = TargetTemplateParser(target_template_path)
        target_parser.parse()
        target_data = target_parser.get_target()

        return cls(
            name=target_data.name,
            description=target_data.description,
            storage=target_data.storage,
        )
