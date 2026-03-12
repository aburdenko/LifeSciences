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
Workflow agent for biological pathway analysis and network modeling.
"""

from google.adk.agents import LlmAgent
from api.config import settings
from api.tools.science.pathway import analyze_biological_pathway, query_biomedical_graph

pathway_analysis_workflow = LlmAgent(
    name="PathwayAnalysisWorkflow",
    model=settings.gemini_model_powerful,
    description="Agent specialized in analyzing biological pathways and querying biomedical knowledge graphs.",
    instruction="""
    You are an expert bioinformatician and systems biologist.
    
    1. If provided with a list of genes or proteins, use `analyze_biological_pathway` to identify significant biological pathways.
    2. Use `query_biomedical_graph` to find connections between specific biological entities (genes, drugs, diseases).
    3. Synthesize these findings to explain the mechanism of a disease or the effect of a drug at a network level.
    4. Provide insights into potential drug targets based on the connectivity in the graph.
    
    Always use scientific terminology correctly.
    """,
    tools=[analyze_biological_pathway, query_biomedical_graph],
    output_key="pathway_results"
)
