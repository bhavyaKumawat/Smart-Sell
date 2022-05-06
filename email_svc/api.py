import os
import asyncio
import logging
from typing import List, Optional

from fastapi import FastAPI, status, BackgroundTasks, UploadFile, File, Form, Query, Depends
from pydantic import EmailStr

from email_svc.email_operations import send


description = """
SmartSell API to send emails
"""
tags_metadata = [
    {
        "name": "SmartSell Email",
        "description": "Send Email",
    },
]
logger = logging.getLogger()
ss_email = FastAPI(
    title="SmartSell Email API",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata
)


@ss_email.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@ss_email.get('/v1/healthcheck', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}


@ss_email.post('/api/send_mail')
async def send_mail(subject: str = Form(...), body: str = Form(...), background_tasks: BackgroundTasks = Form(...),
                    recipient: EmailStr = Form(..., description="user@example.com"),
                    file: Optional[UploadFile] = File(None)):
    message = await send(subject, body, background_tasks, recipient, file)
    return {"message": message}
