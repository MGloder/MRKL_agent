"""main function for testing the agent initialization and intent detection"""
from application import ApplicationInitializer
from utils.logging import logging

logger = logging.getLogger(__name__)

# Create default app configuration
application = ApplicationInitializer.initialize()


def main():
    """Main function for testing the agent initialization and intent detection"""
    logger.info("Starting agent initialization...")
    agent_template_path = "./src/config/agent_template/restaurant_guide_agent.yaml"
    role_template_path = "./src/config/role_template/restaurant_guide_role.yaml"
    target_template_path = "./src/config/target_template/user.yaml"
    engagement_id = application.user_engagement_service.create_engagement(
        agent_template_path=agent_template_path,
        role_template_path=role_template_path,
        target_template_path=target_template_path,
    )

    try:
        user_query = "I want to find a restaurant in San Francisco"
        result = application.interact(
            engagement_id=engagement_id,
            raw_query=user_query,
        )
        logger.info("Detected intent: %s", result)

    except Exception as e:
        logger.error("Failed to initialize agent: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
