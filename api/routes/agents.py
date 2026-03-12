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
API routes for agentic interactions.
"""

from fastapi import APIRouter, Depends, Header
from fastapi.responses import StreamingResponse
from typing import Optional
import uuid

from api.services.agent_service import AgentService
from api.dependencies import get_agent_service

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.post("/chat")
async def chat(
    query: str,
    user_id: str = Header(default="anonymous"),
    session_id: Optional[str] = Header(default=None),
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Interact with the Sentinel Life Sciences Agentic Coordinator.
    """
    if not session_id:
        session_id = str(uuid.uuid4())
        
    async def response_generator():
        async for chunk in agent_service.process_request(user_id, session_id, query):
            yield chunk

    return StreamingResponse(response_generator(), media_type="text/plain")
