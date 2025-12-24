OSS Sentinel
PythonGitHubOpenAILicense

Automated AI-Driven Health Monitor & Decision Engine for Open Source Ecosystems.
The Problem
Traditional OSS metrics like Star counts and Forks are lagging indicators. They do not reflect current operational reality, maintenance burden, or developer satisfaction of a project.

OSS Sentinel addresses this gap by analyzing the "heartbeat" of a repository: its Issues. By leveraging NLP to classify sentiment and urgency, we move beyond vanity metrics to actionable insights about project stability and technical debt.

Architecture
The pipeline follows a rigorous data engineering flow:

Ingestion Layer: Connects to GitHub Search API to fetch raw issue data based on temporal and repository targets.
Processing Layer: Uses Pandas to clean, normalize, and flatten nested JSON structures into a structured schema.
Enrichment Layer: Employs OpenAI's GPT-4o-mini to perform deep semantic classification on every issue:
Sentiment: (Positive / Neutral / Negative)
Category: (Bug / Feature / Documentation / Other)
Urgency: (High / Medium / Low)
Analytics Layer: Computes a proprietary Pain Index (Sentiment × Urgency) and generates diagnostic heatmaps.
Architecture Diagram

Findings & Insights
As a Proof of Concept, OSS Sentinel analyzed the health of three major Business Intelligence tools (Apache Superset, Grafana, and Metabase) over the last 6 months (Window: 180 Days, Sample: 100 issues/repo).

Health Comparison (Pain Index)
Repository	Pain Index	Sentiment Distribution	High Urgency Rate
Grafana	-1.03	Balanced (51% Neg / 12% Pos)	25%
Metabase	-1.54	Mixed (67% Neg / 7% Pos)	41%
Apache Superset	-2.21	Critical (87% Neg)	53%
Pain Index Formula: (-1 to +1) × (Low:1 / Med:2 / High:3). Lower is "worse".

Key Insights
Grafana: The "Safe Bet"
Exhibits the lowest "Pain Score". While issues exist, they tend to be of medium urgency. The higher positive sentiment ratio indicates a healthier community response to issues.
Apache Superset: The "Trauma Hospital"
The data reveals a demanding technical debt load. The overwhelming negative sentiment (87%) coupled with the highest Urgency rate suggests the project is in a constant state of triage. Adoption requires a strong internal engineering team.
Metabase: The "Tired Middle Ground"
Sits between the two. High urgency bugs are prevalent, but the community is slightly more positive than Apache, indicating a resilient but strained support ecosystem.
How to Run
Prerequisites
Python 3.9+
GitHub Personal Access Token (Classic) with public_repo scope.
OpenAI API Key.
Installation
Clone the repository.
Install dependencies:
pip install -r requirements.txt
Configuration
Set your environment variables:

export GITHUB_TOKEN="your_github_token"export OPENAI_API_KEY="your_openai_key"
Execution
Run the full pipeline:
python main.py

Or run specific modules:

python src/ingestion.py
python src/processing.py
python src/enrichment.py
python src/analyze.py

Results and plots will be saved in assets/plots/ and data/analysis/.

License
Distributed under the MIT License. See LICENSE for more information.

