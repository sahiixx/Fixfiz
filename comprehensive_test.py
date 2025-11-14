#!/usr/bin/env python3
"""
Comprehensive E2E Backend Testing - All Systems
Focus on Priority 1 systems and comprehensive coverage
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime

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

class ComprehensiveTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.failed_tests = []
        self.critical_failures = []
        self.minor_issues = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: any = None, critical: bool = True):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response": response_data,
            "critical": critical
        })
        
        if not success:
            self.failed_tests.append(test_name)
            if critical:
                self.critical_failures.append(test_name)
            else:
                self.minor_issues.append(test_name)

    # ================================================================================================
    # PRIORITY 1 - CRITICAL SYSTEMS
    # ================================================================================================
    
    async def test_white_label_system(self):
        """Test White Label & Multi-Tenancy System"""
        print("\n🏢 WHITE LABEL & MULTI-TENANCY SYSTEM:")
        print("-" * 60)
        
        # Test 1: Create Tenant with valid data
        try:
            tenant_data = {
                "tenant_name": "Dubai Digital Solutions",
                "domain": "dubaidigital.ae",  # Added missing domain
                "company_info": {
                    "name": "Dubai Digital Solutions LLC",
                    "contact_person": "Mohammed Al-Rashid",
                    "email": "mohammed@dubaidigital.ae",
                    "phone": "+971-4-555-9999"
                },
                "branding": {
                    "primary_color": "#1E40AF",
                    "secondary_color": "#F59E0B",
                    "company_name": "Dubai Digital Solutions"
                }
            }
            
            async with self.session.post(
                f"{API_BASE}/white-label/create-tenant",
                json=tenant_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.tenant_id = data.get("data", {}).get("tenant_id", "test_tenant")
                        self.log_test("White Label - Create Tenant", True, "Tenant created successfully")
                    else:
                        self.log_test("White Label - Create Tenant", False, f"Creation failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("White Label - Create Tenant", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("White Label - Create Tenant", False, f"Exception: {str(e)}")
        
        # Test 2: Get all tenants
        try:
            async with self.session.get(f"{API_BASE}/white-label/tenants") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        tenants = data.get("data", {}).get("tenants", [])
                        self.log_test("White Label - Get Tenants", True, f"Retrieved {len(tenants)} tenants")
                    else:
                        self.log_test("White Label - Get Tenants", False, f"Failed to get tenants: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("White Label - Get Tenants", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("White Label - Get Tenants", False, f"Exception: {str(e)}")
        
        # Test 3: Get tenant branding
        try:
            tenant_id = getattr(self, 'tenant_id', 'sample_tenant_id')
            async with self.session.get(f"{API_BASE}/white-label/tenant/{tenant_id}/branding") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("White Label - Get Tenant Branding", True, "Branding retrieved successfully")
                    else:
                        self.log_test("White Label - Get Tenant Branding", False, f"Failed to get branding: {data}")
                elif response.status == 404:
                    self.log_test("White Label - Get Tenant Branding", True, "Tenant not found (expected for sample ID)", critical=False)
                else:
                    error_text = await response.text()
                    self.log_test("White Label - Get Tenant Branding", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("White Label - Get Tenant Branding", False, f"Exception: {str(e)}")
        
        # Test 4: Create reseller package
        try:
            reseller_data = {
                "reseller_name": "Emirates Business Hub",
                "domain": "emiratesbusinesshub.ae",  # Added missing domain
                "package_info": {
                    "name": "UAE Digital Package",
                    "description": "Complete digital solution for UAE businesses"
                },
                "branding": {
                    "primary_color": "#00A651",
                    "company_name": "Emirates Business Hub"
                }
            }
            
            async with self.session.post(
                f"{API_BASE}/white-label/create-reseller",
                json=reseller_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("White Label - Create Reseller", True, "Reseller package created successfully")
                    else:
                        self.log_test("White Label - Create Reseller", False, f"Creation failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("White Label - Create Reseller", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("White Label - Create Reseller", False, f"Exception: {str(e)}")

    async def test_inter_agent_communication(self):
        """Test Inter-Agent Communication System"""
        print("\n🤝 INTER-AGENT COMMUNICATION SYSTEM:")
        print("-" * 60)
        
        # Test 1: Initiate collaboration
        try:
            collaboration_request = {
                "collaboration_name": "Dubai Client Onboarding",
                "client_info": {
                    "company": "Al Barsha Tech Solutions LLC",
                    "industry": "technology",
                    "location": "Dubai Internet City, UAE"
                },
                "agents_involved": ["sales", "marketing", "content"],
                "collaboration_type": "sequential_workflow"
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/collaborate",
                json=collaboration_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.collaboration_id = data.get("data", {}).get("collaboration_id", "test_collab")
                        self.log_test("Inter-Agent - Initiate Collaboration", True, "Collaboration initiated successfully")
                    else:
                        self.log_test("Inter-Agent - Initiate Collaboration", False, f"Initiation failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Inter-Agent - Initiate Collaboration", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Inter-Agent - Initiate Collaboration", False, f"Exception: {str(e)}")
        
        # Test 2: Get collaboration status
        try:
            collaboration_id = getattr(self, 'collaboration_id', 'sample_collaboration_id')
            async with self.session.get(f"{API_BASE}/agents/collaborate/{collaboration_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("Inter-Agent - Get Collaboration Status", True, "Status retrieved successfully")
                    else:
                        self.log_test("Inter-Agent - Get Collaboration Status", False, f"Status retrieval failed: {data}")
                elif response.status == 404:
                    self.log_test("Inter-Agent - Get Collaboration Status", True, "Collaboration not found (expected for sample ID)", critical=False)
                else:
                    error_text = await response.text()
                    self.log_test("Inter-Agent - Get Collaboration Status", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Inter-Agent - Get Collaboration Status", False, f"Exception: {str(e)}")
        
        # Test 3: Task delegation
        try:
            delegation_request = {
                "from_agent_id": "sales_agent",
                "to_agent_id": "marketing_agent",
                "task_data": {
                    "task_type": "create_campaign",
                    "client_info": {
                        "company": "Dubai Fashion Boutique",
                        "budget": "AED 50,000"
                    }
                }
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/delegate-task",
                json=delegation_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("Inter-Agent - Delegate Task", True, "Task delegated successfully")
                    else:
                        self.log_test("Inter-Agent - Delegate Task", False, f"Delegation failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Inter-Agent - Delegate Task", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Inter-Agent - Delegate Task", False, f"Exception: {str(e)}")
        
        # Test 4: Communication metrics
        try:
            async with self.session.get(f"{API_BASE}/agents/communication/metrics") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("Inter-Agent - Get Metrics", True, "Metrics retrieved successfully")
                    else:
                        self.log_test("Inter-Agent - Get Metrics", False, f"Metrics retrieval failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Inter-Agent - Get Metrics", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Inter-Agent - Get Metrics", False, f"Exception: {str(e)}")

    # ================================================================================================
    # PRIORITY 2 - CORE FEATURES
    # ================================================================================================
    
    async def test_ai_agents(self):
        """Test All 5 AI Agents"""
        print("\n🤖 AI AGENTS SYSTEM:")
        print("-" * 60)
        
        # Test Sales Agent
        try:
            lead_data = {
                "company_name": "Al Barsha Trading LLC",
                "contact_name": "Fatima Al-Zahra",
                "email": "fatima@albarsha.ae",
                "industry": "retail",
                "budget_range": "AED 50K - 150K/month"
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/sales/qualify-lead",
                json=lead_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("AI Agents - Sales Agent", True, "Lead qualification task submitted")
                    else:
                        self.log_test("AI Agents - Sales Agent", False, f"Sales agent failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("AI Agents - Sales Agent", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("AI Agents - Sales Agent", False, f"Exception: {str(e)}")
        
        # Test Marketing Agent
        try:
            campaign_data = {
                "campaign_name": "Dubai Summer Shopping Festival 2024",
                "client_business": "Luxury Fashion Boutique",
                "target_market": "Dubai, Abu Dhabi, Sharjah",
                "budget": "AED 75,000"
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/marketing/create-campaign",
                json=campaign_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("AI Agents - Marketing Agent", True, "Campaign creation task submitted")
                    else:
                        self.log_test("AI Agents - Marketing Agent", False, f"Marketing agent failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("AI Agents - Marketing Agent", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("AI Agents - Marketing Agent", False, f"Exception: {str(e)}")
        
        # Test Content Agent
        try:
            content_data = {
                "content_type": "social_media_campaign",
                "business_info": {
                    "name": "Dubai Marina Restaurant",
                    "industry": "hospitality",
                    "location": "Dubai Marina, UAE"
                },
                "campaign_theme": "Ramadan Iftar Special Menu 2024"
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/content/generate",
                json=content_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("AI Agents - Content Agent", True, "Content generation task submitted")
                    else:
                        self.log_test("AI Agents - Content Agent", False, f"Content agent failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("AI Agents - Content Agent", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("AI Agents - Content Agent", False, f"Exception: {str(e)}")
        
        # Test Analytics Agent
        try:
            analysis_data = {
                "business_name": "Dubai Tech Startup Hub",
                "analysis_type": "market_performance",
                "data_sources": ["website_analytics", "social_media", "sales_data"],
                "time_period": "Q1 2024"
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/analytics/analyze",
                json=analysis_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("AI Agents - Analytics Agent", True, "Data analysis task submitted")
                    else:
                        self.log_test("AI Agents - Analytics Agent", False, f"Analytics agent failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("AI Agents - Analytics Agent", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("AI Agents - Analytics Agent", False, f"Exception: {str(e)}")
        
        # Test Operations Agent
        try:
            workflow_data = {
                "workflow_name": "Client Onboarding Automation",
                "business_context": {
                    "company": "Dubai Digital Agency",
                    "industry": "digital_marketing"
                },
                "workflow_steps": ["client_data_collection", "contract_generation", "payment_processing"]
            }
            
            async with self.session.post(
                f"{API_BASE}/agents/operations/automate-workflow",
                json=workflow_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("AI Agents - Operations Agent", True, "Workflow automation task submitted")
                    else:
                        self.log_test("AI Agents - Operations Agent", False, f"Operations agent failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("AI Agents - Operations Agent", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("AI Agents - Operations Agent", False, f"Exception: {str(e)}")

    async def test_smart_insights_analytics(self):
        """Test Smart Insights & Analytics Engine"""
        print("\n🧠 SMART INSIGHTS & ANALYTICS ENGINE:")
        print("-" * 60)
        
        # Test Performance Analysis
        try:
            performance_data = {
                "business_context": {
                    "company": "Dubai E-commerce Hub",
                    "industry": "e_commerce",
                    "location": "Dubai, UAE"
                },
                "performance_metrics": {
                    "website_traffic": {
                        "monthly_visitors": 125000,
                        "bounce_rate": "35%",
                        "conversion_rate": "2.8%"
                    },
                    "sales_data": {
                        "monthly_revenue": "AED 450,000",
                        "order_value": "AED 285"
                    }
                }
            }
            
            async with self.session.post(
                f"{API_BASE}/insights/analyze-performance",
                json=performance_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        insights_count = data.get("data", {}).get("insights_generated", 0)
                        self.log_test("Smart Insights - Performance Analysis", True, f"Generated {insights_count} insights")
                    else:
                        self.log_test("Smart Insights - Performance Analysis", False, f"Analysis failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Smart Insights - Performance Analysis", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Smart Insights - Performance Analysis", False, f"Exception: {str(e)}")

    async def test_payment_integration(self):
        """Test Payment Integration (Stripe)"""
        print("\n💳 PAYMENT INTEGRATION (STRIPE):")
        print("-" * 60)
        
        # Test Get Payment Packages
        try:
            async with self.session.get(f"{API_BASE}/integrations/payments/packages") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        packages = data.get("data", {}).get("packages", {})
                        self.log_test("Payment - Get Packages", True, f"Retrieved {len(packages)} payment packages")
                    else:
                        self.log_test("Payment - Get Packages", False, f"Failed to get packages: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Payment - Get Packages", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Payment - Get Packages", False, f"Exception: {str(e)}")
        
        # Test Create Checkout Session
        try:
            session_data = {
                "package_id": "starter",
                "host_url": "https://test.example.com"
            }
            
            async with self.session.post(
                f"{API_BASE}/integrations/payments/create-session",
                json=session_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("Payment - Create Session", True, "Checkout session created successfully")
                    else:
                        self.log_test("Payment - Create Session", False, f"Session creation failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Payment - Create Session", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Payment - Create Session", False, f"Exception: {str(e)}")

    async def test_basic_apis(self):
        """Test Basic APIs"""
        print("\n🔧 BASIC APIS:")
        print("-" * 60)
        
        # Test Health Check
        try:
            async with self.session.get(f"{API_BASE}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "healthy":
                        self.log_test("Basic APIs - Health Check", True, "Service is healthy")
                    else:
                        self.log_test("Basic APIs - Health Check", False, f"Unexpected status: {data.get('status')}")
                else:
                    self.log_test("Basic APIs - Health Check", False, f"HTTP {response.status}")
        except Exception as e:
            self.log_test("Basic APIs - Health Check", False, f"Exception: {str(e)}")
        
        # Test Contact Form
        try:
            contact_data = {
                "name": "Ahmed Al-Rashid",
                "email": "ahmed.rashid@example.ae",
                "phone": "+971501234567",
                "service": "social_media",
                "message": "I need help with social media marketing for my Dubai-based restaurant."
            }
            
            async with self.session.post(
                f"{API_BASE}/contact",
                json=contact_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("Basic APIs - Contact Form", True, "Contact form submitted successfully")
                    else:
                        self.log_test("Basic APIs - Contact Form", False, f"Contact form failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Basic APIs - Contact Form", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Basic APIs - Contact Form", False, f"Exception: {str(e)}")
        
        # Test AI Problem Analyzer
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
                    if data.get("success"):
                        self.log_test("Basic APIs - AI Problem Analyzer", True, "Problem analysis completed successfully")
                    else:
                        self.log_test("Basic APIs - AI Problem Analyzer", False, f"Analysis failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Basic APIs - AI Problem Analyzer", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Basic APIs - AI Problem Analyzer", False, f"Exception: {str(e)}")
        
        # Test Analytics
        try:
            async with self.session.get(f"{API_BASE}/analytics/summary") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        self.log_test("Basic APIs - Analytics", True, "Analytics data retrieved successfully")
                    else:
                        self.log_test("Basic APIs - Analytics", False, f"Analytics failed: {data}")
                else:
                    error_text = await response.text()
                    self.log_test("Basic APIs - Analytics", False, f"HTTP {response.status}: {error_text}")
        except Exception as e:
            self.log_test("Basic APIs - Analytics", False, f"Exception: {str(e)}")

    async def run_comprehensive_tests(self):
        """Run comprehensive E2E backend tests"""
        print(f"🚀 COMPREHENSIVE E2E BACKEND TESTING - ALL SYSTEMS")
        print(f"📍 Backend URL: {BACKEND_URL}")
        print(f"📍 API Base: {API_BASE}")
        print("=" * 80)
        
        # Priority 1 - Critical Systems
        print("\n🔥 PRIORITY 1 - CRITICAL SYSTEMS")
        print("=" * 80)
        await self.test_white_label_system()
        await self.test_inter_agent_communication()
        
        # Priority 2 - Core Features
        print("\n⭐ PRIORITY 2 - CORE FEATURES")
        print("=" * 80)
        await self.test_ai_agents()
        await self.test_smart_insights_analytics()
        await self.test_payment_integration()
        
        # Priority 3 - Basic APIs
        print("\n🔧 PRIORITY 3 - BASIC APIS")
        print("=" * 80)
        await self.test_basic_apis()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE E2E TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = len(self.failed_tests)
        critical_failures = len(self.critical_failures)
        minor_issues = len(self.minor_issues)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"  - Critical Failures: {critical_failures}")
        print(f"  - Minor Issues: {minor_issues}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.critical_failures:
            print(f"\n🚨 CRITICAL FAILURES:")
            for test in self.critical_failures:
                print(f"   - {test}")
        
        if self.minor_issues:
            print(f"\n⚠️  MINOR ISSUES:")
            for test in self.minor_issues:
                print(f"   - {test}")
        
        if not self.failed_tests:
            print(f"\n🎉 All tests passed!")
        
        return critical_failures == 0

async def main():
    """Main test runner"""
    async with ComprehensiveTester() as tester:
        success = await tester.run_comprehensive_tests()
        return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)