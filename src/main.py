import logging
from core.entity.agent import Agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # This will print to console as well
    ],
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting agent initialization...")

    try:
        agent = Agent.from_template(
            "./config/agent_template/restaurant_guide_agent.yaml",
            "./config/role_template/restaurant_guide_role.yaml",
        )

        logger.info(f"Agent initialized successfully:")
        logger.info(f"Goal: {agent.get_goal()}")
        logger.info(f"Initial state: {agent.get_current_state().name}")
        logger.info(
            f"Available next states: {[state.name for state in agent.get_role().get_next_states(agent.get_current_state().name)]}"
        )

    except Exception as e:
        logger.error(f"Failed to initialize agent: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
