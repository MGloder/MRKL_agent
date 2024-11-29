from dataclasses import dataclass
from typing import Optional
import yaml


@dataclass
class Agent:
    goal: str


class AgentTemplateParser:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.agent: Optional[Agent] = None

    def parse(self) -> None:
        """Parse the YAML template file and populate the agent data"""
        with open(self.template_path, "r") as f:
            template = yaml.safe_load(f)

        agent_data = template["agent"]
        self.agent = Agent(goal=agent_data["goal"])

    def get_agent(self) -> Optional[Agent]:
        """Get the parsed agent"""
        return self.agent
