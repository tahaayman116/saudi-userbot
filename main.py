#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for Replit deployment
Starts keep-alive server and the user bot
بدون الحاجة لـ UptimeRobot - keep-alive داخلي!
"""

import asyncio
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Start keep-alive server
try:
    from keep_alive import keep_alive, internal_ping
    keep_alive()
    logger.info("✅ Keep-alive server started")
except Exception as e:
    logger.warning(f"⚠️ Could not start keep-alive server: {e}")

# Import and run the bot
try:
    logger.info("🚀 Starting Saudi User Bot...")
    
    # Import the main bot module
    from cloud_userbot import main
    
    # Create event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Start internal ping in background
    try:
        loop.create_task(internal_ping())
        logger.info("✅ Internal keep-alive ping started - No need for UptimeRobot!")
    except:
        logger.info("⚠️ Internal ping not available, but bot will still work")
    
    # Run the bot
    loop.run_until_complete(main())
    
except KeyboardInterrupt:
    logger.info("🛑 Bot stopped by user")
except Exception as e:
    logger.error(f"❌ Fatal error: {e}")
    sys.exit(1)

