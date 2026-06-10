#!/usr/bin/env python3

import os
import sys
import requests


def log(msg: str):
    print(f"[on_receive] {msg}", file=sys.stderr)


def getenv_required(name: str):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def main():
    try:
        phone_id = getenv_required("PHONE_ID")

        bot_token = getenv_required(f"TELEGRAM_BOT_TOKEN_{phone_id}")
        chat_id = getenv_required(f"TELEGRAM_CHAT_ID_{phone_id}")
        message_thread_id = getenv_required(f"MESSAGE_THREAD_ID_{phone_id}")

        sms_from = os.getenv("SMS_1_NUMBER", "unknown")
        sms_text = os.getenv("SMS_1_TEXT", "")
    
    except Exception as e:
        log(f"unable to load required env variable: {str(e)}")

    message = (
        "📩 New SMS\n\n"
        f"Modem: {phone_id}\n"
        f"From: {sms_from}\n"
        f"{sms_text}"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    try:
        r = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": message,
                "message_thread_id": message_thread_id,
                "disable_web_page_preview": True,
            },
            timeout=10,
        )

        if r.status_code != 200:
            log(f"ERROR: Telegram API returned {r.status_code}: {r.text}")

    except Exception as e:
        log(f"ERROR: failed to send Telegram message: {e}")

    log(f"Forwarded SMS via modem {phone_id} from {sms_from}")


if __name__ == "__main__":
    main()