from utils.logging import logger
from api.webhook import app
from waitress import serve

if __name__ == "__main__":
    logger.info("Starting server...")
    serve(app, host="0.0.0.0", port=8080)
