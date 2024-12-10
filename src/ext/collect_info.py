"""This module contains functions that simulate the process of collecting user information."""

from utils.logging import logging

logger = logging.getLogger(__name__)


def ask_geo_location() -> str:
    """ask_geo_location() -> None"""
    logger.info("Asking for geographical location...")
    return "True"


def ask_credit_card_type_issuer() -> str:
    """ask_credit_card_type_issuer() -> None"""
    logger.info("Asking for credit card type and issuer...")
    return "True"


def ask_price_range() -> str:
    """ask_price_range() -> None"""
    logger.info("Asking for price range...")
    return "True"


def ask_rating_range() -> str:
    """ask_rating_range() -> None"""
    logger.info("Asking for rating range...")
    return "True"


def ask_customize_preferences() -> str:
    """ask_customize_preferences() -> None"""
    logger.info("Asking to customize preferences...")
    return "True"
