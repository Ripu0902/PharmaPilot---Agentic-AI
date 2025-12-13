"""
Clinical Trials Data Tool
Retrieves clinical trial data from dummy database
"""
import json
from typing import Optional, List, Dict


# Dummy Clinical Trials Database
CLINICAL_TRIALS_DB = {
    "NCT04567890": {
        "title": "Phase 3 Clinical Trial for Cancer Drug XYZ",
        "drug_name": "Cancer Drug XYZ",
        "phase": "Phase 3",
        "status": "Recruiting",
        "enrollment": 500,
        "primary_outcome": "Overall Survival",
        "efficacy_rate": "82%",
        "safety_profile": "Well tolerated, mild side effects",
        "adverse_events": ["Nausea (15%)", "Fatigue (10%)", "Hair loss (20%)"],
        "patient_demographics": {
            "age_range": "45-75 years",
            "gender_ratio": "50/50",
            "cancer_type": "Non-small cell lung cancer"
        },
        "duration": "24 months",
        "sponsor": "PharmaCorp Inc"
    },
    "NCT04123456": {
        "title": "Phase 2 Trial for Diabetes Treatment DTZ-100",
        "drug_name": "DTZ-100",
        "phase": "Phase 2",
        "status": "Active",
        "enrollment": 300,
        "primary_outcome": "HbA1c Reduction",
        "efficacy_rate": "78%",
        "safety_profile": "Generally safe with acceptable tolerability",
        "adverse_events": ["Gastrointestinal upset (8%)", "Headache (5%)"],
        "patient_demographics": {
            "age_range": "30-65 years",
            "gender_ratio": "55/45",
            "condition": "Type 2 Diabetes"
        },
        "duration": "12 months",
        "sponsor": "EndoPharm LLC"
    },
    "NCT03987654": {
        "title": "Phase 1 Safety Study for Immunotherapy IMT-50",
        "drug_name": "IMT-50",
        "phase": "Phase 1",
        "status": "Enrolling by invitation",
        "enrollment": 50,
        "primary_outcome": "Safety and Tolerability",
        "efficacy_rate": "Early data promising",
        "safety_profile": "Dose escalation ongoing",
        "adverse_events": ["Cytokine release syndrome (Grade 1-2)"],
        "patient_demographics": {
            "age_range": "18-70 years",
            "cancer_type": "Advanced melanoma"
        },
        "duration": "6 months",
        "sponsor": "ImmunoGen Corp"
    }
}


def get_clinical_trial_data(query: str) -> Dict:
    """
    Retrieves clinical trial data from dummy database
    
    Args:
        query: Search query (drug name, NCT number, or trial phase)
        
    Returns:
        Dictionary with matching trial data
    """
    query_lower = query.lower()
    results = {}
    
    # Search by NCT number
    if query_lower.startswith("nct"):
        if query in CLINICAL_TRIALS_DB:
            return {"found": True, "trials": [CLINICAL_TRIALS_DB[query]]}
        else:
            return {"found": False, "message": f"NCT {query} not found"}
    
    # Search by drug name or phase
    for nct_number, trial_data in CLINICAL_TRIALS_DB.items():
        if (query_lower in trial_data.get("drug_name", "").lower() or
            query_lower in trial_data.get("phase", "").lower() or
            query_lower in trial_data.get("title", "").lower()):
            results[nct_number] = trial_data
    
    if results:
        return {"found": True, "trials": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No trials found for '{query}'"}


def get_all_clinical_trials() -> Dict:
    """
    Retrieves all clinical trials from dummy database
    
    Returns:
        Dictionary with all trials
    """
    return {
        "found": True,
        "trials": list(CLINICAL_TRIALS_DB.values()),
        "count": len(CLINICAL_TRIALS_DB)
    }


def get_trial_by_phase(phase: str) -> Dict:
    """
    Get clinical trials by phase
    
    Args:
        phase: Trial phase (Phase 1, Phase 2, Phase 3, Phase 4)
        
    Returns:
        Dictionary with matching trials
    """
    phase_lower = phase.lower()
    results = {}
    
    for nct_number, trial_data in CLINICAL_TRIALS_DB.items():
        if phase_lower in trial_data.get("phase", "").lower():
            results[nct_number] = trial_data
    
    if results:
        return {"found": True, "trials": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No trials found for {phase}"}


def format_trial_for_llm(trial_data: Dict) -> str:
    """
    Format trial data for LLM processing
    
    Args:
        trial_data: Trial dictionary
        
    Returns:
        Formatted string representation
    """
    formatted = f"""
CLINICAL TRIAL DATA:
- Title: {trial_data.get('title', 'N/A')}
- NCT Number: {trial_data.get('nct_number', 'N/A')}
- Drug: {trial_data.get('drug_name', 'N/A')}
- Phase: {trial_data.get('phase', 'N/A')}
- Status: {trial_data.get('status', 'N/A')}
- Enrollment: {trial_data.get('enrollment', 'N/A')} participants
- Primary Outcome: {trial_data.get('primary_outcome', 'N/A')}
- Efficacy Rate: {trial_data.get('efficacy_rate', 'N/A')}
- Safety Profile: {trial_data.get('safety_profile', 'N/A')}
- Adverse Events: {', '.join(trial_data.get('adverse_events', []))}
- Trial Duration: {trial_data.get('duration', 'N/A')}
- Sponsor: {trial_data.get('sponsor', 'N/A')}
"""
    return formatted
