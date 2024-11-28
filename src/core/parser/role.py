from dataclasses import dataclass
from typing import List, Dict, Optional
import yaml


@dataclass
class Transition:
    to: str
    condition: Optional[str] = None


@dataclass 
class State:
    name: str
    type: str
    transitions: List[Transition]
    subtasks: List[str] = None
    description: Optional[str] = None


class RoleTemplateParser:
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.states: Dict[str, State] = {}
        self.properties: Dict[str, Dict] = {}
        
    def parse(self) -> None:
        """Parse the YAML template file and populate the states and properties"""
        with open(self.template_path, 'r') as f:
            template = yaml.safe_load(f)
            
        # Parse states
        for state_data in template['states']:
            transitions = [
                Transition(**transition) 
                for transition in state_data.get('transitions', [])
            ]
            
            state = State(
                name=state_data['name'],
                type=state_data['type'], 
                transitions=transitions,
                subtasks=state_data.get('subtasks')
            )
            
            self.states[state.name] = state
            
        # Parse properties
        self.properties = template.get('properties', {})
        
        # Add descriptions to states
        for state_name, state in self.states.items():
            if state_name in self.properties:
                state.description = self.properties[state_name]['description']
                
    def get_state(self, state_name: str) -> Optional[State]:
        """Get a state by name"""
        return self.states.get(state_name)
    
    def get_all_states(self) -> Dict[str, State]:
        """Get all states"""
        return self.states
    
    def get_properties(self) -> Dict[str, Dict]:
        """Get all properties"""
        return self.properties
