"""
Industry Templates & Blueprints - Pre-configured agent setups for specific industries
Implements the template system for rapid deployment across different business types
"""
import json
from typing import Dict, Any, List
from datetime import datetime, timezone
from enum import Enum

class IndustryType(Enum):
    ECOMMERCE = "ecommerce"
    SAAS = "saas" 
    LOCAL_SERVICE = "local_service"
    HEALTHCARE = "healthcare"
    FINTECH = "fintech"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"
    RESTAURANT = "restaurant"
    AGENCY = "agency"
    MANUFACTURING = "manufacturing"

class TemplateManager:
    """
    Manages industry-specific templates and blueprints for rapid agent deployment
    """
    
    def __init__(self):
        self.templates = {}
        self._load_industry_templates()
    
    def _load_industry_templates(self):
        """Load all industry-specific templates"""
        
        # E-commerce Template
        self.templates[IndustryType.ECOMMERCE] = {
            "name": "E-commerce Business Template",
            "description": "Complete automation suite for online retail businesses",
            "agents": {
                "sales_agent": {
                    "config": {
                        "qualification_score_threshold": 6.0,
                        "follow_up_intervals": [1, 3, 7],
                        "business_hours": {"start": 8, "end": 20},
                        "response_templates": {
                            "qualified_lead": "Thank you for your interest in our products! I'd love to show you how our solutions can increase your online sales.",
                            "product_inquiry": "Great choice! Let me provide you with detailed information about {product} and how it can benefit your business.",
                            "abandoned_cart": "I noticed you left some items in your cart. Would you like assistance completing your order?"
                        }
                    },
                    "workflows": ["lead_qualification", "cart_recovery", "upsell_campaigns", "customer_retention"]
                },
                "marketing_agent": {
                    "config": {
                        "campaign_types": ["product_launch", "seasonal_promotion", "retention_campaign", "lookalike_audience"],
                        "channels": ["facebook", "google", "instagram", "email", "sms"],
                        "budget_allocation": {"facebook": 0.4, "google": 0.3, "email": 0.2, "other": 0.1}
                    },
                    "workflows": ["campaign_creation", "audience_segmentation", "performance_optimization", "roi_tracking"]
                },
                "content_agent": {
                    "config": {
                        "content_types": ["product_descriptions", "blog_posts", "social_media", "email_campaigns", "ad_copy"],
                        "seo_focus": True,
                        "brand_voice": "professional yet approachable"
                    },
                    "workflows": ["product_content", "seo_optimization", "social_scheduling", "email_sequences"]
                },
                "analytics_agent": {
                    "config": {
                        "kpis": ["conversion_rate", "cart_abandonment", "customer_lifetime_value", "return_rate"],
                        "reporting_frequency": "daily",
                        "alerts": ["inventory_low", "conversion_drop", "traffic_spike"]
                    },
                    "workflows": ["sales_analytics", "customer_behavior", "inventory_optimization", "predictive_modeling"]
                }
            },
            "integrations": ["shopify", "stripe", "mailchimp", "facebook_ads", "google_analytics", "klaviyo"],
            "sample_workflows": [
                {
                    "name": "New Customer Onboarding", 
                    "steps": ["welcome_email", "product_recommendations", "first_purchase_discount", "review_request"],
                    "duration": "14 days"
                },
                {
                    "name": "Abandoned Cart Recovery",
                    "steps": ["cart_reminder_1h", "discount_offer_24h", "last_chance_72h", "win_back_7d"],
                    "duration": "7 days"
                }
            ]
        }
        
        # SaaS Template
        self.templates[IndustryType.SAAS] = {
            "name": "SaaS Business Template", 
            "description": "Comprehensive automation for Software as a Service companies",
            "agents": {
                "sales_agent": {
                    "config": {
                        "qualification_score_threshold": 8.0,
                        "follow_up_intervals": [1, 3, 7, 14, 30],
                        "business_hours": {"start": 9, "end": 18},
                        "response_templates": {
                            "qualified_lead": "Thanks for your interest in {product}! I'd love to show you how we can help streamline your {use_case}.",
                            "demo_request": "Perfect! Let me schedule a personalized demo to show you exactly how {product} can solve your {pain_point}.",
                            "trial_follow_up": "How is your {product} trial going? I'm here to help you get the most value from the platform."
                        }
                    },
                    "workflows": ["lead_scoring", "demo_scheduling", "trial_optimization", "expansion_sales"]
                },
                "marketing_agent": {
                    "config": {
                        "campaign_types": ["freemium_conversion", "trial_activation", "feature_adoption", "churn_prevention"],
                        "channels": ["linkedin", "google", "content_marketing", "webinars", "email"],
                        "funnel_stages": ["awareness", "consideration", "trial", "conversion", "expansion"]
                    },
                    "workflows": ["inbound_marketing", "trial_nurturing", "feature_promotion", "customer_success"]
                },
                "content_agent": {
                    "config": {
                        "content_types": ["documentation", "tutorials", "case_studies", "whitepapers", "webinar_content"],
                        "technical_depth": "high",
                        "audience_personas": ["technical_decision_maker", "business_stakeholder", "end_user"]
                    },
                    "workflows": ["educational_content", "feature_documentation", "success_stories", "thought_leadership"]
                },
                "analytics_agent": {
                    "config": {
                        "kpis": ["mrr", "churn_rate", "trial_conversion", "feature_adoption", "nps_score"],
                        "cohort_analysis": True,
                        "predictive_churn": True
                    },
                    "workflows": ["subscription_analytics", "user_behavior", "churn_prediction", "revenue_forecasting"]
                }
            },
            "integrations": ["stripe", "hubspot", "intercom", "mixpanel", "segment", "slack"],
            "sample_workflows": [
                {
                    "name": "Trial User Activation",
                    "steps": ["welcome_sequence", "feature_tutorials", "use_case_guidance", "success_milestones"],
                    "duration": "14 days"
                },
                {
                    "name": "Expansion Revenue Campaign", 
                    "steps": ["usage_analysis", "upgrade_opportunity", "personalized_outreach", "success_tracking"],
                    "duration": "30 days"
                }
            ]
        }
        
        # Local Service Template
        self.templates[IndustryType.LOCAL_SERVICE] = {
            "name": "Local Service Business Template",
            "description": "Automation suite for local service providers and small businesses",
            "agents": {
                "sales_agent": {
                    "config": {
                        "qualification_score_threshold": 7.0,
                        "follow_up_intervals": [1, 3, 7],
                        "business_hours": {"start": 8, "end": 18},
                        "local_focus": True,
                        "response_templates": {
                            "qualified_lead": "Thank you for contacting {business_name}! I'd love to discuss how we can help with your {service_type} needs.",
                            "appointment_request": "I'd be happy to schedule a consultation. What time works best for you this week?",
                            "follow_up": "Following up on your {service_type} inquiry. Are you still interested in moving forward?"
                        }
                    },
                    "workflows": ["local_lead_qualification", "appointment_scheduling", "quote_generation", "follow_up_sequences"]
                },
                "marketing_agent": {
                    "config": {
                        "campaign_types": ["local_search", "gmb_optimization", "review_generation", "referral_program"],
                        "channels": ["google_my_business", "facebook_local", "nextdoor", "local_directories"],
                        "geo_targeting": True
                    },
                    "workflows": ["local_seo", "reputation_management", "community_engagement", "seasonal_promotions"]
                },
                "content_agent": {
                    "config": {
                        "content_types": ["service_pages", "local_blog", "testimonials", "before_after", "faq"],
                        "local_keywords": True,
                        "community_focus": True
                    },
                    "workflows": ["local_content", "review_responses", "social_media", "educational_posts"]
                },
                "analytics_agent": {
                    "config": {
                        "kpis": ["lead_volume", "conversion_rate", "average_job_value", "customer_satisfaction"],
                        "local_metrics": True,
                        "seasonality_tracking": True
                    },
                    "workflows": ["lead_analytics", "service_performance", "seasonal_trends", "competitor_analysis"]
                }
            },
            "integrations": ["google_my_business", "facebook", "quickbooks", "calendly", "review_platforms"],
            "sample_workflows": [
                {
                    "name": "New Customer Journey",
                    "steps": ["initial_contact", "needs_assessment", "quote_delivery", "service_scheduling", "follow_up"],
                    "duration": "7 days"
                },
                {
                    "name": "Review Generation Campaign",
                    "steps": ["service_completion", "satisfaction_check", "review_request", "response_management"],
                    "duration": "14 days"
                }
            ]
        }
        
        # Healthcare Template
        self.templates[IndustryType.HEALTHCARE] = {
            "name": "Healthcare Practice Template",
            "description": "HIPAA-compliant automation for healthcare providers",
            "agents": {
                "sales_agent": {
                    "config": {
                        "qualification_score_threshold": 8.5,
                        "compliance_mode": "HIPAA",
                        "patient_privacy": True,
                        "response_templates": {
                            "appointment_inquiry": "Thank you for contacting {practice_name}. I'd be happy to help you schedule an appointment with Dr. {doctor_name}.",
                            "insurance_verification": "Let me verify your insurance coverage and provide you with cost estimates for your visit.",
                            "follow_up_care": "How are you feeling after your recent visit? Do you have any questions about your treatment plan?"
                        }
                    },
                    "workflows": ["appointment_scheduling", "insurance_verification", "patient_onboarding", "care_coordination"]
                },
                "marketing_agent": {
                    "config": {
                        "campaign_types": ["patient_education", "preventive_care", "service_awareness", "health_screenings"],
                        "channels": ["website", "email", "patient_portal", "community_outreach"],
                        "compliance_requirements": ["HIPAA", "medical_advertising"]
                    },
                    "workflows": ["patient_education", "wellness_campaigns", "appointment_reminders", "health_screenings"]
                },
                "content_agent": {
                    "config": {
                        "content_types": ["patient_education", "procedure_explanations", "health_tips", "practice_updates"],
                        "medical_accuracy": True,
                        "compliance_review": True
                    },
                    "workflows": ["educational_content", "procedure_guides", "wellness_tips", "practice_communications"]
                },
                "analytics_agent": {
                    "config": {
                        "kpis": ["patient_satisfaction", "appointment_adherence", "treatment_outcomes", "practice_efficiency"],
                        "privacy_protection": True,
                        "outcome_tracking": True
                    },
                    "workflows": ["patient_analytics", "outcome_measurement", "practice_performance", "quality_improvement"]
                }
            },
            "integrations": ["epic", "cerner", "allscripts", "patient_portal", "insurance_systems"],
            "sample_workflows": [
                {
                    "name": "New Patient Onboarding",
                    "steps": ["appointment_scheduling", "intake_forms", "insurance_verification", "pre_visit_preparation"],
                    "duration": "3 days"
                },
                {
                    "name": "Preventive Care Campaign",
                    "steps": ["screening_eligibility", "patient_outreach", "appointment_booking", "follow_up_care"],
                    "duration": "30 days"
                }
            ]
        }
        
        # Add more templates...
        self._add_additional_templates()
    
    def _add_additional_templates(self):
        """Add remaining industry templates"""
        
        # Fintech Template
        self.templates[IndustryType.FINTECH] = {
            "name": "Fintech Business Template",
            "description": "Secure automation for financial technology companies",
            "focus_areas": ["compliance", "security", "customer_trust", "regulatory_reporting"],
            "key_features": ["fraud_detection", "kyc_automation", "risk_assessment", "regulatory_compliance"]
        }
        
        # Real Estate Template  
        self.templates[IndustryType.REAL_ESTATE] = {
            "name": "Real Estate Agency Template",
            "description": "Complete automation for real estate professionals",
            "focus_areas": ["lead_nurturing", "property_marketing", "client_management", "transaction_coordination"],
            "key_features": ["crm_integration", "listing_automation", "market_analysis", "client_communication"]
        }
        
        # Restaurant Template
        self.templates[IndustryType.RESTAURANT] = {
            "name": "Restaurant Business Template", 
            "description": "Hospitality-focused automation for restaurants and food services",
            "focus_areas": ["reservation_management", "customer_experience", "inventory_optimization", "delivery_coordination"],
            "key_features": ["pos_integration", "review_management", "loyalty_programs", "delivery_platforms"]
        }
    
    def get_template(self, industry: IndustryType) -> Dict[str, Any]:
        """Get specific industry template"""
        return self.templates.get(industry, {})
    
    def get_all_templates(self) -> Dict[str, Any]:
        """Get all available templates"""
        return {
            "templates": {industry.value: template for industry, template in self.templates.items()},
            "total_templates": len(self.templates),
            "industries": [industry.value for industry in IndustryType]
        }
    
    def generate_deployment_config(self, industry: IndustryType, customizations: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate deployment configuration for specific industry"""
        template = self.get_template(industry)
        
        if not template:
            return {"error": f"Template not found for industry: {industry.value}"}
        
        # Base configuration
        deployment_config = {
            "deployment_id": f"deploy_{industry.value}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            "industry": industry.value,
            "template_name": template.get("name"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "agents_to_deploy": [],
            "integrations_to_setup": template.get("integrations", []),
            "workflows_to_activate": [],
            "estimated_setup_time": "30-45 minutes"
        }
        
        # Agent configurations
        for agent_name, agent_config in template.get("agents", {}).items():
            agent_deployment = {
                "agent_type": agent_name,
                "config": agent_config.get("config", {}),
                "workflows": agent_config.get("workflows", []),
                "priority": "high" if agent_name == "sales_agent" else "medium"
            }
            
            # Apply customizations
            if customizations and agent_name in customizations:
                custom_config = customizations[agent_name]
                agent_deployment["config"].update(custom_config)
            
            deployment_config["agents_to_deploy"].append(agent_deployment)
        
        # Workflow configurations
        for workflow in template.get("sample_workflows", []):
            workflow_config = {
                "name": workflow["name"],
                "steps": workflow["steps"],
                "duration": workflow["duration"],
                "auto_activate": True
            }
            deployment_config["workflows_to_activate"].append(workflow_config)
        
        return deployment_config
    
    def validate_template_compatibility(self, industry: IndustryType, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if template meets specific requirements"""
        template = self.get_template(industry)
        
        validation_result = {
            "compatible": True,
            "missing_features": [],
            "additional_setup_required": [],
            "recommendations": []
        }
        
        # Check required features
        required_features = requirements.get("features", [])
        template_features = template.get("key_features", [])
        
        for feature in required_features:
            if feature not in template_features:
                validation_result["missing_features"].append(feature)
                validation_result["compatible"] = False
        
        # Check required integrations
        required_integrations = requirements.get("integrations", [])
        template_integrations = template.get("integrations", [])
        
        for integration in required_integrations:
            if integration not in template_integrations:
                validation_result["additional_setup_required"].append(f"Custom integration: {integration}")
        
        # Add recommendations
        if not validation_result["compatible"]:
            validation_result["recommendations"].append("Consider custom development for missing features")
        
        if validation_result["additional_setup_required"]:
            validation_result["recommendations"].append("Plan for additional integration setup time")
        
        validation_result["recommendations"].append(f"Template provides {len(template_integrations)} out-of-box integrations")
        
        return validation_result
    
    def create_custom_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a custom industry template"""
        try:
            template_name = template_data.get("name", "Custom Template")
            template_id = template_data.get("id", template_name.lower().replace(" ", "_"))
            
            custom_template = {
                "name": template_name,
                "description": template_data.get("description", "Custom industry template"),
                "industry": "custom",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "agents": template_data.get("agents", {}),
                "integrations": template_data.get("integrations", []),
                "workflows": template_data.get("workflows", []),
                "custom_config": template_data.get("config", {})
            }
            
            # Store custom template
            self.templates[template_id] = custom_template
            
            return {
                "template_id": template_id,
                "message": "Custom template created successfully",
                "template": custom_template
            }
            
        except Exception as e:
            return {"error": f"Failed to create custom template: {str(e)}"}

# Global template manager instance
template_manager = TemplateManager()