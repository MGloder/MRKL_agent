"""Service module for various functionalities."""
from .service_center import ServiceCenterInitializer

# Create default app configuration
service_center = ServiceCenterInitializer.initialize()

__all__ = ["service_center"]
