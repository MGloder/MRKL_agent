# Configure logging.py
import logging

# Update format to include class name
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # This will print to console as well
    ],
)
