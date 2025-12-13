#!/usr/bin/env python3
"""
Quick test script for the orchestrator without FastAPI server.
Run directly: python test_orchestrator_direct.py
"""

import sys
import asyncio
from datetime import datetime
import os

# Set up path so `src` modules import correctly
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, "src")
# Prefer adding the src directory so imports like `from graph.state import ...` work
if os.path.isdir(src_dir):
    sys.path.insert(0, src_dir)
# Also add project root as a fallback
sys.path.insert(0, script_dir)
os.chdir(script_dir)

def test_orchestrator():
    """Test the orchestrator directly"""
    try:
        print("=" * 80)
        print("PHARMACEUTICAL RESEARCH ORCHESTRATOR - DIRECT TEST")
        print("=" * 80)
        print()
        
        # Test 1: Clinical Trial Query
        print("[TEST 1] Clinical Trial Query")
        print("-" * 80)
        query1 = "What are the latest clinical trials for cancer treatment?"
        print(f"Query: {query1}")
        print()
        
        orchestrator_available = False
        try:
            from orchestrator import run_orchestrator, format_response
            orchestrator_available = True
            print("Running orchestrator...")
            print("(Note: Requires LLM configured in src/services/llm_service.py)")
            final_state = run_orchestrator(query1)
            final_response = format_response(final_state)

            print(f"\n✓ Response:")
            print(f"  {final_response[:200]}...")
            print(f"\n✓ State Messages: {len(final_state['message'])}")

        except Exception as e:
            print(f"✗ Error: {e}")
            print("\nNote: Ensure llm_service.py is configured with valid API key")
        
        print("\n")
        
        # Test 2: Patent Query
        print("[TEST 2] Patent Query")
        print("-" * 80)
        query2 = "Search for patents related to drug formulation"
        print(f"Query: {query2}")
        print()
        
        if orchestrator_available:
            try:
                final_state = run_orchestrator(query2)
                final_response = format_response(final_state)

                print(f"✓ Response:")
                print(f"  {final_response[:200]}...")
                print(f"\n✓ State Messages: {len(final_state['message'])}")

            except Exception as e:
                print(f"✗ Error: {e}")
        else:
            print("✗ Orchestrator unavailable — skipping this test (import failed earlier)")
        
        print("\n")
        
        # Test 3: Data Tools Direct Access
        print("[TEST 3] Data Tools Direct Access")
        print("-" * 80)
        
        try:
            from tools.clinical_trials_data import get_clinical_trial_data, get_all_clinical_trials
            from tools.patent_data import get_all_patents
            from tools.regulatory_data import get_approved_drugs
            from tools.scientific_journal_data import get_all_articles
        except ImportError as e:
            print(f"✗ Import Error: {e}")
            print("Skipping data tools test")
            print("\n")
            return

        print("\n1. Clinical Trials:")
        trials_result = get_all_clinical_trials()
        trials = trials_result.get('trials', [])
        print(f"   ✓ Found {len(trials)} trials")
        for trial in trials[:1]:
            print(f"     - {trial.get('drug_name', 'N/A')}: {trial.get('title', 'N/A')[:60]}...")
        
        print("\n2. Patents:")
        patents_result = get_all_patents()
        patents = patents_result.get('patents', [])
        print(f"   ✓ Found {len(patents)} patents")
        for patent in patents[:1]:
            print(f"     - {patent.get('patent_id', 'N/A')}: {patent.get('title', 'N/A')[:60]}...")
        
        print("\n3. Regulatory Approved Drugs:")
        approved_result = get_approved_drugs()
        approved = approved_result.get('applications', [])
        print(f"   ✓ Found {len(approved)} approved drugs")
        for drug in approved[:1]:
            print(f"     - {drug.get('nda_id', 'N/A')}: {drug.get('drug_name', 'N/A')}")
        
        print("\n4. Journal Articles:")
        articles_result = get_all_articles()
        articles = articles_result.get('articles', [])
        print(f"   ✓ Found {len(articles)} articles")
        for article in articles[:1]:
            doi = article.get('doi', article.get('DOI', 'N/A'))
            title = article.get('title', 'N/A')
            print(f"     - {doi}: {title[:60]}...")
            print(f"     - DOI: {doi}")
            print(f"     - Title: {title}")
        
        print("\n")
        
        # Test 4: Router
        print("[TEST 4] Query Router")
        print("-" * 80)
        
        from src.graph.router import route_query
        from src.graph.state import State
        from langchain_core.messages import HumanMessage
        
        test_queries = [
            "What clinical trials are recruiting?",
            "Show me active patents",
            "FDA approval status",
            "Recent cancer research papers"
        ]
        
        for test_query in test_queries:
            state = State(
                system_prompt="",
                clinical_trials_prompt="",
                patent_prompt="",
                regulator_prompt="",
                scientific_journal_prompt="",
                message=[HumanMessage(content=test_query)]
            )
            try:
                result = route_query(state)
                print(f"✓ '{test_query[:40]}...' → {result}")
            except Exception as e:
                print(f"✗ Routing error for '{test_query[:40]}...': {e}")
        
        print("\n")
        print("=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        print("\nNext Steps:")
        print("1. Configure LLM in src/services/llm_service.py")
        print("2. Run: uvicorn src.app:app --reload")
        print("3. Visit: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_orchestrator()
