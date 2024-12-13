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
    restaurant_guide_agent = user_engagement_service.get_agent_with_engagement_id(
        engagement_id
    )
    try:
        while True:
            logger.debug(
                "Agent current state: %s", restaurant_guide_agent.current_state
            )
            user_query = input("User: ")
            result = restaurant_guide_agent.interact(user_query)
            logger.debug("Interaction result: %s", str(result))

            # Print agent response
            if result.is_success:
                if "llm_message" in result.message:
                    print("Agent:", result.message["llm_message"])
                elif "task_results" in result.message:
                    print("Agent: Task Results:")
                    for task_result in result.message["task_results"]:
                        print(
                            f"  - {task_result['task_name']}: {task_result['result']}"
                        )
            else:
                print("Agent Error:", result.error)

    except Exception as e:
        logger.error("Failed to initialize agent: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
