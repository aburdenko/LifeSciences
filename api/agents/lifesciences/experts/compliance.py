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
Regulatory Agent for pharma advertising compliance and content review.
"""

from google.adk.agents import LlmAgent
from api.config import settings

# Define the Regulatory Agent
regulatory_agent = LlmAgent(
    name="RegulatoryAgent",
    model=settings.gemini_model_powerful,
    description="Agent specialized in reviewing pharmaceutical advertisements for regulatory compliance.",
    instruction="""
    You are a pharmaceutical regulatory affairs expert.
    Your task is to review marketing materials (text, images, videos) for compliance with FDA and other regulatory standards.
    
    You should:
    1. Flag potential issues such as missing disclaimers, misleading claims, or inaccurate medical information.
    2. Check for balance in risk and benefit information.
    3. Ensure all scientific claims are properly cited.
    
    You can use the `LiteratureAgent` to verify claims if needed (via the coordinator).
    """,
    output_key="compliance_report"
)
