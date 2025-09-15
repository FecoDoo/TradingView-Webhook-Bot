# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : handler.py              #
# ----------------------------------------------- #

import smtplib
import ssl
from email.mime.text import MIMEText

import tweepy
from discord_webhook import DiscordEmbed, DiscordWebhook
from slack_webhook import Slack
from telegram import Bot

import config


def send_alert(data, logger=None) -> Exception | None:
    msg = data["msg"].encode("latin-1", "backslashreplace").decode("unicode_escape")

    if config.send_telegram_alerts:
        if config.tg_token is None or config.tg_token == "":
            if logger:
                logger.error("Telegram bot token is not set.")
            return Exception("Telegram bot token is not set.")

        logger.info("Sending to Telegram...")
        tg_bot = Bot(token=config.tg_token)
        try:
            tg_bot.sendMessage(
                data["telegram"],
                msg,
                parse_mode="MARKDOWN",
            )
        except KeyError:
            tg_bot.sendMessage(
                config.channel,
                msg,
                parse_mode="MARKDOWN",
            )
        except Exception as e:
            return e

    if config.send_discord_alerts:
        if config.discord_webhook is None or config.discord_webhook == "":
            if logger:
                logger.error("Discord webhook URL is not set.")
            return Exception("Discord webhook URL is not set.")

        logger.info("Sending to Discord...")
        try:
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/" + data["discord"]
            )
            embed = DiscordEmbed(title=msg)
            webhook.add_embed(embed)
            webhook.execute()
        except KeyError:
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/" + config.discord_webhook
            )
            embed = DiscordEmbed(title=msg)
            webhook.add_embed(embed)
            webhook.execute()
        except Exception as e:
            return e

    if config.send_slack_alerts:
        if config.slack_webhook is None or config.slack_webhook == "":
            if logger:
                logger.error("Slack webhook URL is not set.")
            return Exception("Slack webhook URL is not set.")

        logger.info("Sending to Slack...")
        try:
            slack = Slack(url="https://hooks.slack.com/services/" + data["slack"])
            slack.post(text=msg)
        except KeyError:
            slack = Slack(
                url="https://hooks.slack.com/services/" + config.slack_webhook
            )
            slack.post(text=msg)
        except Exception as e:
            return e

    if config.send_twitter_alerts:
        if (
            config.tw_ckey is None
            or config.tw_ckey == ""
            or config.tw_csecret is None
            or config.tw_csecret == ""
            or config.tw_atoken is None
            or config.tw_atoken == ""
            or config.tw_asecret is None
            or config.tw_asecret == ""
        ):
            if logger:
                logger.error("Twitter API credentials are not fully set.")
            return Exception("Twitter API credentials are not fully set.")

        logger.info("Sending to Twitter...")
        tw_auth = tweepy.OAuthHandler(config.tw_ckey, config.tw_csecret)
        tw_auth.set_access_token(config.tw_atoken, config.tw_asecret)
        tw_api = tweepy.API(tw_auth)
        try:
            tw_api.update_status(
                status=msg.replace("*", "").replace("_", "").replace("`", "")
            )
        except Exception as e:
            return e

    if config.send_email_alerts:
        if (
            config.email_sender is None
            or config.email_sender == ""
            or config.email_receivers is None
            or not any(config.email_receivers)
            or config.email_host is None
            or config.email_host == ""
            or config.email_port is None
            or config.email_port == ""
            or config.email_user is None
            or config.email_user == ""
            or config.email_password is None
            or config.email_password == ""
        ):
            if logger:
                logger.error("Email settings are not fully set.")
            return Exception("Email settings are not fully set.")

        logger.info("Sending to Email...")
        try:
            email_msg = MIMEText(msg.replace("*", "").replace("_", "").replace("`", ""))
            email_msg["Subject"] = config.email_subject
            email_msg["From"] = config.email_sender
            email_msg["To"] = config.email_sender
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                config.email_host, config.email_port, context=context
            ) as server:
                server.login(config.email_user, config.email_password)
                server.sendmail(
                    config.email_sender, config.email_receivers, email_msg.as_string()
                )
                server.quit()
        except Exception as e:
            return e

    return None
