from typing import Optional

import yaml

from core.entity.target import Target


class TargetTemplateParser:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.target: Optional[Target] = None

    def parse(self) -> None:
        """Parse the YAML template file and populate the target"""
        with open(self.template_path, "r") as f:
            template = yaml.safe_load(f)

        target_data = template["target"]
        self.target = Target(
            name=target_data["name"],
            description=target_data["description"],
        )

    def get_target(self) -> Optional[Target]:
        """Get the parsed target"""
        return self.target
