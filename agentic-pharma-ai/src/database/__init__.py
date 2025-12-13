"""Mock Data Sources - Simulating Real Databases"""
import json
from typing import Dict, List
from datetime import datetime, timedelta
import random


class MockDataSources:
    """Mock data sources simulating real pharmaceutical databases with 5x expanded data"""

    # Comprehensive molecule database
    MOLECULES = {
        "Metformin": {"ta": "Diabetes", "brand": "Glucophage"},
        "Lisinopril": {"ta": "Cardiovascular", "brand": "Prinivil"},
        "Atorvastatin": {"ta": "Cardiovascular", "brand": "Lipitor"},
        "Omeprazole": {"ta": "Gastroenterology", "brand": "Prilosec"},
        "Amlodipine": {"ta": "Cardiovascular", "brand": "Norvasc"},
        "Sertraline": {"ta": "Psychiatry", "brand": "Zoloft"},
        "Albuterol": {"ta": "Respiratory", "brand": "Ventolin"},
        "Ibuprofen": {"ta": "Pain Management", "brand": "Advil"},
        "Levothyroxine": {"ta": "Endocrinology", "brand": "Synthroid"},
        "Losartan": {"ta": "Cardiovascular", "brand": "Cozaar"},
    }
    
    MANUFACTURERS = [
        "Pfizer", "Merck", "AstraZeneca", "Novartis", "Johnson & Johnson",
        "Roche", "Sanofi", "GlaxoSmithKline", "Eli Lilly", "Bristol Myers Squibb",
        "Amgen", "Gilead", "Abbvie", "Regeneron", "Moderna",
        "Allergan", "Teva", "Mylan", "Sandoz", "Hospira"
    ]
    
    SPONSORS = [
        "Academic Medical Center", "Innovative Therapeutics", "BigPharma Corp",
        "Clinical Research Institute", "University Hospital", "National Cancer Institute",
        "Veterans Affairs", "Mayo Clinic", "Stanford University", "Harvard Medical School",
        "Memorial Sloan Kettering", "Cleveland Clinic", "Johns Hopkins", "Dana-Farber"
    ]
    
    INDICATIONS = [
        "Type 2 Diabetes", "Hypertension", "Heart Failure", "Atrial Fibrillation",
        "Breast Cancer", "Colorectal Cancer", "Lung Cancer", "Melanoma",
        "Crohn's Disease", "Ulcerative Colitis", "Rheumatoid Arthritis", "Psoriasis",
        "COPD", "Asthma", "Pneumonia", "COVID-19"
    ]

    @staticmethod
    def search_iqvia(molecule: str) -> Dict:
        """Mock IQVIA market data - 5x expanded with multiple molecules and regions"""
        molecule_data = MockDataSources.MOLECULES.get(molecule, {"ta": "Multi-indication", "brand": molecule})
        
        # Generate base metrics
        base_revenue = random.uniform(300, 2500)
        cagr = random.uniform(3, 18)
        
        # Generate regional data
        regions = {
            "North America": {"percent": random.uniform(35, 55), "revenue_share": base_revenue * random.uniform(0.35, 0.55)},
            "Europe": {"percent": random.uniform(25, 40), "revenue_share": base_revenue * random.uniform(0.25, 0.40)},
            "Asia-Pacific": {"percent": random.uniform(10, 30), "revenue_share": base_revenue * random.uniform(0.10, 0.30)},
            "Latin America": {"percent": random.uniform(3, 10), "revenue_share": base_revenue * random.uniform(0.03, 0.10)},
            "Middle East & Africa": {"percent": random.uniform(2, 8), "revenue_share": base_revenue * random.uniform(0.02, 0.08)},
        }
        
        # Generate competitive landscape
        top_competitors = random.sample(MockDataSources.MANUFACTURERS, min(10, len(MockDataSources.MANUFACTURERS)))
        
        return {
            "molecule": molecule,
            "brand_name": molecule_data["brand"],
            "market_overview": {
                "tam_usd_million": round(base_revenue * (1 + cagr/100) ** 5, 2),
                "current_market_size_2024_usd_million": round(base_revenue, 2),
                "cagr_5yr_percent": round(cagr, 2),
                "market_trend": random.choice([
                    "Growing demand in emerging markets with 15% CAGR",
                    "Steady growth in developed markets with price compression",
                    "Rapid expansion in Asia-Pacific (20% YoY)",
                    "Consolidation in North America, growth in international",
                    "Strong uptake in novel indication expansion"
                ]),
                "therapeutic_area": molecule_data["ta"],
                "market_maturity": random.choice(["Growth", "Mature", "Decline", "Emerging"])
            },
            "competitive_landscape": {
                "total_competitors": random.randint(15, 45),
                "top_10_manufacturers": [
                    {
                        "rank": i+1,
                        "manufacturer": competitor,
                        "market_share_percent": round(random.uniform(2, 25) if i < 3 else random.uniform(1, 8), 2),
                        "revenue_2024_usd_million": round(base_revenue * random.uniform(0.02, 0.25), 2),
                        "yoy_growth_percent": round(random.uniform(-5, 20), 2)
                    }
                    for i, competitor in enumerate(top_competitors[:10])
                ],
                "hhi_index": round(random.uniform(800, 3500), 0),  # Market concentration indicator
                "competitive_intensity": "HIGH" if random.choice([True, False]) else "MODERATE"
            },
            "formulation_segmentation": {
                "oral": {
                    "revenue_usd_million": round(base_revenue * random.uniform(0.50, 0.70), 2),
                    "percent": round(random.uniform(50, 70), 1),
                    "volume_units": round(random.uniform(500000, 5000000), 0)
                },
                "injectable": {
                    "revenue_usd_million": round(base_revenue * random.uniform(0.15, 0.35), 2),
                    "percent": round(random.uniform(15, 35), 1),
                    "volume_units": round(random.uniform(100000, 800000), 0)
                },
                "topical": {
                    "revenue_usd_million": round(base_revenue * random.uniform(0.05, 0.20), 2),
                    "percent": round(random.uniform(5, 20), 1),
                    "volume_units": round(random.uniform(50000, 300000), 0)
                },
                "other": {
                    "revenue_usd_million": round(base_revenue * random.uniform(0.02, 0.10), 2),
                    "percent": round(random.uniform(2, 10), 1),
                    "volume_units": round(random.uniform(10000, 100000), 0)
                }
            },
            "regional_breakdown": {
                region: {
                    "revenue_usd_million": round(region_data["revenue_share"], 2),
                    "percent": round(region_data["percent"], 1),
                    "growth_rate_percent": round(random.uniform(-2, 22), 2),
                    "market_maturity": random.choice(["Mature", "Growth", "Emerging"])
                }
                for region, region_data in regions.items()
            },
            "historical_data": [
                {
                    "year": 2020 + i,
                    "revenue_usd_million": round(base_revenue * (1 + cagr/100) ** (i - 4), 2),
                    "volume_units": round(random.uniform(1000000, 10000000), 0),
                    "growth_percent": round(cagr, 2) if i > 0 else 0,
                    "market_share_top3_percent": round(random.uniform(35, 65), 1)
                }
                for i in range(5)
            ],
            "dosage_strength_breakdown": {
                f"Strength {j}": {
                    "revenue_usd_million": round(base_revenue * random.uniform(0.10, 0.30), 2),
                    "percent": round(random.uniform(10, 30), 1),
                    "volume_units": round(random.uniform(100000, 500000), 0)
                }
                for j in range(1, 5)
            },
            "_data_quality": {
                "yyd_flag": random.choice([True, False]),
                "currency_normalized": "USD (using average annual FX rates)",
                "name_matching": "Fuzzy matching applied",
                "data_completeness": f"{random.randint(85, 100)}%",
                "last_update": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "confidence_score": round(random.uniform(0.80, 0.99), 2)
            }
        }

    @staticmethod
    def search_exim(molecule: str) -> Dict:
        """Mock EXIM trade data - 5x expanded with multiple countries and quarters"""
        countries_exporters = ["China", "India", "USA", "Germany", "Japan", "Switzerland", "Belgium", "Ireland"]
        countries_importers = ["USA", "Germany", "France", "UK", "Japan", "Canada", "Australia", "Spain"]
        
        return {
            "molecule": molecule,
            "hs_code": f"{random.randint(2900, 3004)}.{random.randint(10, 90)}",
            "hs_code_status": random.choice(["Specific code available", "Basket code (includes similar molecules)", "Ambiguous - verify"]),
            "trade_summary": {
                "total_imports_kg": round(random.uniform(500000, 5000000), 0),
                "total_exports_kg": round(random.uniform(400000, 4500000), 0),
                "total_import_value_usd_million": round(random.uniform(5, 150), 2),
                "total_export_value_usd_million": round(random.uniform(4, 140), 2),
                "import_growth_yoy_percent": round(random.uniform(-15, 35), 2),
                "export_growth_yoy_percent": round(random.uniform(-10, 30), 2)
            },
            "top_exporters": [
                {
                    "rank": i + 1,
                    "country": exporter,
                    "export_volume_kg": round(random.uniform(100000, 1500000), 0),
                    "export_value_usd_million": round(random.uniform(1, 50), 2),
                    "unit_price_usd_per_kg": round(random.uniform(5, 100), 2),
                    "yoy_growth_percent": round(random.uniform(-10, 40), 2),
                    "market_share_percent": round(random.uniform(5, 25), 1)
                }
                for i, exporter in enumerate(random.sample(countries_exporters, min(8, len(countries_exporters))))
            ],
            "top_importers": [
                {
                    "rank": i + 1,
                    "country": importer,
                    "import_volume_kg": round(random.uniform(80000, 1200000), 0),
                    "import_value_usd_million": round(random.uniform(1, 45), 2),
                    "unit_price_usd_per_kg": round(random.uniform(5, 100), 2),
                    "yoy_growth_percent": round(random.uniform(-12, 35), 2),
                    "market_share_percent": round(random.uniform(5, 20), 1)
                }
                for i, importer in enumerate(random.sample(countries_importers, min(8, len(countries_importers))))
            ],
            "quarterly_trends": [
                {
                    "quarter": f"Q{q} 2024",
                    "import_volume_kg": round(random.uniform(100000, 1200000), 0),
                    "export_volume_kg": round(random.uniform(80000, 1100000), 0),
                    "avg_import_price_usd_kg": round(random.uniform(10, 90), 2),
                    "avg_export_price_usd_kg": round(random.uniform(12, 95), 2)
                }
                for q in range(1, 5)
            ],
            "volume_vs_value_analysis": {
                "price_erosion_detected": random.choice([True, False]),
                "price_erosion_percent": round(random.uniform(-15, 5), 2),
                "premium_pricing_regions": random.sample(["Japan", "USA", "Switzerland", "Germany"], random.randint(1, 3)),
                "commodity_pricing_regions": random.sample(["India", "China", "Vietnam", "Thailand"], random.randint(1, 3)),
                "price_elasticity": round(random.uniform(0.5, 2.5), 2)
            },
            "trend_detection": {
                "recent_spikes_detected": random.choice([True, False]),
                "q3_2024_import_spike_percent": round(random.uniform(-10, 45), 2),
                "likely_driver": random.choice(["New product launch", "Supply diversification", "Stockpiling", "Market expansion"]),
                "supply_chain_disruption_risk": random.choice(["LOW", "MEDIUM", "HIGH"])
            },
            "supplier_analysis": {
                "concentration_ratio_top3": round(random.uniform(30, 75), 1),
                "supplier_diversification": random.choice(["Low risk", "Moderate risk", "High concentration"]),
                "new_suppliers_emerging": random.randint(0, 5),
                "supplier_reliability_score": round(random.uniform(0.6, 0.95), 2)
            },
            "unit_standardization": "All data standardized to kg (conversions: g/kg=1, mt=1000)",
            "_anomalies": {
                "outlier_transactions_flagged": random.choice([True, False]),
                "outliers_definition": "Unit price >2 std dev from mean",
                "suspicious_shipments": random.randint(0, 5),
                "sample_shipments_detected": random.choice([True, False]),
                "rd_shipment_volumes": round(random.uniform(0, 50000), 0)
            },
            "_data_quality": {
                "completeness": f"{random.randint(80, 100)}%",
                "timeliness": "Updated monthly",
                "accuracy_score": round(random.uniform(0.85, 0.99), 2)
            }
        }

    @staticmethod
    def search_patents(molecule: str) -> Dict:
        """Mock patent database - 5x expanded with multiple jurisdictions"""
        expiry_years = [2026, 2027, 2028, 2029, 2030, 2031]
        patent_types = ["Composition of Matter", "Process Patent", "Formulation Patent", "Use Patent", "Method Patent"]
        jurisdictions_list = ["US", "EU", "JP", "CA", "AU", "IN", "CH"]
        
        return {
            "molecule": molecule,
            "total_patent_families": random.randint(5, 25),
            "patents": [
                {
                    "patent_id": f"{jur}{10000000 + i}",
                    "jurisdiction": jur,
                    "title": random.choice([
                        f"{molecule} for novel indication",
                        f"Process patent for {molecule} synthesis",
                        f"Extended release formulation of {molecule}",
                        f"Salt forms of {molecule}",
                        f"Combination therapy with {molecule}"
                    ]),
                    "patent_type": random.choice(patent_types),
                    "filing_date": (datetime.now() - timedelta(days=365*random.randint(8, 20))).strftime("%Y-%m-%d"),
                    "grant_date": (datetime.now() - timedelta(days=365*random.randint(5, 15))).strftime("%Y-%m-%d"),
                    "expiry_date": f"{random.choice(expiry_years)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                    "status": random.choice(["Active", "Pending", "Expired", "Abandoned"]),
                    "assignee": random.choice(MockDataSources.MANUFACTURERS),
                    "strength_ranking": "HIGH" if i == 0 else "MEDIUM" if i == 1 else "LOW",
                    "_risk_flag": "🔴 HIGH RISK" if i == 0 and random.choice([True, False]) else "🟡 MEDIUM RISK" if i < 3 else "🟢 LOW RISK",
                    "_fto_impact": "Blocks generic entry" if i == 0 else "Limited impact (process/formulation)" if i < 3 else "No impact (expired/expiring)",
                    "litigation_status": random.choice(["None", "Pending", "Paragraph IV challenge", "Appeal"]),
                    "legal_fees_status": random.choice(["Paid", "Current", "Lapsed"])
                }
                for jur in random.sample(jurisdictions_list, random.randint(3, 5))
                for i in range(random.randint(2, 5))
            ],
            "litigation_status": {
                "active_cases": random.randint(0, 5),
                "orange_book_certs": random.randint(0, 3),
                "paragraph_iv_challenges": random.randint(0, 2),
                "recent_litigation": random.choice([
                    "Merck v. Generics Inc. (Pending)",
                    "None",
                    "First Generics v. BigPharma (Appeal)",
                    "Settlement reached Q3 2024"
                ]),
                "settlements": random.randint(0, 2)
            },
            "loss_of_exclusivity_analysis": {
                "primary_patent_expiry": f"{random.choice(expiry_years)}-{random.randint(1,12):02d}-15",
                "secondary_patents_count": random.randint(0, 5),
                "evergreening_strategy": "Detected" if random.choice([True, False]) else "Not detected",
                "spc_extension_possible": random.choice([True, False]),
                "spc_expiry": f"{random.choice(expiry_years) + 5}-{random.randint(1,12):02d}-15" if random.choice([True, False]) else "N/A",
                "pte_extension_us": random.randint(0, 5),
                "estimated_generic_entry": f"Q{random.randint(1,4)} {random.choice(expiry_years) + 1}",
                "expected_price_erosion_percent": round(random.uniform(30, 80), 1)
            },
            "jurisdiction_summary": {
                "us": {
                    "status": random.choice(["🔴 HIGH RISK", "🟡 MEDIUM RISK", "🟢 LOW RISK"]),
                    "primary_patents": random.randint(1, 5),
                    "expiry_date": f"{random.choice(expiry_years)}-06-15"
                },
                "eu": {
                    "status": random.choice(["🔴 HIGH RISK", "🟡 MEDIUM RISK", "🟢 LOW RISK"]),
                    "primary_patents": random.randint(1, 4),
                    "spc_available": random.choice([True, False])
                },
                "japan": {
                    "status": random.choice(["🔴 HIGH RISK", "🟡 MEDIUM RISK", "🟢 LOW RISK"]),
                    "primary_patents": random.randint(0, 3),
                    "expiry_date": f"{random.choice(expiry_years)}-03-20"
                },
                "rest_of_world": {
                    "coverage": f"{random.randint(20, 80)}% of markets",
                    "status": "Mixed protection"
                }
            },
            "_metadata": {
                "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                "data_source": "USPTO + Orange Book + WIPO + EPO",
                "confidence_score": round(random.uniform(0.85, 0.99), 2),
                "last_update": (datetime.now() - timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d"),
                "recommendations": [
                    "Monitor upcoming Paragraph IV challenges",
                    "Prepare lifecycle management strategy",
                    "Consider authorized generics or co-promotion",
                    "Evaluate patent extension strategies"
                ]
            }
        }

    @staticmethod
    def search_clinical_trials(molecule: str) -> Dict:
        """Mock ClinicalTrials.gov data - 5x expanded with detailed trial info"""
        phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
        statuses = ["Recruiting", "Active, not recruiting", "Completed", "Terminated", "Withdrawn"]
        
        trials_by_indication = {}
        
        for indication in random.sample(MockDataSources.INDICATIONS, random.randint(3, 6)):
            trials_by_indication[indication] = [
                {
                    "nct_id": f"NCT{random.randint(10000000, 99999999)}",
                    "title": f"{molecule} in {indication}",
                    "phase": random.choice(phases),
                    "status": random.choice(statuses),
                    "sponsor": random.choice(MockDataSources.SPONSORS),
                    "enrollment": random.randint(50, 1500),
                    "target_enrollment": random.randint(100, 2000),
                    "actual_enrollment": random.randint(40, 1500),
                    "enrollment_status": random.choice(["On track", "Ahead of schedule", "Behind schedule"]),
                    "start_date": (datetime.now() - timedelta(days=365*random.randint(1, 4))).strftime("%Y-%m-%d"),
                    "primary_endpoints": random.sample(
                        ["Overall Survival (OS)", "Progression-Free Survival (PFS)", "Safety/Tolerability", 
                         "Quality of Life", "Biomarkers", "Efficacy", "Pharmacokinetics"],
                        random.randint(1, 3)
                    ),
                    "secondary_endpoints": random.sample(
                        ["Biomarkers", "Quality of Life", "Pharmacodynamics", "Economic outcomes"],
                        random.randint(1, 2)
                    ),
                    "inclusion_criteria": random.choice([
                        "Age 18-75, confirmed diagnosis",
                        "Stage III-IV disease",
                        "ECOG PS 0-2",
                        "Adequate organ function"
                    ]),
                    "exclusion_criteria": "Prior therapy, active infection, pregnancy",
                    "estimated_completion": (datetime.now() + timedelta(days=365*random.randint(1, 4))).strftime("%Y-%m-%d"),
                    "estimated_completion_date_actual": (datetime.now() + timedelta(days=365*random.randint(1, 4))).strftime("%Y-%m-%d"),
                    "results_posted": random.choice([True, False]),
                    "termination_reason": random.choice(["N/A", "Efficacy", "Futility", "Safety"]) if random.choice([True, False]) else "N/A",
                    "_mesh_synonyms": {
                        "Breast Cancer": ["Breast Carcinoma", "Breast Neoplasm", "Mammary Cancer"],
                        "Diabetes": ["Diabetes Mellitus", "Glycemic Control"],
                        "Heart Failure": ["Cardiac Failure", "Congestive Heart Failure"],
                    },
                    "_trial_classification": random.choice(["Early Stage", "Late Stage", "Phase 4", "Observational"]),
                    "_competitive_threat": "HIGH" if random.choice([True, False]) else "MODERATE",
                }
                for _ in range(random.randint(2, 4))
            ]
        
        return {
            "molecule": molecule,
            "total_active_trials": sum(len(v) for v in trials_by_indication.values()),
            "total_recruiting_trials": random.randint(3, 15),
            "trials_by_indication": trials_by_indication,
            "pipeline_summary": {
                "phase_1_count": random.randint(1, 5),
                "phase_2_count": random.randint(2, 8),
                "phase_3_count": random.randint(1, 6),
                "phase_4_count": random.randint(0, 4),
                "total_patients_enrolled": random.randint(500, 5000),
                "total_estimated_patients": random.randint(1000, 10000)
            },
            "sponsor_analysis": {
                "industry_sponsored": random.randint(2, 8),
                "academic_sponsored": random.randint(1, 5),
                "government_sponsored": random.randint(0, 3),
                "top_sponsor": random.choice(MockDataSources.SPONSORS)
            },
            "timeline_analysis": {
                "avg_phase_duration": f"{random.randint(18, 48)} months",
                "estimated_approval_date": (datetime.now() + timedelta(days=365*random.randint(2, 5))).strftime("%Y-%m-%d"),
                "key_milestones": [
                    f"Phase 3 readout: Q{random.randint(1, 4)} {random.randint(2024, 2027)}",
                    f"NDA submission: Q{random.randint(1, 4)} {random.randint(2025, 2028)}",
                    f"Potential approval: Q{random.randint(1, 4)} {random.randint(2026, 2029)}"
                ]
            },
            "_metadata": {
                "filters_applied": "Recruiting + Active, not recruiting",
                "endpoint_extraction": "Enabled",
                "mesh_mapping": "Disease synonyms mapped",
                "status_clarity": "Terminated/Withdrawn distinguished",
                "timeline_estimation": "Enabled",
                "data_source": "ClinicalTrials.gov",
                "last_update": (datetime.now() - timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d")
            }
        }

    @staticmethod
    def search_internal_docs(query: str) -> Dict:
        """Mock internal knowledge base - 5x expanded with multiple documents"""
        doc_types = ["Strategic Plan", "Portfolio Review", "KOL Interview Notes", "Competitive Analysis", 
                     "Field Feedback Report", "Market Assessment", "R&D Pipeline Review", "Budget Allocation"]
        
        return {
            "query": query,
            "total_documents_searched": random.randint(50, 200),
            "documents_found": random.randint(3, 10),
            "relevant_documents": [
                {
                    "filename": f"{random.choice(doc_types)} {random.randint(2020, 2024)}.pdf",
                    "page": random.randint(1, 100),
                    "relevance_score": round(random.uniform(0.65, 1.0), 2),
                    "document_type": random.choice(doc_types),
                    "date": (datetime.now() - timedelta(days=365*random.randint(0, 2))).strftime("%Y-%m-%d"),
                    "excerpt": f"Document discusses {query} with relevance to market strategy",
                    "sentiment": random.choice(["Positive", "Neutral", "Negative"]),
                    "key_topics": random.sample(["Market Opportunity", "Competitive Risk", "R&D Investment", "Commercial Viability"], 2)
                }
                for _ in range(random.randint(3, 7))
            ],
            "key_insights": [
                {
                    "insight": f"Company {random.choice(['has strong presence', 'is gaining traction', 'faces competition'])} in {query} space",
                    "source": f"Strategic Plan 2024-2026.pdf, Page {random.randint(1, 50)}",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "confidence": random.choice(["High", "Medium", "Low"]),
                    "strategic_relevance": random.choice(["High", "Medium", "Low"])
                },
                {
                    "insight": "Physicians interested in once-daily formulations and improved safety profiles",
                    "source": f"KOL Interview Notes Q3 2024.pdf, Page {random.randint(1, 30)}",
                    "date": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                    "confidence": "High",
                    "strategic_relevance": "High"
                },
                {
                    "insight": "Emerging market growing 25% YoY with pricing flexibility opportunity",
                    "source": f"Market Assessment 2024.pdf, Page {random.randint(1, 40)}",
                    "date": (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d"),
                    "confidence": "High",
                    "strategic_relevance": "Medium"
                }
            ],
            "field_feedback": [
                "Market preference for oral formulations in primary care",
                "Safety profile is key differentiator vs competitors",
                "Pricing sensitivity in emerging markets (30-40% premium tolerance)",
                f"Strong interest in {query} from key opinion leaders",
                "Combination therapy opportunities identified",
                "Unmet need in resistant/refractory cases"
            ],
            "strategic_alignment": {
                "portfolio_fit": random.choice(["Excellent", "Good", "Fair", "Poor"]),
                "capability_gap": random.choice(["Minimal", "Moderate", "Significant"]),
                "investment_priority": random.choice(["High", "Medium", "Low"]),
                "competitive_position": random.choice(["Leader", "Challenger", "Niche", "Emerging"])
            },
            "conflicting_perspectives": [
                {
                    "perspective_a": "Market growing rapidly",
                    "perspective_b": "Market growth slowing",
                    "document_a": "2024 Analysis",
                    "document_b": "2023 Forecast",
                    "resolution": "Growth moderating but still healthy 8-12% CAGR"
                }
            ] if random.choice([True, False]) else [],
            "_metadata": {
                "search_type": "Full-text semantic search",
                "ocr_processing": "Enabled",
                "citation_format": "Source: [Filename, Page #]",
                "search_completeness": f"{random.randint(85, 100)}%",
                "hallucination_guard": "Strict",
                "access_level": "Confidential - Internal Use Only",
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
        }

    @staticmethod
    def web_search(query: str) -> Dict:
        """Mock web search - 5x expanded with varied sources and recent data"""
        trusted_sources = [
            ("FDA.gov", 10, "Regulatory approval"),
            ("EMA.europa.eu", 10, "European regulatory update"),
            ("Nature Medicine", 9, "Clinical research study"),
            ("The Lancet", 9, "Peer-reviewed publication"),
            ("American Heart Association", 8, "Clinical guidelines"),
            ("NIH.gov", 9, "Government research"),
            ("JAMA", 9, "Medical journal article"),
            ("New England Journal of Medicine", 9, "Clinical trial results"),
            ("WHO Guidelines", 10, "International guidelines"),
            ("Reuters Health", 7, "Health news"),
        ]
        
        # Generate multiple results from varied sources
        selected_sources = random.sample(trusted_sources, min(random.randint(4, 7), len(trusted_sources)))
        results = []
        
        for idx, (source, credibility, topic) in enumerate(selected_sources):
            results.append({
                "rank": idx + 1,
                "title": f"Latest developments in {query}: {topic}",
                "source": source,
                "url": f"https://{source.lower().replace(' ', '-')}/articles/{query.replace(' ', '-')}-{idx}",
                "publication_date": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d"),
                "article_date": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d"),
                "summary": f"Comprehensive article on {query} discussing latest advances and clinical implications",
                "_credibility_score": credibility,
                "_source_type": "HIGH-CREDIBILITY" if credibility >= 8 else "VERIFY",
                "content_type": random.choice(["Research Study", "Guidelines", "News", "Opinion", "Meta-Analysis"]),
                "snippet": f"Recent study shows {random.choice(['promising results', 'safety concerns', 'efficacy data'])} for {query}",
                "access_status": random.choice(["Open Access", "Paywalled", "Free Summary Available"]),
                "open_access_link": f"https://pubmedcentral.nih.gov/articles/{random.randint(1000000, 9999999)}" if random.choice([True, False]) else None
            })
        
        return {
            "query": query,
            "total_results": random.randint(100, 5000),
            "results_shown": len(results),
            "results": results,
            "guidelines": {
                "guidelines_found": random.randint(2, 5),
                "first_line_treatment": f"Current {random.choice(['FDA', 'EMA', 'WHO'])} guidelines recommend {query} for {random.choice(MockDataSources.INDICATIONS)}",
                "second_line_alternatives": f"Alternative treatments: {', '.join(random.sample(['Drug A', 'Drug B', 'Drug C', 'Combination therapy'], 2))}",
                "guideline_source": random.choice(["FDA", "EMA", "WHO", "NICE", "ASCO"]),
                "guideline_year": 2024,
                "date_verified": datetime.now().strftime("%Y-%m-%d"),
                "guideline_updates": f"Updated {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])} 2024"
            },
            "recent_news": [
                {
                    "headline": f"FDA approves new indication for {query}",
                    "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
                    "category": "Regulatory Approval",
                    "impact": "High",
                    "url": f"https://fda.gov/news/{random.randint(100000, 999999)}"
                },
                {
                    "headline": f"Major acquisition in {query} space",
                    "date": (datetime.now() - timedelta(days=random.randint(1, 120))).strftime("%Y-%m-%d"),
                    "category": "M&A",
                    "impact": "Medium",
                    "url": f"https://reuters.com/health/{random.randint(100000, 999999)}"
                },
                {
                    "headline": f"Safety alert issued for {query}",
                    "date": (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d"),
                    "category": "Safety Alert",
                    "impact": "Critical" if random.choice([True, False]) else "Moderate",
                    "url": f"https://fda.gov/safety/{random.randint(100000, 999999)}"
                }
            ],
            "emerging_trends": [
                f"Increased focus on {random.choice(['personalized medicine', 'combination therapies', 'rare indications'])}",
                f"Growing interest in {random.choice(['digital health integration', 'patient monitoring', 'real-world evidence'])}",
                f"Shift toward {random.choice(['home-based treatment', 'long-acting formulations', 'fixed-dose combinations'])}"
            ],
            "competitive_intelligence": {
                "competitor_approvals": random.randint(0, 3),
                "pipeline_updates": random.randint(1, 5),
                "market_share_shifts": random.choice(["No significant changes", "New entrant gaining traction", "Leader consolidating position"])
            },
            "_metadata": {
                "source_filter": "Whitelisted (FDA, EMA, NIH, journals)",
                "social_media_excluded": True,
                "paywall_detection": "Open-access prioritized",
                "date_verification": f"Latest guideline verified as of {datetime.now().strftime('%Y-%m-%d')}",
                "freshness": "Results from last 180 days",
                "search_completeness": f"{random.randint(90, 100)}%",
                "credibility_assessment": "Multiple high-credibility sources included",
                "last_update": datetime.now().strftime("%Y-%m-%d")
            }
        }

        """Mock IQVIA market data with TAM, CAGR, and segmentation"""
        base_year_revenue = random.uniform(300, 800)
        cagr = random.uniform(5, 15)
        
        return {
            "molecule": molecule,
            "market_overview": {
                "tam_usd_million": round(base_year_revenue * (1 + cagr/100) ** 5, 2),
                "current_market_size_2024_usd_million": round(base_year_revenue, 2),
                "cagr_5yr_percent": round(cagr, 2),
                "market_trend": random.choice([
                    "Growing demand in emerging markets",
                    "Steady growth in developed markets",
                    "Rapid expansion in Asia-Pacific"
                ]),
                "therapeutic_area": random.choice(["Cardiovascular", "Diabetes", "Oncology", "Immunology"])
            },
            "competitive_landscape": {
                "top_10_manufacturers": [
                    {"rank": i+1, "manufacturer": f"{random.choice(['Pfizer', 'Novartis', 'AstraZeneca', 'Merck', 'Johnson & Johnson'])}", 
                     "market_share_percent": round(random.uniform(3, 20), 2)}
                    for i in range(10)
                ]
            },
            "formulation_segmentation": {
                "oral": {"revenue_usd_million": round(base_year_revenue * 0.6, 2), "percent": 60},
                "injectable": {"revenue_usd_million": round(base_year_revenue * 0.3, 2), "percent": 30},
                "topical": {"revenue_usd_million": round(base_year_revenue * 0.1, 2), "percent": 10}
            },
            "historical_data": [
                {
                    "year": 2020 + i,
                    "revenue_usd_million": round(base_year_revenue * (1 + cagr/100) ** (i - 4), 2),
                    "growth_percent": round(cagr, 2) if i > 0 else 0
                }
                for i in range(5)
            ],
            "_data_quality": {
                "yyd_flag": False,
                "currency_normalized": "USD (using average annual FX rates)",
                "name_matching": "Fuzzy matching applied (e.g., Acetaminophen ≈ Paracetamol)",
                "data_completeness": "100% (specific molecule data available)"
            }
        }

    @staticmethod
    def search_exim(molecule: str) -> Dict:
        """Mock EXIM trade data with volume, value, and supply chain analysis"""
        return {
            "molecule": molecule,
            "trade_summary": {
                "total_imports_kg": round(random.uniform(500000, 2000000), 0),
                "total_exports_kg": round(random.uniform(400000, 1500000), 0),
                "total_import_value_usd_million": round(random.uniform(5, 50), 2),
                "total_export_value_usd_million": round(random.uniform(4, 40), 2)
            },
            "top_exporters": [
                {
                    "country": exporter,
                    "export_volume_kg": round(random.uniform(100000, 500000), 0),
                    "export_value_usd_million": round(random.uniform(1, 15), 2),
                    "unit_price_usd_per_kg": round(random.uniform(10, 100), 2)
                }
                for exporter in ["China", "India", "USA", "Germany", "Japan"]
            ],
            "top_importers": [
                {
                    "country": importer,
                    "import_volume_kg": round(random.uniform(80000, 400000), 0),
                    "import_value_usd_million": round(random.uniform(1, 12), 2),
                    "unit_price_usd_per_kg": round(random.uniform(10, 100), 2)
                }
                for importer in ["USA", "Germany", "France", "UK", "Japan"]
            ],
            "volume_vs_value_analysis": {
                "note": "Price erosion detected in generic segments",
                "premium_pricing_zones": ["Japan", "USA"],
                "commodity_pricing_zones": ["India", "China"]
            },
            "trend_detection": {
                "q3_import_spike_percent": round(random.uniform(-5, 25), 2),
                "insight": "Sudden spikes indicate potential launches or supply diversification",
                "yoy_comparison": "QoQ growth analysis available"
            },
            "unit_conversion_status": "All data standardized to kg",
            "_anomalies": {
                "outlier_transactions_flagged": True,
                "outliers_definition": "Unit price >2 std dev from mean (potential samples/R&D)",
                "hs_code_note": "If basket code used, results may include similar molecules"
            }
        }

    @staticmethod
    def search_patents(molecule: str) -> Dict:
        """Mock patent database with FTO analysis and expiry timelines"""
        expiry_years = [2026, 2027, 2028, 2029, 2030]
        
        return {
            "molecule": molecule,
            "patents": [
                {
                    "patent_id": f"US{10000000 + i}",
                    "title": f"{molecule} for novel indication" if i == 0 else f"Process patent for {molecule} synthesis",
                    "patent_type": "Composition of Matter" if i == 0 else "Process Patent",
                    "jurisdiction": "US",
                    "filing_date": (datetime.now() - timedelta(days=365*15)).strftime("%Y-%m-%d"),
                    "grant_date": (datetime.now() - timedelta(days=365*12)).strftime("%Y-%m-%d"),
                    "expiry_date": f"{random.choice(expiry_years)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                    "status": "Active",
                    "assignee": random.choice(["BigPharma Corp", "Generic Pharma Inc", "Innovation Labs"]),
                    "_risk_flag": "🔴 HIGH RISK" if i == 0 else "🟡 MEDIUM RISK",
                    "_fto_impact": "Blocks generic entry" if i == 0 else "Limited impact (process patent)"
                }
                for i in range(3)
            ],
            "litigation_status": {
                "active_cases": 0,
                "orange_book_certs": 0,
                "paragraph_iv_challenges": 0,
                "recent_litigation": "None"
            },
            "loss_of_exclusivity_analysis": {
                "primary_patent_expiry": f"{random.choice(expiry_years)}-06-15",
                "secondary_patents_detected": 1,
                "evergreening_strategy": "Secondary patents filed 5-7 years post-primary",
                "estimated_generic_entry": f"{random.choice(expiry_years) + 1}"
            },
            "jurisdiction_summary": {
                "us_status": "🔴 HIGH RISK - Active CoM patent",
                "eu_status": "🟡 MEDIUM RISK - SPC may extend protection",
                "japan_status": "🟢 LOW RISK - Patents expiring soon",
                "rest_of_world": "Grouped - variable protection"
            },
            "_metadata": {
                "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                "data_source": "USPTO + Orange Book + Legal dockets",
                "recommendations": [
                    "Monitor Paragraph IV challenges",
                    "Plan for generic entry strategy",
                    "Evaluate lifecycle management opportunities"
                ]
            }
        }

    @staticmethod
    def search_clinical_trials(molecule: str) -> Dict:
        """Mock ClinicalTrials.gov data with MeSH mapping and indication grouping"""
        indications = ["Heart Failure", "Diabetes Prevention", "Oncology", "Respiratory Disease"]
        phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
        
        trials_by_indication = {}
        
        for indication in indications:
            trials_by_indication[indication] = [
                {
                    "nct_id": f"NCT{random.randint(10000000, 99999999)}",
                    "title": f"{molecule} in {indication}",
                    "phase": random.choice(phases),
                    "status": random.choice(["Recruiting", "Active, not recruiting", "Completed"]),
                    "sponsor": random.choice(["Academic Medical Center", "Innovative Therapeutics", "BigPharma Corp"]),
                    "enrollment": random.randint(100, 1000),
                    "target_enrollment": random.randint(100, 1000),
                    "start_date": (datetime.now() - timedelta(days=365*2)).strftime("%Y-%m-%d"),
                    "primary_endpoints": ["Overall Survival (OS)", "Progression-Free Survival (PFS)", "Safety/Tolerability"],
                    "secondary_endpoints": [random.choice(["Quality of Life", "Biomarkers", "Pharmacokinetics"])],
                    "estimated_completion": (datetime.now() + timedelta(days=365*2)).strftime("%Y-%m-%d"),
                    "_mesh_synonyms": {
                        "Heart Failure": ["Heart Decompensation", "Cardiac Failure"],
                        "Diabetes": ["Diabetes Mellitus", "Glycemic Control"],
                        "Oncology": ["Neoplasm", "Malignancy", "Cancer"]
                    },
                    "_trial_classification": "Active Pipeline" if random.choice(phases) in ["Phase 2", "Phase 3"] else "Advanced Stage"
                }
                for _ in range(2)
            ]
        
        return {
            "molecule": molecule,
            "total_active_trials": sum(len(v) for v in trials_by_indication.values()),
            "trials_by_indication": trials_by_indication,
            "pipeline_summary": {
                "phase_1_count": random.randint(1, 3),
                "phase_2_count": random.randint(2, 5),
                "phase_3_count": random.randint(1, 4),
                "phase_4_count": random.randint(0, 2)
            },
            "_metadata": {
                "filters_applied": "Recruiting + Active, not recruiting",
                "endpoint_extraction": "Primary and secondary endpoints extracted",
                "mesh_mapping": "Disease synonyms mapped (e.g., Breast Cancer → Carcinoma)",
                "status_clarity": "Terminated/Withdrawn distinguished from Completed",
                "timeline_estimation": "Enabled based on phase and enrollment"
            }
        }

    @staticmethod
    def search_internal_docs(query: str) -> Dict:
        """Mock internal knowledge base with RAG capabilities"""
        return {
            "query": query,
            "relevant_documents": [
                {
                    "filename": "Strategic Plan 2024-2026.pdf",
                    "page": random.randint(1, 50),
                    "relevance_score": round(random.uniform(0.7, 1.0), 2),
                    "excerpt": f"Company strategy emphasizes {query} opportunities"
                },
                {
                    "filename": "Cardiovascular Portfolio Review.pdf",
                    "page": random.randint(1, 30),
                    "relevance_score": round(random.uniform(0.6, 0.9), 2),
                    "excerpt": f"Portfolio assessment includes {query} potential"
                }
            ],
            "key_insights": [
                {
                    "insight": f"Company has strong presence in {query} space",
                    "source": "Strategic Plan 2024-2026.pdf, Page 12",
                    "date": "2024",
                    "confidence": "High"
                },
                {
                    "insight": "Physicians interested in once-daily formulations",
                    "source": "KOL Interview Notes Q3 2024.pdf, Page 5",
                    "date": "2024",
                    "confidence": "High"
                }
            ],
            "field_feedback": [
                "Market preference for oral formulations",
                "Safety profile is key differentiator",
                "Pricing sensitivity in emerging markets"
            ],
            "_metadata": {
                "ocr_processing": "Enabled for scanned PDFs",
                "citation_format": "Source: [Filename, Page #]",
                "conflicting_info": "None detected",
                "search_completeness": "100%",
                "hallucination_guard": "Strict - only known info returned"
            }
        }

    @staticmethod
    def web_search(query: str) -> Dict:
        """Mock web search with credibility scoring and source filtering"""
        trusted_sources = [
            ("FDA.gov", 10, "FDA approval"),
            ("EMA.europa.eu", 10, "European regulatory news"),
            ("Nature Medicine", 9, "Clinical research"),
            ("The Lancet", 9, "Peer-reviewed study"),
            ("American Heart Association", 8, "Clinical guidelines"),
            ("NIH.gov", 9, "Government research")
        ]
        
        results = []
        for source, credibility, topic in random.sample(trusted_sources, min(3, len(trusted_sources))):
            results.append({
                "title": f"Recent developments in {query}: {topic}",
                "source": source,
                "url": f"https://{source.lower()}/articles/{query.replace(' ', '-')}",
                "publication_date": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d"),
                "summary": f"Latest research and regulatory updates on {query}",
                "_credibility_score": credibility,
                "_source_type": "HIGH-CREDIBILITY" if credibility >= 8 else "VERIFY",
                "snippet": f"Study shows promising results for {query} in clinical use"
            })
        
        return {
            "query": query,
            "results": results,
            "guidelines": {
                "first_line_treatment": f"Current guidelines recommend {query} as first-line therapy",
                "second_line_alternatives": "Alternative treatments available for resistant cases",
                "guideline_source": random.choice(["FDA", "EMA", "WHO"]),
                "guideline_year": 2024,
                "date_verified": datetime.now().strftime("%Y-%m-%d")
            },
            "recent_news": [
                {
                    "headline": f"FDA approves new indication for {query}",
                    "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
                    "category": random.choice(["Regulatory Approval", "M&A", "Safety Alert"])
                }
            ],
            "_metadata": {
                "source_filter": "Whitelisted (FDA, EMA, NIH, major journals)",
                "paywall_detection": "Open-access versions prioritized",
                "date_verification": "Latest guideline versions confirmed",
                "freshness": "Results from last 6 months",
                "search_completeness": "Comprehensive coverage"
            }
        }

