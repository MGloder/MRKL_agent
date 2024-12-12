"""This module contains functions that simulate the process of collecting user information."""
from utils import tools
from utils.logging import logging

logger = logging.getLogger(__name__)


def collect_information(
    location: str, rating_range: str, custom_preference: str
) -> dict:
    """Collect information from the user and return the restaurant information"""
    query = f"Restaurant, Location: {location}, Rating: {rating_range}, Preference: {custom_preference}"
    logger.info("Get restaurant information based on the query: %s", query)
    return tools.make_google_place_api_call(query=query)
