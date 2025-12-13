"""
Regulatory Data Tool
Retrieves FDA approval and regulatory data from dummy database
"""
import json
from typing import Optional, List, Dict


# Dummy Regulatory Database
REGULATORY_DB = {
    "NDA-207524": {
        "application_type": "NDA",
        "drug_name": "Cancer Drug XYZ",
        "application_number": "NDA-207524",
        "submission_date": "2020-06-15",
        "approval_date": "2021-03-22",
        "status": "Approved",
        "approval_type": "Accelerated Approval",
        "indication": "Treatment of advanced non-small cell lung cancer",
        "dosage": "100mg capsule, 200mg daily",
        "manufacturer": "PharmaCorp Inc",
        "adverse_events_reported": [
            "Nausea (15%)",
            "Fatigue (10%)",
            "Hair loss (20%)",
            "Neutropenia (Grade 3-4: 8%)"
        ],
        "black_box_warning": False,
        "rems_required": False,
        "post_marketing_commitment": "Phase 4 trial to study long-term efficacy"
    },
    "NDA-207892": {
        "application_type": "NDA",
        "drug_name": "DTZ-100",
        "application_number": "NDA-207892",
        "submission_date": "2019-11-20",
        "approval_date": "2020-09-14",
        "status": "Approved",
        "approval_type": "Standard Review",
        "indication": "Treatment of Type 2 Diabetes",
        "dosage": "100mg, 250mg, 500mg tablets - once daily",
        "manufacturer": "EndoPharm LLC",
        "adverse_events_reported": [
            "Nausea (8%)",
            "Headache (5%)",
            "Pancreatitis risk monitoring required"
        ],
        "black_box_warning": False,
        "rems_required": False,
        "post_marketing_commitment": "Monitor for pancreatitis in post-marketing surveillance"
    },
    "BLA-256789": {
        "application_type": "BLA",
        "drug_name": "IMT-50",
        "application_number": "BLA-256789",
        "submission_date": "2018-05-10",
        "approval_date": "2019-09-30",
        "status": "Approved",
        "approval_type": "Priority Review",
        "indication": "Treatment of advanced melanoma and non-small cell lung cancer",
        "dosage": "3mg/kg IV infusion, once every 2 weeks",
        "manufacturer": "ImmunoGen Corp",
        "adverse_events_reported": [
            "Cytokine release syndrome (Grade 1-2: 15%)",
            "Immune-related adverse events (irAEs)",
            "Hepatotoxicity (5%)",
            "Pneumonitis (3%)"
        ],
        "black_box_warning": True,
        "black_box_details": "Severe immune-mediated adverse reactions",
        "rems_required": True,
        "rems_details": "Risk Evaluation and Mitigation Strategy (REMS) program required",
        "post_marketing_commitment": "Close monitoring of immune-related adverse events"
    },
    "IND-142567": {
        "application_type": "IND",
        "drug_name": "DTZ-100 Extended Release",
        "application_number": "IND-142567",
        "submission_date": "2021-01-15",
        "approval_date": "2021-02-28",
        "status": "Active",
        "phase": "Phase 2",
        "indication": "Once-daily treatment of Type 2 Diabetes",
        "manufacturer": "EndoPharm LLC",
        "comments": "Parent NDA approved; extension study ongoing"
    }
}


def get_regulatory_data(query: str) -> Dict:
    """
    Retrieves regulatory data from dummy database
    
    Args:
        query: Search query (drug name, application number, or manufacturer)
        
    Returns:
        Dictionary with matching regulatory data
    """
    query_lower = query.lower()
    results = {}
    
    # Search by application number
    if query.startswith(("NDA", "BLA", "IND")):
        if query in REGULATORY_DB:
            return {"found": True, "applications": [REGULATORY_DB[query]]}
        else:
            return {"found": False, "message": f"Application {query} not found"}
    
    # Search by drug name or manufacturer
    for app_num, app_data in REGULATORY_DB.items():
        if (query_lower in app_data.get("drug_name", "").lower() or
            query_lower in app_data.get("manufacturer", "").lower() or
            query_lower in str(app_data).lower()):
            results[app_num] = app_data
    
    if results:
        return {"found": True, "applications": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No regulatory data found for '{query}'"}


def get_approved_drugs() -> Dict:
    """
    Get all FDA approved drugs from database
    
    Returns:
        Dictionary with approved applications
    """
    results = {}
    
    for app_num, app_data in REGULATORY_DB.items():
        if app_data.get("status") == "Approved":
            results[app_num] = app_data
    
    if results:
        return {"found": True, "applications": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": "No approved drugs found"}


def get_drugs_with_black_box_warning() -> Dict:
    """
    Get drugs with black box warnings
    
    Returns:
        Dictionary with drugs having black box warnings
    """
    results = {}
    
    for app_num, app_data in REGULATORY_DB.items():
        if app_data.get("black_box_warning", False):
            results[app_num] = app_data
    
    if results:
        return {"found": True, "applications": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": "No drugs with black box warnings found"}


def get_drugs_requiring_rems() -> Dict:
    """
    Get drugs requiring REMS program
    
    Returns:
        Dictionary with drugs requiring REMS
    """
    results = {}
    
    for app_num, app_data in REGULATORY_DB.items():
        if app_data.get("rems_required", False):
            results[app_num] = app_data
    
    if results:
        return {"found": True, "applications": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": "No drugs requiring REMS found"}


def format_regulatory_for_llm(app_data: Dict) -> str:
    """
    Format regulatory data for LLM processing
    
    Args:
        app_data: Regulatory application dictionary
        
    Returns:
        Formatted string representation
    """
    app_type = app_data.get("application_type", "N/A")
    
    formatted = f"""
REGULATORY APPLICATION DATA:
- Application Type: {app_type}
- Drug Name: {app_data.get('drug_name', 'N/A')}
- Application Number: {app_data.get('application_number', 'N/A')}
- Status: {app_data.get('status', 'N/A')}
- Submission Date: {app_data.get('submission_date', 'N/A')}
- Approval Date: {app_data.get('approval_date', 'N/A')}
"""
    
    if app_type in ["NDA", "BLA"]:
        formatted += f"""- Approval Type: {app_data.get('approval_type', 'N/A')}
- Indication: {app_data.get('indication', 'N/A')}
- Dosage: {app_data.get('dosage', 'N/A')}
- Manufacturer: {app_data.get('manufacturer', 'N/A')}
- Adverse Events: {'; '.join(app_data.get('adverse_events_reported', []))}
- Black Box Warning: {app_data.get('black_box_warning', False)}
"""
        if app_data.get("black_box_warning"):
            formatted += f"  Details: {app_data.get('black_box_details', 'N/A')}\n"
        
        formatted += f"""- REMS Required: {app_data.get('rems_required', False)}
"""
        if app_data.get("rems_required"):
            formatted += f"  Details: {app_data.get('rems_details', 'N/A')}\n"
    
    elif app_type == "IND":
        formatted += f"""- Phase: {app_data.get('phase', 'N/A')}
- Indication: {app_data.get('indication', 'N/A')}
- Manufacturer: {app_data.get('manufacturer', 'N/A')}
- Comments: {app_data.get('comments', 'N/A')}
"""
    
    return formatted
