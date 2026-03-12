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
Workflow agent for pharma regulatory compliance (the original Sentinel workflow).
"""

from google.adk.agents import LlmAgent
from api.config import settings
from api.agents.experts.compliance import regulatory_agent

sentinel_workflow = LlmAgent(
    name="SentinelWorkflow",
    model=settings.gemini_model_powerful,
    description="Agent specialized in pharma advertising compliance and promotional content review.",
    instruction="""
    You are the Sentinel Regulatory Assistant. Your goal is to ensure pharma marketing materials are compliant.
    
    1. Review the provided content (text, image context, or video transcripts).
    2. Delegate the deep analysis to the `RegulatoryAgent` expert.
    3. Verify that all medical claims are backed by literature if needed.
    4. Provide a structured compliance report.
    
    Maintain the standard Sentinel rigor for FDA/EMA compliance.
    """,
    sub_agents=[regulatory_agent],
    output_key="sentinel_compliance_report"
)
