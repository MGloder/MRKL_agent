"""main function for testing the agent initialization and intent detection"""
from core.entity.agent import Agent
from core.entity.target import Target
from core.entity.unified_context import UnifiedContext
from lib.modules.nlu.intent_detector import IntentDetector
from utils.logging import logging

logger = logging.getLogger(__name__)


def main():
    """Main function for testing the agent initialization and intent detection"""
    logger.info("Starting agent initialization...")

    try:
        agent = Agent.from_template(
            "./config/agent_template/restaurant_guide_agent.yaml",
            "./config/role_template/restaurant_guide_role.yaml",
        )

        logger.info("Agent initialized successfully:")
        logger.info("Goal: {agent.get_goal()}")
        logger.info("Current state: {agent.get_current_state().name}")

        user = Target.from_template("./config/target_template/user.yaml")
        user_query = "I want to find a restaurant in San Francisco"
        logger.info("User initialized successfully: %s", user.name)

        unified_context = UnifiedContext.from_config(
            agent=agent, target=user, interaction_his=[]
        )
        logger.info(
            "Unified context initialized successfully: %s", str(unified_context)
        )

        intent_detector = IntentDetector()
        result = intent_detector.detect_intent(
            unified_context=unified_context, raw_query=user_query
        )
        logger.info("Detected intent: %s", result)

    except Exception as e:
        logger.error("Failed to initialize agent: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
