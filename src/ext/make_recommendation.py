"""make recommendation module"""
from utils.logging import logging

logger = logging.getLogger(__name__)


def generate_recommendation() -> str:
    """Generate recommendation for the user"""
    logger.info("<Recommendation generated>")
    return "True"
