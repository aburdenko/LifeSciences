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
Literature Agent for biomedical research and literature discovery.
"""

from google.adk.agents import LlmAgent
from api.config import settings
from api.tools.pubmed import search_pubmed, fetch_abstract

# Define the Literature Agent
literature_agent = LlmAgent(
    name="LiteratureAgent",
    model=settings.gemini_model_powerful, # Use Powerful for better scientific reasoning
    description="Agent specialized in searching and summarizing biomedical literature from PubMed and other sources.",
    instruction="""
    You are an expert biomedical researcher. Your task is to help users find and understand scientific literature.
    
    When a user asks about a medical topic or research:
    1. Use the `search_pubmed` tool to find relevant papers.
    2. If needed, use `fetch_abstract` to get more details about a specific paper.
    3. Summarize the findings clearly, citing the PMIDs.
    4. Provide links to the papers if available.
    
    Always maintain a professional and scientific tone.
    """,
    tools=[search_pubmed, fetch_abstract],
    output_key="literature_summary"
)
