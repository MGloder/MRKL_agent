import graphviz

from core.entity.role import Role


def visualize_state_machine(
    template_path: str, output_path: str = "state_machine"
) -> None:
    """
    Visualize the state machine defined in the YAML template using Graphviz.

    Args:
        template_path: Path to the YAML template file
        output_path: Path where the visualization should be saved (without extension)
    """
    # Parse the template
    role = Role.from_template(template_path)

    # Create a new directed graph
    dot = graphviz.Digraph(comment="State Machine Visualization")
    dot.attr(rankdir="LR")  # Left to right layout

    # Add nodes (states)
    for state_name, state in role.states.items():
        # Set node attributes based on state type
        node_attrs = {
            "shape": "rectangle",
            "style": "filled",
            "fillcolor": "#90EE90"
            if state.state_type == "start"
            else "#FFB6C1"
            if state.state_type == "end"
            else "#ADD8E6",
            "width": "0.5",  # Set width of the node
            "height": "0.5",  # Set height of the node
        }

        # Add label with description if available
        label = state_name
        if state.description:
            label += f"\n{state.description}"

        dot.node(state_name, label, **node_attrs)

    # Add edges (transitions)
    for state_name, state in role.states.items():
        for transition in state.transitions:
            edge_label = transition.condition if transition.condition else ""
            dot.edge(state_name, transition.to, edge_label)

    # Save the visualization
    dot.render(output_path, format="png", cleanup=True)
    print(f"Visualization saved to {output_path}.png")


if __name__ == "__main__":
    # Example usage
    file_path = "../src/config/role_template/restaurant_guide_role.yaml"
    visualize_state_machine(file_path)
