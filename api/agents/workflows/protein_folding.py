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
Workflow agent for protein folding and structure prediction.
"""

from google.adk.agents import LlmAgent
from api.config import settings
from api.tools.science.protein import predict_protein_structure, run_molecular_dynamics

protein_folding_workflow = LlmAgent(
    name="ProteinFoldingWorkflow",
    model=settings.gemini_model_powerful,
    description="Agent specialized in predicting protein structures and running simulations using AlphaFold.",
    instruction="""
    You are an expert structural biologist. Your goal is to help users predict protein 3D structures and analyze their dynamics.
    
    1. For a given amino acid sequence, use `predict_protein_structure` to run AlphaFold.
    2. Explain the confidence scores (pLDDT) and what they mean for the structural integrity.
    3. If requested, use `run_molecular_dynamics` to simulate how the protein behaves over time.
    4. Provide the GCS URIs for the resulting PDB or trajectory files.
    
    Always highlight that these computations run on Google Cloud's high-performance computing infrastructure.
    """,
    tools=[predict_protein_structure, run_molecular_dynamics],
    output_key="folding_results"
)
