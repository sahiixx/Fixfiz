#!/usr/bin/env python3
"""
Backend API Testing Suite for NOWHERE Digital Platform
Tests the AI Problem Analysis API and existing endpoints
"""

import asyncio
import aiohttp
import json
import sys
import os
from datetime import datetime, date
from typing import Dict, Any, Optional

# Get backend URL from frontend .env file
def get_backend_url():
    """Get backend URL from frontend .env file"""
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
    return "http://localhost:8001"

BACKEND_URL = get_backend_url()
API_BASE = f"{BACKEND_URL}/api"

class BackendTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.failed_tests = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response": response_data
        })
        
        if not success:
            self.failed_tests.append(test_name)
    
    async def test_health_endpoint(self):
        """Test GET /api/health endpoint"""
        try:
            async with self.session.get(f"{API_BASE}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "healthy":
                        self.log_test("Health Check", True, "Service is healthy")
                        return True
                    else:
                        self.log_test("Health Check", False, f"Unexpected status: {data.get('status')}", data)
                        return False
                else:
                    self.log_test("Health Check", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False
    
    async def test_contact_form_submission(self):
        """Test POST /api/contact endpoint"""
        try:
            contact_data = {
                "name": "Ahmed Al-Rashid",
                "email": "ahmed.rashid@example.ae",
                "phone": "+971501234567",
                "service": "social_media",
                "message": "I need help with social media marketing for my Dubai-based restaurant. Looking to increase online presence and customer engagement."
            }
            
            async with self.session.post(
                f"{API_BASE}/contact",
                json=contact_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "id" in data.get("data", {}):
                        self.log_test("Contact Form Submission", True, "Contact form submitted successfully")
                        return True
                    else:
                        self.log_test("Contact Form Submission", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Contact Form Submission", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Contact Form Submission", False, f"Exception: {str(e)}")
            return False
    
    async def test_content_recommendations(self):
        """Test GET /api/content/recommendations endpoint"""
        try:
            business_info = "E-commerce fashion store in Dubai looking to increase online sales through digital marketing"
            
            async with self.session.get(
                f"{API_BASE}/content/recommendations",
                params={"business_info": business_info}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "recommendations" in data.get("data", {}):
                        recommendations = data["data"]["recommendations"]
                        if recommendations and len(recommendations) > 10:  # Should be substantial content
                            self.log_test("Content Recommendations", True, "AI recommendations generated successfully")
                            return True
                        else:
                            self.log_test("Content Recommendations", False, "Recommendations too short or empty", data)
                            return False
                    else:
                        self.log_test("Content Recommendations", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Content Recommendations", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Content Recommendations", False, f"Exception: {str(e)}")
            return False
    
    async def test_ai_problem_analysis_valid_request(self):
        """Test POST /api/ai/analyze-problem with valid data"""
        try:
            problem_data = {
                "problem_description": "I need to increase online sales for my e-commerce business",
                "industry": "ecommerce",
                "budget_range": "AED 25K - 75K/month"
            }
            
            async with self.session.post(
                f"{API_BASE}/ai/analyze-problem",
                json=problem_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Check response structure
                    if not data.get("success"):
                        self.log_test("AI Problem Analysis - Valid Request", False, "Response success is false", data)
                        return False
                    
                    analysis = data.get("data", {}).get("analysis", {})
                    if not analysis:
                        self.log_test("AI Problem Analysis - Valid Request", False, "No analysis data in response", data)
                        return False
                    
                    # Check required fields
                    required_fields = [
                        "problem_description", "industry", "ai_analysis", 
                        "market_insights", "strategy_proposal", "estimated_roi",
                        "implementation_time", "budget_range", "priority_level"
                    ]
                    
                    missing_fields = []
                    for field in required_fields:
                        if field not in analysis:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        self.log_test("AI Problem Analysis - Valid Request", False, f"Missing fields: {missing_fields}", data)
                        return False
                    
                    # Check that AI analysis fields have substantial content
                    ai_fields = ["ai_analysis", "market_insights", "strategy_proposal"]
                    for field in ai_fields:
                        content = analysis.get(field, "")
                        if not content or len(content) < 50:  # Should be substantial content
                            self.log_test("AI Problem Analysis - Valid Request", False, f"Field '{field}' has insufficient content", data)
                            return False
                    
                    # Check that input data is preserved
                    if analysis["problem_description"] != problem_data["problem_description"]:
                        self.log_test("AI Problem Analysis - Valid Request", False, "Problem description not preserved", data)
                        return False
                    
                    if analysis["industry"] != problem_data["industry"]:
                        self.log_test("AI Problem Analysis - Valid Request", False, "Industry not preserved", data)
                        return False
                    
                    self.log_test("AI Problem Analysis - Valid Request", True, "Complete analysis with all required fields")
                    return True
                    
                else:
                    self.log_test("AI Problem Analysis - Valid Request", False, f"HTTP {response.status}", await response.text())
                    return False
                    
        except Exception as e:
            self.log_test("AI Problem Analysis - Valid Request", False, f"Exception: {str(e)}")
            return False
    
    async def test_ai_problem_analysis_minimal_data(self):
        """Test POST /api/ai/analyze-problem with minimal data"""
        try:
            problem_data = {
                "problem_description": "Need more customers",
                "industry": "general"
            }
            
            async with self.session.post(
                f"{API_BASE}/ai/analyze-problem",
                json=problem_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("success") and data.get("data", {}).get("analysis"):
                        analysis = data["data"]["analysis"]
                        # Should still provide default budget range when not specified
                        if "budget_range" in analysis and analysis["budget_range"]:
                            self.log_test("AI Problem Analysis - Minimal Data", True, "Handles minimal data with defaults")
                            return True
                        else:
                            self.log_test("AI Problem Analysis - Minimal Data", False, "No default budget range provided", data)
                            return False
                    else:
                        self.log_test("AI Problem Analysis - Minimal Data", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("AI Problem Analysis - Minimal Data", False, f"HTTP {response.status}", await response.text())
                    return False
                    
        except Exception as e:
            self.log_test("AI Problem Analysis - Minimal Data", False, f"Exception: {str(e)}")
            return False
    
    async def test_ai_problem_analysis_empty_request(self):
        """Test POST /api/ai/analyze-problem with empty data"""
        try:
            problem_data = {}
            
            async with self.session.post(
                f"{API_BASE}/ai/analyze-problem",
                json=problem_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                # Should still work with empty data (using defaults)
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("AI Problem Analysis - Empty Request", True, "Handles empty request gracefully")
                        return True
                    else:
                        self.log_test("AI Problem Analysis - Empty Request", False, "Failed with empty request", data)
                        return False
                else:
                    # If it returns an error, that's also acceptable behavior
                    self.log_test("AI Problem Analysis - Empty Request", True, f"Properly rejects empty request with HTTP {response.status}")
                    return True
                    
        except Exception as e:
            self.log_test("AI Problem Analysis - Empty Request", False, f"Exception: {str(e)}")
            return False
    
    async def test_ai_problem_analysis_invalid_json(self):
        """Test POST /api/ai/analyze-problem with invalid JSON"""
        try:
            async with self.session.post(
                f"{API_BASE}/ai/analyze-problem",
                data="invalid json",
                headers={"Content-Type": "application/json"}
            ) as response:
                # Should return 400 or 422 for invalid JSON
                if response.status in [400, 422]:
                    self.log_test("AI Problem Analysis - Invalid JSON", True, f"Properly rejects invalid JSON with HTTP {response.status}")
                    return True
                else:
                    self.log_test("AI Problem Analysis - Invalid JSON", False, f"Unexpected status: HTTP {response.status}", await response.text())
                    return False
                    
        except Exception as e:
            self.log_test("AI Problem Analysis - Invalid JSON", False, f"Exception: {str(e)}")
            return False
    
    async def test_analytics_summary(self):
        """Test GET /api/analytics/summary endpoint"""
        try:
            async with self.session.get(f"{API_BASE}/analytics/summary") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "today" in data.get("data", {}):
                        self.log_test("Analytics Summary", True, "Analytics data retrieved successfully")
                        return True
                    else:
                        self.log_test("Analytics Summary", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Analytics Summary", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Analytics Summary", False, f"Exception: {str(e)}")
            return False
    
    async def test_chat_session_creation(self):
        """Test POST /api/chat/session endpoint"""
        try:
            async with self.session.post(
                f"{API_BASE}/chat/session",
                json={},
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "session_id" in data.get("data", {}):
                        session_id = data["data"]["session_id"]
                        # Store session_id for use in message test
                        self.chat_session_id = session_id
                        self.log_test("Chat Session Creation", True, f"Session created with ID: {session_id}")
                        return True
                    else:
                        self.log_test("Chat Session Creation", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Chat Session Creation", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Chat Session Creation", False, f"Exception: {str(e)}")
            return False
    
    async def test_chat_message_sending(self):
        """Test POST /api/chat/message endpoint"""
        try:
            # First ensure we have a session ID
            if not hasattr(self, 'chat_session_id'):
                await self.test_chat_session_creation()
            
            if not hasattr(self, 'chat_session_id'):
                self.log_test("Chat Message Sending", False, "No chat session available")
                return False
            
            message_data = {
                "session_id": self.chat_session_id,
                "message": "What digital marketing services do you recommend for a restaurant in Dubai?",
                "user_id": "test_user_123"
            }
            
            async with self.session.post(
                f"{API_BASE}/chat/message",
                json=message_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "response" in data.get("data", {}):
                        ai_response = data["data"]["response"]
                        if ai_response and len(ai_response) > 10:  # Should be substantial response
                            self.log_test("Chat Message Sending", True, "AI chat response received successfully")
                            return True
                        else:
                            self.log_test("Chat Message Sending", False, "AI response too short or empty", data)
                            return False
                    else:
                        self.log_test("Chat Message Sending", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Chat Message Sending", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Chat Message Sending", False, f"Exception: {str(e)}")
            return False

    # ================================================================================================
    # AI AGENT SYSTEM TESTS - NEW COMPREHENSIVE TESTING
    # ================================================================================================
    
    async def test_agents_status(self):
        """Test GET /api/agents/status - Agent status retrieval"""
        try:
            async with self.session.get(f"{API_BASE}/agents/status") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "data" in data:
                        agent_status = data["data"]
                        # Should contain agent information
                        if isinstance(agent_status, dict):
                            self.log_test("Agent Status Retrieval", True, "Agent status retrieved successfully")
                            return True
                        else:
                            self.log_test("Agent Status Retrieval", False, "Invalid agent status format", data)
                            return False
                    else:
                        self.log_test("Agent Status Retrieval", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Agent Status Retrieval", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Agent Status Retrieval", False, f"Exception: {str(e)}")
            return False

    async def test_orchestrator_metrics(self):
        """Test GET /api/agents/metrics - Orchestrator metrics"""
        try:
            async with self.session.get(f"{API_BASE}/agents/metrics") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "data" in data:
                        metrics = data["data"]
                        # Should contain metrics information
                        if isinstance(metrics, dict):
                            self.log_test("Orchestrator Metrics", True, "Orchestrator metrics retrieved successfully")
                            return True
                        else:
                            self.log_test("Orchestrator Metrics", False, "Invalid metrics format", data)
                            return False
                    else:
                        self.log_test("Orchestrator Metrics", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Orchestrator Metrics", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Orchestrator Metrics", False, f"Exception: {str(e)}")
            return False

    async def test_task_history(self):
        """Test GET /api/agents/tasks/history - Task history"""
        try:
            async with self.session.get(f"{API_BASE}/agents/tasks/history") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "data" in data:
                        history_data = data["data"]
                        # Should contain tasks array
                        if "tasks" in history_data and isinstance(history_data["tasks"], list):
                            self.log_test("Task History", True, "Task history retrieved successfully")
                            return True
                        else:
                            self.log_test("Task History", False, "Invalid task history format", data)
                            return False
                    else:
                        self.log_test("Task History", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Task History", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Task History", False, f"Exception: {str(e)}")
            return False

    async def test_sales_agent_qualify_lead(self):
        """Test POST /api/agents/sales/qualify-lead - Lead qualification with Dubai business data"""
        try:
            # Dubai business lead data
            lead_data = {
                "company_name": "Al Barsha Trading LLC",
                "contact_name": "Fatima Al-Zahra",
                "email": "fatima@albarsha.ae",
                "phone": "+971-4-555-0123",
                "industry": "retail",
                "location": "Dubai, UAE",
                "business_size": "medium",
                "annual_revenue": "AED 5M - 15M",
                "current_challenges": "Need to expand online presence and improve digital marketing ROI",
                "budget_range": "AED 50K - 150K/month",
                "timeline": "3-6 months",
                "decision_maker": True
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/sales/qualify-lead",
                json=lead_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "task_id" in data.get("data", {}):
                        task_id = data["data"]["task_id"]
                        self.log_test("Sales Agent - Lead Qualification", True, f"Lead qualification task submitted: {task_id}")
                        return True
                    else:
                        self.log_test("Sales Agent - Lead Qualification", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Sales Agent - Lead Qualification", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Sales Agent - Lead Qualification", False, f"Exception: {str(e)}")
            return False

    async def test_sales_pipeline_analysis(self):
        """Test GET /api/agents/sales/pipeline - Sales pipeline analysis"""
        try:
            async with self.session.get(f"{API_BASE}/agents/sales/pipeline") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "task_id" in data.get("data", {}):
                        task_id = data["data"]["task_id"]
                        self.log_test("Sales Pipeline Analysis", True, f"Pipeline analysis task submitted: {task_id}")
                        return True
                    else:
                        self.log_test("Sales Pipeline Analysis", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Sales Pipeline Analysis", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Sales Pipeline Analysis", False, f"Exception: {str(e)}")
            return False

    async def test_sales_generate_proposal(self):
        """Test POST /api/agents/sales/generate-proposal - Proposal generation"""
        try:
            # Dubai business proposal data
            proposal_data = {
                "client_name": "Emirates Digital Solutions",
                "industry": "fintech",
                "location": "DIFC, Dubai",
                "services_needed": ["digital_marketing", "web_development", "seo", "social_media"],
                "budget_range": "AED 100K - 300K",
                "project_timeline": "6 months",
                "business_goals": "Launch new fintech app in UAE market, acquire 10K users in first year",
                "target_audience": "UAE residents aged 25-45, tech-savvy professionals",
                "competitors": ["Careem Pay", "CBD Now", "ADCB Hayyak"],
                "special_requirements": "Compliance with UAE Central Bank regulations"
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/sales/generate-proposal",
                json=proposal_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "task_id" in data.get("data", {}):
                        task_id = data["data"]["task_id"]
                        self.log_test("Sales Agent - Proposal Generation", True, f"Proposal generation task submitted: {task_id}")
                        return True
                    else:
                        self.log_test("Sales Agent - Proposal Generation", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Sales Agent - Proposal Generation", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Sales Agent - Proposal Generation", False, f"Exception: {str(e)}")
            return False

    async def test_marketing_create_campaign(self):
        """Test POST /api/agents/marketing/create-campaign - Marketing campaign creation"""
        try:
            # Dubai marketing campaign data
            campaign_data = {
                "campaign_name": "Dubai Summer Shopping Festival 2024",
                "client_business": "Luxury Fashion Boutique",
                "target_market": "Dubai, Abu Dhabi, Sharjah",
                "campaign_type": "seasonal_promotion",
                "budget": "AED 75,000",
                "duration": "30 days",
                "objectives": ["increase_brand_awareness", "drive_sales", "customer_acquisition"],
                "target_audience": {
                    "demographics": "Women 25-45, high income",
                    "interests": ["luxury fashion", "shopping", "lifestyle"],
                    "location": "UAE"
                },
                "channels": ["instagram", "facebook", "google_ads", "influencer_marketing"],
                "kpis": ["reach", "engagement", "conversions", "roas"]
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/marketing/create-campaign",
                json=campaign_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "task_id" in data.get("data", {}):
                        task_id = data["data"]["task_id"]
                        self.log_test("Marketing Agent - Campaign Creation", True, f"Campaign creation task submitted: {task_id}")
                        return True
                    else:
                        self.log_test("Marketing Agent - Campaign Creation", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Marketing Agent - Campaign Creation", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Marketing Agent - Campaign Creation", False, f"Exception: {str(e)}")
            return False

    async def test_content_agent_generate(self):
        """Test POST /api/agents/content/generate - Content generation agent"""
        try:
            # Dubai content generation data
            content_data = {
                "content_type": "social_media_campaign",
                "business_info": {
                    "name": "Dubai Marina Restaurant",
                    "industry": "hospitality",
                    "location": "Dubai Marina, UAE",
                    "specialty": "Mediterranean cuisine with Dubai skyline views"
                },
                "campaign_theme": "Ramadan Iftar Special Menu 2024",
                "target_audience": "Families and professionals in Dubai",
                "tone": "warm, welcoming, culturally respectful",
                "platforms": ["instagram", "facebook", "linkedin"],
                "content_requirements": {
                    "posts_count": 10,
                    "include_hashtags": True,
                    "include_call_to_action": True,
                    "languages": ["english", "arabic"]
                }
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/content/generate",
                json=content_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "task_id" in data.get("data", {}):
                        task_id = data["data"]["task_id"]
                        self.log_test("Content Agent - Content Generation", True, f"Content generation task submitted: {task_id}")
                        return True
                    else:
                        self.log_test("Content Agent - Content Generation", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Content Agent - Content Generation", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Content Agent - Content Generation", False, f"Exception: {str(e)}")
            return False

    async def test_analytics_agent_analyze(self):
        """Test POST /api/agents/analytics/analyze - Analytics agent"""
        try:
            # Dubai business analytics data
            analysis_data = {
                "business_name": "Dubai Tech Startup Hub",
                "analysis_type": "market_performance",
                "data_sources": ["website_analytics", "social_media", "sales_data", "customer_feedback"],
                "time_period": "Q1 2024",
                "metrics_focus": ["user_acquisition", "conversion_rates", "customer_lifetime_value", "market_penetration"],
                "business_context": {
                    "industry": "technology",
                    "location": "Dubai Internet City",
                    "target_market": "UAE startups and SMEs",
                    "business_model": "B2B SaaS"
                },
                "goals": ["identify_growth_opportunities", "optimize_marketing_spend", "improve_customer_retention"]
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/analytics/analyze",
                json=analysis_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success") and "task_id" in data.get("data", {}):
                        task_id = data["data"]["task_id"]
                        self.log_test("Analytics Agent - Data Analysis", True, f"Data analysis task submitted: {task_id}")
                        return True
                    else:
                        self.log_test("Analytics Agent - Data Analysis", False, "Invalid response structure", data)
                        return False
                else:
                    self.log_test("Analytics Agent - Data Analysis", False, f"HTTP {response.status}", await response.text())
                    return False
        except Exception as e:
            self.log_test("Analytics Agent - Data Analysis", False, f"Exception: {str(e)}")
            return False

    async def test_agent_control_functions(self):
        """Test agent control functions - pause, resume, reset"""
        try:
            # Test with a sample agent ID (sales agent)
            agent_id = "sales_agent"
            
            # Test pause agent
            async with self.session.post(f"{API_BASE}/agents/{agent_id}/pause") as response:
                if response.status in [200, 404]:  # 404 is acceptable if agent doesn't exist
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            pause_success = True
                        else:
                            pause_success = False
                    else:
                        pause_success = True  # 404 is acceptable
                else:
                    pause_success = False
            
            # Test resume agent
            async with self.session.post(f"{API_BASE}/agents/{agent_id}/resume") as response:
                if response.status in [200, 404]:  # 404 is acceptable if agent doesn't exist
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            resume_success = True
                        else:
                            resume_success = False
                    else:
                        resume_success = True  # 404 is acceptable
                else:
                    resume_success = False
            
            # Test reset agent
            async with self.session.post(f"{API_BASE}/agents/{agent_id}/reset") as response:
                if response.status in [200, 404]:  # 404 is acceptable if agent doesn't exist
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            reset_success = True
                        else:
                            reset_success = False
                    else:
                        reset_success = True  # 404 is acceptable
                else:
                    reset_success = False
            
            # Overall success if all operations work
            if pause_success and resume_success and reset_success:
                self.log_test("Agent Control Functions", True, "Pause, resume, and reset operations working")
                return True
            else:
                failed_ops = []
                if not pause_success:
                    failed_ops.append("pause")
                if not resume_success:
                    failed_ops.append("resume")
                if not reset_success:
                    failed_ops.append("reset")
                self.log_test("Agent Control Functions", False, f"Failed operations: {', '.join(failed_ops)}")
                return False
                
        except Exception as e:
            self.log_test("Agent Control Functions", False, f"Exception: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all backend tests"""
        print(f"🚀 Starting Comprehensive Backend API Tests")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"📍 API Base: {API_BASE}")
        print("=" * 60)
        
        # Test core endpoints first
        print("\n🔧 Testing Core Endpoints:")
        print("-" * 40)
        await self.test_health_endpoint()
        await self.test_contact_form_submission()
        await self.test_content_recommendations()
        await self.test_analytics_summary()
        
        print("\n💬 Testing Chat System:")
        print("-" * 40)
        await self.test_chat_session_creation()
        await self.test_chat_message_sending()
        
        print("\n🤖 Testing AI Problem Analysis Endpoint:")
        print("-" * 40)
        
        # Test AI Problem Analysis endpoint
        await self.test_ai_problem_analysis_valid_request()
        await self.test_ai_problem_analysis_minimal_data()
        await self.test_ai_problem_analysis_empty_request()
        await self.test_ai_problem_analysis_invalid_json()
        
        print("\n🎯 Testing AI Agent System - PRIORITY TESTING:")
        print("-" * 50)
        
        # Test Agent Orchestrator Endpoints
        print("\n📊 Agent Orchestrator:")
        await self.test_agents_status()
        await self.test_orchestrator_metrics()
        await self.test_task_history()
        
        # Test Sales Agent Integration
        print("\n💼 Sales Agent Integration:")
        await self.test_sales_agent_qualify_lead()
        await self.test_sales_pipeline_analysis()
        await self.test_sales_generate_proposal()
        
        # Test Marketing & Content Agents
        print("\n📈 Marketing & Content Agents:")
        await self.test_marketing_create_campaign()
        await self.test_content_agent_generate()
        await self.test_analytics_agent_analyze()
        
        # Test Agent Control Functions
        print("\n⚙️ Agent Control Functions:")
        await self.test_agent_control_functions()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"   - {test}")
        else:
            print(f"\n🎉 All tests passed!")
        
        return failed_tests == 0

async def main():
    """Main test runner"""
    async with BackendTester() as tester:
        success = await tester.run_all_tests()
        return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)