import os

# Root project folder
ROOT = "agentic-pharma-ai"

# Folder structure
folders = [
    f"{ROOT}/src",
    f"{ROOT}/src/graph",
    f"{ROOT}/src/agents",
    f"{ROOT}/src/tools",
    f"{ROOT}/src/services",
    f"{ROOT}/src/models",
    f"{ROOT}/src/database",
    f"{ROOT}/src/ui",
    f"{ROOT}/src/ui/templates",
    f"{ROOT}/src/report",
    f"{ROOT}/src/logging",
    f"{ROOT}/src/utils",
    f"{ROOT}/demos",
    f"{ROOT}/tests/unit",
    f"{ROOT}/tests/integration",
    f"{ROOT}/tests/mock_data",
    f"{ROOT}/reports/archived_reports",
]

# Files to create
files = [
    f"{ROOT}/README.md",
    f"{ROOT}/LICENSE",
    f"{ROOT}/requirements.txt",
    f"{ROOT}/.env.example",
    f"{ROOT}/config.yaml",

    f"{ROOT}/src/main.py",
    f"{ROOT}/src/app.py",

    f"{ROOT}/src/graph/__init__.py",
    f"{ROOT}/src/graph/graph_definition.py",
    f"{ROOT}/src/graph/state.py",
    f"{ROOT}/src/graph/router.py",
    f"{ROOT}/src/graph/utils.py",

    f"{ROOT}/src/agents/__init__.py",
    f"{ROOT}/src/agents/regulator_agent.py",
    f"{ROOT}/src/agents/clinical_trials_agent.py",
    f"{ROOT}/src/agents/scientific_journal_agent.py",
    f"{ROOT}/src/agents/patent_agent.py",
    f"{ROOT}/src/agents/summarizer_agent.py",

    f"{ROOT}/src/tools/__init__.py",
    f"{ROOT}/src/tools/web_scraper.py",
    f"{ROOT}/src/tools/clinical_db_connector.py",
    f"{ROOT}/src/tools/regulatory_api_connector.py",
    f"{ROOT}/src/tools/patent_api_connector.py",
    f"{ROOT}/src/tools/summarization.py",

    f"{ROOT}/src/services/storage_service.py",
    f"{ROOT}/src/services/search_service.py",
    f"{ROOT}/src/services/llm_service.py",
    f"{ROOT}/src/services/vector_store_service.py",

    f"{ROOT}/src/models/clinical_trial_schema.py",
    f"{ROOT}/src/models/regulatory_schema.py",
    f"{ROOT}/src/models/patent_schema.py",
    f"{ROOT}/src/models/molecule_schema.py",

    f"{ROOT}/src/database/mongo_client.py",
    f"{ROOT}/src/database/vector_db_client.py",

    f"{ROOT}/src/ui/__init__.py",
    f"{ROOT}/src/ui/api.py",
    f"{ROOT}/src/ui/streamlit_app.py",

    f"{ROOT}/src/report/generator.py",
    f"{ROOT}/src/report/exporter.py",
    f"{ROOT}/src/report/storage.py",

    f"{ROOT}/src/logging/logger.py",
    f"{ROOT}/src/logging/monitoring.py",

    f"{ROOT}/src/utils/error_handler.py",
    f"{ROOT}/src/utils/config_loader.py",
    f"{ROOT}/src/utils/constants.py",

    f"{ROOT}/demos/demo_notebook.ipynb",
    f"{ROOT}/demos/example_inputs.md",

    f"{ROOT}/tests/unit/test_agents.py",
    f"{ROOT}/tests/unit/test_tools.py",
    f"{ROOT}/tests/unit/test_graph.py",
    f"{ROOT}/tests/integration/test_end_to_end_pipeline.py",
    f"{ROOT}/tests/mock_data/sample_html.html",
]

# Create directories
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create each file with empty content (or default header)
for file in files:
    with open(file, "w") as f:
        f.write("# placeholder\n")

print("\n🥳 Repository structure successfully created!")
print(f"📁 Root folder: {ROOT}")
