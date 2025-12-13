"""
Patent Data Tool
Retrieves patent information from dummy database
"""
import json
from typing import Optional, List, Dict


# Dummy Patent Database
PATENTS_DB = {
    "US10234567": {
        "title": "Novel Cancer Drug Formulation XYZ",
        "patent_number": "US10234567",
        "filing_date": "2018-05-15",
        "grant_date": "2021-03-22",
        "expiration_date": "2038-05-15",
        "years_remaining": 13,
        "status": "Active",
        "assignee": "PharmaCorp Inc",
        "inventors": ["Dr. John Smith", "Dr. Sarah Johnson"],
        "claims_count": 25,
        "abstract": "A novel formulation of cancer-fighting compound with improved bioavailability",
        "key_claims": [
            "Crystalline form of compound A",
            "Dosage between 50-200mg",
            "Method of treatment for NSCLC"
        ],
        "citations": 45,
        "freedom_to_operate": "Clear"
    },
    "US10567890": {
        "title": "Diabetes Treatment Method DTZ-100",
        "patent_number": "US10567890",
        "filing_date": "2017-08-20",
        "grant_date": "2020-11-15",
        "expiration_date": "2037-08-20",
        "years_remaining": 12,
        "status": "Active",
        "assignee": "EndoPharm LLC",
        "inventors": ["Dr. Emily Davis"],
        "claims_count": 18,
        "abstract": "Method for treating Type 2 diabetes with DTZ-100 compound",
        "key_claims": [
            "DTZ-100 compound structure",
            "Oral dosage form",
            "Daily dosing 100-500mg"
        ],
        "citations": 32,
        "freedom_to_operate": "Clear"
    },
    "US9876543": {
        "title": "Immunotherapy Agent IMT-50",
        "patent_number": "US9876543",
        "filing_date": "2016-02-10",
        "grant_date": "2019-09-30",
        "expiration_date": "2036-02-10",
        "years_remaining": 11,
        "status": "Active",
        "assignee": "ImmunoGen Corp",
        "inventors": ["Dr. Michael Chen", "Dr. Lisa Wong"],
        "claims_count": 22,
        "abstract": "Monoclonal antibody-based immunotherapy for advanced cancers",
        "key_claims": [
            "IMT-50 antibody structure",
            "Intravenous administration",
            "Treatment of melanoma and lung cancer"
        ],
        "citations": 58,
        "freedom_to_operate": "Some patent landscape crowding"
    },
    "US11123456": {
        "title": "Extended Release Formulation of DTZ-100",
        "patent_number": "US11123456",
        "filing_date": "2019-03-12",
        "grant_date": "2022-01-18",
        "expiration_date": "2039-03-12",
        "years_remaining": 14,
        "status": "Active",
        "assignee": "EndoPharm LLC",
        "inventors": ["Dr. Emily Davis", "Dr. Robert Wilson"],
        "claims_count": 15,
        "abstract": "Extended-release formulation of DTZ-100 for once-daily dosing",
        "key_claims": [
            "Polymer-based extended release matrix",
            "Once-daily dosing capability",
            "Improved patient compliance"
        ],
        "citations": 12,
        "freedom_to_operate": "Clear"
    }
}


def get_patent_data(query: str) -> Dict:
    """
    Retrieves patent data from dummy database
    
    Args:
        query: Search query (patent number, drug name, or company)
        
    Returns:
        Dictionary with matching patent data
    """
    query_lower = query.lower()
    results = {}
    
    # Search by patent number
    if query.startswith("US"):
        if query in PATENTS_DB:
            return {"found": True, "patents": [PATENTS_DB[query]]}
        else:
            return {"found": False, "message": f"Patent {query} not found"}
    
    # Search by title, drug name, or assignee
    for patent_num, patent_data in PATENTS_DB.items():
        if (query_lower in patent_data.get("title", "").lower() or
            query_lower in patent_data.get("assignee", "").lower() or
            query_lower in str(patent_data).lower()):
            results[patent_num] = patent_data
    
    if results:
        return {"found": True, "patents": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No patents found for '{query}'"}


def get_all_patents() -> Dict:
    """
    Retrieves all patents from dummy database
    
    Returns:
        Dictionary with all patents
    """
    return {
        "found": True,
        "patents": list(PATENTS_DB.values()),
        "count": len(PATENTS_DB)
    }


def get_active_patents() -> Dict:
    """
    Get all active patents
    
    Returns:
        Dictionary with active patents
    """
    results = {}
    
    for patent_num, patent_data in PATENTS_DB.items():
        if patent_data.get("status") == "Active":
            results[patent_num] = patent_data
    
    if results:
        return {"found": True, "patents": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": "No active patents found"}


def get_patents_expiring_soon(years: int = 5) -> Dict:
    """
    Get patents expiring within specified years
    
    Args:
        years: Number of years to look ahead
        
    Returns:
        Dictionary with expiring patents
    """
    results = {}
    
    for patent_num, patent_data in PATENTS_DB.items():
        years_remaining = patent_data.get("years_remaining", 0)
        if 0 < years_remaining <= years:
            results[patent_num] = patent_data
    
    if results:
        return {"found": True, "patents": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No patents expiring within {years} years"}


def format_patent_for_llm(patent_data: Dict) -> str:
    """
    Format patent data for LLM processing
    
    Args:
        patent_data: Patent dictionary
        
    Returns:
        Formatted string representation
    """
    formatted = f"""
PATENT DATA:
- Title: {patent_data.get('title', 'N/A')}
- Patent Number: {patent_data.get('patent_number', 'N/A')}
- Status: {patent_data.get('status', 'N/A')}
- Filing Date: {patent_data.get('filing_date', 'N/A')}
- Grant Date: {patent_data.get('grant_date', 'N/A')}
- Expiration Date: {patent_data.get('expiration_date', 'N/A')}
- Years Remaining: {patent_data.get('years_remaining', 'N/A')}
- Assignee: {patent_data.get('assignee', 'N/A')}
- Inventors: {', '.join(patent_data.get('inventors', []))}
- Claims Count: {patent_data.get('claims_count', 'N/A')}
- Key Claims: {'; '.join(patent_data.get('key_claims', []))}
- Freedom to Operate: {patent_data.get('freedom_to_operate', 'N/A')}
- Abstract: {patent_data.get('abstract', 'N/A')}
"""
    return formatted
