#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notification Helper - Creates a simple bot for push notifications
"""

import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

class NotificationHelper:
    def __init__(self, api_id: int, api_hash: str, session_string: str, target_user_id: int):
        self.client = TelegramClient(StringSession(session_string), api_id, api_hash)
        self.target_user_id = target_user_id
    
    async def send_push_notification(self, message: str):
        """Send a push notification that will appear on phone"""
        try:
            await self.client.start()
            
            # Send to the target user (yourself) - this creates a private chat notification
            await self.client.send_message(self.target_user_id, message)
            
            await self.client.disconnect()
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False

# Function to be called from main bot
async def send_phone_notification(api_id: int, api_hash: str, session_string: str, 
                                target_user_id: int, message: str):
    """Send a notification that will appear on phone"""
    helper = NotificationHelper(api_id, api_hash, session_string, target_user_id)
    return await helper.send_push_notification(message)
