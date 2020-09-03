# -*- coding: utf-8 -*-
from bms.v1.action import Action
from email.message import EmailMessage
import aiosmtplib


class SendMail(Action):

    async def execute(
        self,
        username,
        password,
        recipients, # csv list of emails
        subject,
        message,
        server,
        port=587,
        tls=False,
        starttls=False,  # usually on port 587
        sender=None
    ):
        
        try:

            msg = EmailMessage()
            msg["From"] = username
            msg["To"] = recipients
            msg["Subject"] = subject
            msg.set_content(message)
            await aiosmtplib.send(
                msg,
                hostname=server,
                port=port,
                username=username,
                password=password,
                use_tls=tls,
                start_tls=starttls
            )

            return None

        except Exception:
            raise Exception("Error while sending email")
