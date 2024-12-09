"""main function for testing the agent initialization and intent detection"""

from app_initializer import application
from core.entity.agent import Agent
from core.entity.target import Target
from core.entity.unified_context import UnifiedContext
from utils.logging import logging

logger = logging.getLogger(__name__)


def main():
    """Main function for testing the agent initialization and intent detection"""
    logger.info("Starting agent initialization...")

    try:
        agent = Agent.from_template(
            "./src/config/agent_template/restaurant_guide_agent.yaml",
            "./src/config/role_template/restaurant_guide_role.yaml",
        )
        user = Target.from_template("./src/config/target_template/user.yaml")
        user_query = "I want to find a restaurant in San Francisco"
        unified_context = UnifiedContext.from_config(
            agent=agent, target=user, interaction_his=[]
        )
        result = application.intent_detect_service.detect_intent(
            unified_context=unified_context, raw_query=user_query
        )
        logger.info("Detected intent: %s", result)

    except Exception as e:
        logger.error("Failed to initialize agent: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
