# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : config.py               #
# ----------------------------------------------- #

# TradingView Example Alert Message:
# {
# "key":"9T2q394M92", "telegram":"-1001298977502", "discord":"789842349670960670/BFeBBrCt-w2Z9RJ2wlH6TWUjM5bJuC29aJaJ5OQv9sE6zCKY_AlOxxFwRURkgEl852s3", "msg":"Long #{{ticker}} at `{{close}}`"
# }

import os
from dotenv import load_dotenv

load_dotenv()

sec_key = os.getenv(
    "SEC_KEY"
)  # Can be anything. Has to match with "key" in your TradingView alert message

# Telegram Settings
send_telegram_alerts = True
tg_token = os.getenv("BOT_TOKEN")  # Bot token. Get it from @Botfather
channel = 0  # Channel ID (ex. -1001487568087)

# Discord Settings
send_discord_alerts = False
discord_webhook = os.getenv(
    "DISCORD_WEBHOOK"
)  # Discord Webhook URL (https://support.discordapp.com/hc/de/articles/228383668-Webhooks-verwenden)

# Slack Settings
send_slack_alerts = False
slack_webhook = os.getenv(
    "SLACK_WEBHOOK"
)  # Slack Webhook URL (https://api.slack.com/messaging/webhooks)

# Twitter Settings
send_twitter_alerts = False
tw_ckey = os.getenv("TW_CKEY")
tw_csecret = os.getenv("TW_CSECRET")
tw_atoken = os.getenv("TW_ATOKEN")
tw_asecret = os.getenv("TW_ASECRET")

# Email Settings
send_email_alerts = False
email_sender = os.getenv("EMAIL_SENDER")  # Your email address
email_receivers = [
    os.getenv("EMAIL_RECEIVER_1"),
    os.getenv("EMAIL_RECEIVER_2"),
]  # Receivers, can be multiple
email_subject = "Trade Alert!"

email_port = 465  # SMTP SSL Port (ex. 465)
email_host = os.getenv("EMAIL_HOST")  # SMTP host (ex. smtp.gmail.com)
email_user = os.getenv("EMAIL_USER")  # SMTP Login credentials
email_password = os.getenv("EMAIL_PASSWORD")  # SMTP Login credentials
