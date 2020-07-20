# -*- coding: utf-8 -*-

import asyncio
from tornado.options import options
import json
from bms.v1.feedback import ForwardFeedback

class EventListener():

    actions = [
        'FEEDBACK.CREATE'
    ]

    def __init__(self, application):
        self.application = application
        self.conn = None
    
    async def start(self):
        if self.conn is None:
            self.conn = await self.application.pool.acquire()

        for action in self.actions:
            await self.conn.add_listener(action, self.callback)

    async def stop(self):
        for action in self.actions:
            await self.conn.remove_listener(action, self.callback)

        await self.conn.close()

    def callback(self, conn, pid, action, payload):

        if action in self.actions:

            exe = None
            request = {}

            if action == 'FEEDBACK.CREATE':
                try:
                    exe = ForwardFeedback(self.conn)

                    # Extract feedback id from payload
                    feb_id = int(payload)

                    # Prepare request
                    request = {
                        "feb_id": feb_id,
                        "username": options.smtp_username,
                        "password": options.smtp_password,
                        "recipients": options.smtp_recipients,
                        "server": options.smtp_server,
                        "port": options.smtp_port,
                        "tls": options.smtp_tls,
                        "starttls": options.smtp_starttls,
                    }

                except Exception as ex:
                    print(ex)

            else:
                print(f"Action unknown: {action}")

            if exe is not None:
                asyncio.create_task(
                    exe.execute(**request)
                )

        else:
            print(f"Unknown event action: {action}")
