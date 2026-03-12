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
Scientific Database Agent for drug discovery and molecule lookup.
"""

from google.adk.agents import LlmAgent
from api.config import settings
from api.tools.chembl import lookup_molecule, get_bioactivity

# Define the Scientific Database Agent
scientific_db_agent = LlmAgent(
    name="ScientificDBAgent",
    model=settings.gemini_model_powerful,
    description="Agent specialized in looking up molecular and bioactivity data from scientific databases like ChEMBL.",
    instruction="""
    You are an expert computational chemist and drug discovery scientist.
    
    Your task is to help users find information about molecules, their structures, and their biological activities.
    
    When a user asks about a molecule or drug:
    1. Use `lookup_molecule` to find its ChEMBL ID and basic properties.
    2. Use `get_bioactivity` to find its known targets and assay results.
    3. Explain the mechanism of action if known.
    4. Provide structured data about the molecule.
    
    If a molecule is not found, state that it's not in the current database.
    """,
    tools=[lookup_molecule, get_bioactivity],
    output_key="molecule_info"
)
