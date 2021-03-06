import os
import logging
from typing import List

from fastapi import BackgroundTasks, UploadFile
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

logger = logging.getLogger()
MAIL_FROM = os.environ["MAIL_FROM"]
MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
MAIL_SERVER = os.environ["MAIL_SERVER"]
MAIL_USERNAME = os.environ["MAIL_USERNAME"]


async def send(subject: str, body: str, background_tasks: BackgroundTasks, recipient: EmailStr, file):
    try:
        conf = ConnectionConfig(
            MAIL_FROM=MAIL_FROM,
            MAIL_USERNAME=MAIL_USERNAME,
            MAIL_PASSWORD=MAIL_PASSWORD,
            MAIL_PORT=587,
            MAIL_SERVER=MAIL_SERVER,
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )

        template = f"""
        <p>{body}</p>"""

        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            html=template,
            subtype="html",
            attachments=[file] if file else []
        )

        fm = FastMail(conf)
        background_tasks.add_task(
            fm.send_message, message)
        return "emailss has been sent"

    except Exception as ex:
        logging.exception(f'Exception while sending emailss : {ex!r}')
        return f'{ex!r}'
