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
Central Platform Coordinator for Life Sciences workflows.
"""

from google.adk.agents import LlmAgent
from api.config import settings
from api.agents.workflows.protein_folding import protein_folding_workflow
from api.agents.workflows.pathway_analysis import pathway_analysis_workflow
from api.agents.workflows.sentinel import sentinel_workflow
from api.agents.experts.literature import literature_agent
from api.agents.experts.scientific_db import scientific_db_agent

# Define the Life Sciences Platform Agent
# This is the root agent that understands the user's intent and delegates to the correct workflow.
sentinel_coordinator = LlmAgent(
    name="LifeSciencesPlatform",
    model=settings.gemini_model_powerful,
    description="The central coordinator for Google Cloud Life Sciences Platform. Routes to specialized scientific workflows.",
    instruction="""
    You are the Google Cloud Life Sciences Platform Assistant. 
    You manage a suite of specialized agentic workflows to help scientists and researchers.
    
    Your available workflows and experts are:
    1. `ProteinFoldingWorkflow`: Use this for protein structure prediction, AlphaFold, and molecular dynamics.
    2. `PathwayAnalysisWorkflow`: Use this for gene enrichment, network modeling, and biological pathway analysis.
    3. `SentinelWorkflow`: Use this for pharmaceutical advertising compliance and content review.
    4. `LiteratureAgent`: Expert for general biomedical literature search (PubMed).
    5. `ScientificDBAgent`: Expert for looking up molecules and bioactivity (ChEMBL).
    
    When a user provides a request:
    - Identify the primary scientific domain (e.g., Structural Biology, Bioinformatics, Regulatory, etc.).
    - Delegate the task to the most appropriate Workflow agent or Expert agent.
    - If a task requires multiple steps (e.g., find a protein in a paper then fold it), coordinate between agents sequentially.
    - Always emphasize the optimization for Google Cloud (Vertex AI, BigQuery, HPC).
    
    Be precise, scientific, and helpful.
    """,
    sub_agents=[
        protein_folding_workflow, 
        pathway_analysis_workflow, 
        sentinel_workflow,
        literature_agent,
        scientific_db_agent
    ]
)
