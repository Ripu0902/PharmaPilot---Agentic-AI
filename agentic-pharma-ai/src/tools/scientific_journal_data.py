"""
Scientific Journal Data Tool
Retrieves published research and literature from dummy database
"""
import json
from typing import Optional, List, Dict


# Dummy Scientific Journal Database
JOURNAL_DB = {
    "10.1038/s41586-021-03570-6": {
        "title": "Novel cancer drug demonstrates superior efficacy in Phase 3 trial",
        "authors": ["Smith, J.", "Johnson, S.", "Williams, R."],
        "journal": "Nature Medicine",
        "publication_date": "2021-03-22",
        "doi": "10.1038/s41586-021-03570-6",
        "volume": "27",
        "issue": "3",
        "pages": "345-358",
        "impact_factor": 36.1,
        "citations": 245,
        "abstract": "A Phase 3 randomized controlled trial demonstrates that Drug XYZ provides superior overall survival compared to standard treatment in patients with advanced NSCLC",
        "study_design": "Randomized Controlled Trial",
        "sample_size": 500,
        "primary_endpoint": "Overall Survival",
        "results": "Median OS: 16.2 months vs 11.1 months (p<0.001)",
        "keywords": ["cancer", "drug efficacy", "clinical trial", "NSCLC"]
    },
    "10.1056/NEJMoa1906239": {
        "title": "DTZ-100: A novel DPP-4 inhibitor for Type 2 diabetes management",
        "authors": ["Davis, E.", "Chen, M.", "Wong, L."],
        "journal": "New England Journal of Medicine",
        "publication_date": "2020-09-14",
        "doi": "10.1056/NEJMoa1906239",
        "volume": "383",
        "issue": "11",
        "pages": "1011-1023",
        "impact_factor": 74.7,
        "citations": 189,
        "abstract": "DTZ-100, a novel DPP-4 inhibitor, showed significant HbA1c reduction and improved glycemic control in patients with Type 2 diabetes",
        "study_design": "Double-blind Placebo-controlled Trial",
        "sample_size": 300,
        "primary_endpoint": "HbA1c reduction",
        "results": "Mean HbA1c reduction: 1.8% vs 0.3% placebo (p<0.001)",
        "keywords": ["diabetes", "DPP-4 inhibitor", "HbA1c", "clinical trial"]
    },
    "10.1200/JCO.20.01651": {
        "title": "IMT-50 monoclonal antibody improves survival in advanced melanoma",
        "authors": ["Chen, M.", "Wong, L.", "Martinez, D."],
        "journal": "Journal of Clinical Oncology",
        "publication_date": "2019-09-30",
        "doi": "10.1200/JCO.20.01651",
        "volume": "38",
        "issue": "26",
        "pages": "2924-2936",
        "impact_factor": 32.5,
        "citations": 312,
        "abstract": "IMT-50, a novel monoclonal antibody, demonstrates significant improvement in overall survival in patients with advanced melanoma resistant to checkpoint inhibitors",
        "study_design": "Phase 3 Randomized Trial",
        "sample_size": 400,
        "primary_endpoint": "Overall Survival",
        "results": "Median OS: 24.5 months vs 15.8 months with standard therapy (p<0.001)",
        "keywords": ["immunotherapy", "melanoma", "monoclonal antibody", "survival"]
    },
    "10.1038/s41587-021-00879-5": {
        "title": "Extended-release formulation improves DTZ-100 compliance and tolerability",
        "authors": ["Davis, E.", "Wilson, R.", "Kumar, A."],
        "journal": "Nature Biotechnology",
        "publication_date": "2022-01-18",
        "doi": "10.1038/s41587-021-00879-5",
        "volume": "40",
        "issue": "1",
        "pages": "45-58",
        "impact_factor": 39.2,
        "citations": 67,
        "abstract": "An extended-release formulation of DTZ-100 achieves once-daily dosing while maintaining efficacy and improving patient compliance",
        "study_design": "Open-label Pharmacokinetic Study",
        "sample_size": 150,
        "primary_endpoint": "Plasma concentration over 24 hours",
        "results": "Sustained therapeutic levels for 24 hours with once-daily dosing",
        "keywords": ["DTZ-100", "extended-release", "pharmacokinetics", "compliance"]
    },
    "10.1016/S0140-6736(21)02115-8": {
        "title": "Long-term safety profile of cancer drug XYZ: 5-year follow-up data",
        "authors": ["Smith, J.", "Anderson, K.", "Lee, P."],
        "journal": "The Lancet",
        "publication_date": "2021-12-15",
        "doi": "10.1016/S0140-6736(21)02115-8",
        "volume": "399",
        "issue": "10321",
        "pages": "123-135",
        "impact_factor": 79.5,
        "citations": 156,
        "abstract": "Five-year follow-up data from the Phase 3 trial confirms the long-term safety and efficacy of Drug XYZ with manageable adverse events",
        "study_design": "Long-term Safety Follow-up",
        "sample_size": 450,
        "primary_endpoint": "Long-term safety and tolerability",
        "results": "No new safety signals identified; adverse event profile consistent with original trial",
        "keywords": ["cancer", "long-term safety", "follow-up", "efficacy"]
    }
}


def get_journal_data(query: str) -> Dict:
    """
    Retrieves scientific journal data from dummy database
    
    Args:
        query: Search query (DOI, title, author, or keyword)
        
    Returns:
        Dictionary with matching journal articles
    """
    query_lower = query.lower()
    results = {}
    
    # Search by DOI
    if query.startswith("10."):
        if query in JOURNAL_DB:
            return {"found": True, "articles": [JOURNAL_DB[query]]}
        else:
            return {"found": False, "message": f"DOI {query} not found"}
    
    # Search by title, author, journal, or keywords
    for doi, article in JOURNAL_DB.items():
        if (query_lower in article.get("title", "").lower() or
            query_lower in article.get("journal", "").lower() or
            any(query_lower in author.lower() for author in article.get("authors", [])) or
            any(query_lower in keyword.lower() for keyword in article.get("keywords", []))):
            results[doi] = article
    
    if results:
        return {"found": True, "articles": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No articles found for '{query}'"}


def get_all_articles() -> Dict:
    """
    Retrieves all journal articles from dummy database
    
    Returns:
        Dictionary with all articles
    """
    return {
        "found": True,
        "articles": list(JOURNAL_DB.values()),
        "count": len(JOURNAL_DB)
    }


def get_highly_cited_articles(min_citations: int = 100) -> Dict:
    """
    Get articles with high citation counts
    
    Args:
        min_citations: Minimum number of citations
        
    Returns:
        Dictionary with highly cited articles
    """
    results = {}
    
    for doi, article in JOURNAL_DB.items():
        if article.get("citations", 0) >= min_citations:
            results[doi] = article
    
    if results:
        return {"found": True, "articles": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No articles with {min_citations}+ citations found"}


def get_articles_by_journal(journal_name: str) -> Dict:
    """
    Get articles from specific journal
    
    Args:
        journal_name: Name of the journal
        
    Returns:
        Dictionary with articles from journal
    """
    journal_lower = journal_name.lower()
    results = {}
    
    for doi, article in JOURNAL_DB.items():
        if journal_lower in article.get("journal", "").lower():
            results[doi] = article
    
    if results:
        return {"found": True, "articles": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No articles found from {journal_name}"}


def get_articles_by_study_design(study_design: str) -> Dict:
    """
    Get articles by study design
    
    Args:
        study_design: Type of study (RCT, observational, etc.)
        
    Returns:
        Dictionary with articles of specified design
    """
    design_lower = study_design.lower()
    results = {}
    
    for doi, article in JOURNAL_DB.items():
        if design_lower in article.get("study_design", "").lower():
            results[doi] = article
    
    if results:
        return {"found": True, "articles": list(results.values()), "count": len(results)}
    else:
        return {"found": False, "message": f"No {study_design} studies found"}


def format_article_for_llm(article: Dict) -> str:
    """
    Format journal article for LLM processing
    
    Args:
        article: Article dictionary
        
    Returns:
        Formatted string representation
    """
    formatted = f"""
JOURNAL ARTICLE DATA:
- Title: {article.get('title', 'N/A')}
- Authors: {', '.join(article.get('authors', []))}
- Journal: {article.get('journal', 'N/A')}
- Publication Date: {article.get('publication_date', 'N/A')}
- DOI: {article.get('doi', 'N/A')}
- Volume/Issue/Pages: {article.get('volume', 'N/A')}/{article.get('issue', 'N/A')}/{article.get('pages', 'N/A')}
- Impact Factor: {article.get('impact_factor', 'N/A')}
- Citations: {article.get('citations', 'N/A')}
- Study Design: {article.get('study_design', 'N/A')}
- Sample Size: {article.get('sample_size', 'N/A')}
- Primary Endpoint: {article.get('primary_endpoint', 'N/A')}
- Results: {article.get('results', 'N/A')}
- Abstract: {article.get('abstract', 'N/A')}
- Keywords: {', '.join(article.get('keywords', []))}
"""
    return formatted
