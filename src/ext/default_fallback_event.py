"""Default fallback event for the restaurant domain"""

from utils.logging import logging

logger = logging.getLogger(__name__)


def gently_ask_for_relevant_information() -> str:
    """gently_ask_for_relevant_information() -> None"""
    logger.info("<Target is asking info that not related to this role>")
    return "True"
