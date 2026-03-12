# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Agent service for managing ADK agent execution.
"""

import logging
from typing import AsyncGenerator
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from api.agents.coordinator import sentinel_coordinator
from api.config import settings

logger = logging.getLogger(__name__)

class AgentService:
    """
    Service for orchestrating agentic workflows using ADK.
    """
    
    def __init__(self, session_service=None):
        self.session_service = session_service or InMemorySessionService()
        self.runner = Runner(
            agent=sentinel_coordinator,
            app_name="SentinelLifeSciences",
            session_service=self.session_service
        )
        
    async def process_request(
        self, 
        user_id: str, 
        session_id: str, 
        query: str
    ) -> AsyncGenerator[str, None]:
        """
        Process a user request through the agentic coordinator.
        
        Yields:
            Chunks of the agent's response text.
        """
        logger.info(f"Processing agentic request for user {user_id}, session {session_id}")
        
        # Ensure session exists
        try:
            await self.session_service.get_session("SentinelLifeSciences", user_id, session_id)
        except:
            await self.session_service.create_session("SentinelLifeSciences", user_id, session_id)
            
        content = types.Content(role='user', parts=[types.Part(text=query)])
        
        async for event in self.runner.run_async(
            user_id=user_id, 
            session_id=session_id, 
            new_message=content
        ):
            # Check if event has content and parts
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        yield part.text
            
            # You can also yield other event types like tool calls if desired
            if event.type == "tool_call":
                logger.info(f"Agent tool call: {event.tool_name}")
