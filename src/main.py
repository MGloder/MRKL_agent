"""main function for testing the agent initialization and intent detection"""
from service.user_engagement_service import UserEngagementService
from utils.logging import logging

logger = logging.getLogger(__name__)


def main():
    """Main function for testing the agent initialization and intent detection"""
    logger.info("Starting agent initialization...")
    agent_template_path = "./src/config/agent_template/restaurant_guide_agent.yaml"
    role_template_path = "./src/config/role_template/restaurant_guide_role.yaml"
    target_template_path = "./src/config/target_template/user.yaml"
    user_engagement_service = UserEngagementService()
    engagement_id = user_engagement_service.create_engagement(
        agent_template_path=agent_template_path,
        role_template_path=role_template_path,
        target_template_path=target_template_path,
    )

    try:
        user_query = "I want to find a good restaurant in the city"
        restaurant_guide_agent = user_engagement_service.get_agent_with_engagement_id(
            engagement_id
        )
        result = restaurant_guide_agent.interact(user_query)
        logger.info("Interaction result: %s", str(result))

    except Exception as e:
        logger.error("Failed to initialize agent: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
