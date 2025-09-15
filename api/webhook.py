import config

from utils.handler import send_alert
from utils.logging import logger
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

whitelisted_ips = [
    "52.89.214.238",
    "34.212.75.30",
    "54.218.53.128",
    "52.32.178.7",
    "86.115.63.118",
    "127.0.0.1",  # localhost
    "172.18.0.1",  # docker bridge
]

@app.route("/")
def index():
    return jsonify({"message": "OK"}), 200

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "assets"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/webhook", methods=["POST"])
def webhook():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    logger.info(f"Client IP: {client_ip}")

    if client_ip not in whitelisted_ips:
        logger.warning(f"Unauthorized access attempt from {client_ip}")
        return jsonify({"message": "Unauthorized"}), 401
    try:
        if request.method == "POST":
            data = request.get_json()

            if data is None:
                logger.warning("No JSON payload received")
                return jsonify({"message": "Bad Request, invalid JSON payload"}), 400

            if data.get("msg") is None:
                logger.warning("No 'msg' field in the payload")
                return jsonify({"message": "Bad Request, 'msg' field is required"}), 400

            logger.info(f"Request Payload: {data}")

            if data.get("key") == config.sec_key:
                logger.info("Secured Key Matched")
                logger.info("Sending Alert...")

                e = send_alert(data, logger)
                if e:
                    logger.error(f"Error sending alert: {e}")
                    return jsonify({"message": "Error sending alert"}), 500

                return jsonify({"message": "Alert forwarded successfully"}), 200
            else:
                logger.warning("Payload Refused! (Wrong Key)")
                return jsonify({"message": "Unauthorized"}), 401
        else:
            logger.warning("Invalid request method")
            return jsonify({"message": "Method Not Allowed"}), 405
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"message": "Error"}), 400
