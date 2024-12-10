# Agent System

A state-machine-based intelligent agent system designed to allow user to define agent behaviors and roles.

## Key Components

### Agent & Role Templates

- YAML-based templates for defining agent behaviors and roles
- Configurable states, transitions, and event-action mappings
- Properties and descriptions for states and events
- Support for complex state machine flows

### Role Customization

- Users can define different roles for the same agent, allowing for flexible behavior customization.
- Each role can have unique states, events, actions, and prompts.

Example State-machine flowchart:

```
[Initial State]
    |
    v
[Information Collection]    <------------------------
    |-----------------------------------|           |
    v                                   |           |
[Restaurant Recommendation] --------------> [Modify Preferences]
    |-----------------------------------|
    v                                   |
[Restaurant Detail Retrieval]           |
    |-----------------------------------|
    v                                   v
[Success]                           [Error]
```

### Relationship Chart

Below is a chart illustrating the relationship between agents, roles, events and actions:
![relationship.png](.images%2Frelationship.png)
