import logging
from core.entity.agent import Agent
from core.entity.target import Target
from core.entity.unified_context import UnifiedContext
from lib.modules.nlu.intent_detector import IntentDetector
from utils.logging import logging

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
        logger.info(f"Current state: {agent.get_current_state().name}")

        user = Target.from_template("./config/target_template/user.yaml")
        user_query = "I want to find a restaurant in San Francisco"
        logger.info(f"User initialized successfully:")
        logger.info(f"Name: {user.name}")

        unified_context = UnifiedContext.from_config(
            agent=agent, target=user, interaction_his=[]
        )
        logger.info(f"Unified context initialized successfully:")
        logger.info(f"{str(unified_context)}")

        intent_detector = IntentDetector()
        result = intent_detector.detect_intent(
            unified_context=unified_context, raw_query=user_query
        )
        logger.info(f"Detected intent: {result}")

    except Exception as e:
        logger.error(f"Failed to initialize agent: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
