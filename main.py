#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for Replit deployment
Starts keep-alive server and the user bot
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
    from keep_alive import keep_alive
    keep_alive()
    logger.info("✅ Keep-alive server started")
except Exception as e:
    logger.warning(f"⚠️ Could not start keep-alive server: {e}")

# Import and run the bot
try:
    logger.info("🚀 Starting Saudi User Bot...")
    
    # Import the main bot module
    from cloud_userbot import main
    
    # Run the bot
    asyncio.run(main())
    
except KeyboardInterrupt:
    logger.info("🛑 Bot stopped by user")
except Exception as e:
    logger.error(f"❌ Fatal error: {e}")
    sys.exit(1)
