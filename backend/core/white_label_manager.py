"""
White Label Manager - FIXED VERSION with proper async handling
Multi-tenancy and branding customization system
Enables resellers and partners to customize the platform with their own branding
"""
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
from pathlib import Path

from database import get_database
from models import StandardResponse

logger = logging.getLogger(__name__)

class TenantConfig:
    """Configuration for a white-label tenant"""
    
    def __init__(self, tenant_data: Dict[str, Any]):
        self.tenant_id = tenant_data.get('tenant_id', str(uuid.uuid4()))
        self.name = tenant_data.get('name', '')
        self.domain = tenant_data.get('domain', '')
        self.subdomain = tenant_data.get('subdomain', '')
        
        # Branding configuration
        self.branding = tenant_data.get('branding', {})
        self.logo_url = self.branding.get('logo_url', '')
        self.primary_color = self.branding.get('primary_color', '#00FF41')
        self.secondary_color = self.branding.get('secondary_color', '#00FFFF')
        self.background_color = self.branding.get('background_color', '#000000')
        self.font_family = self.branding.get('font_family', 'Inter')
        
        # Platform configuration
        self.platform_name = tenant_data.get('platform_name', 'AI Business Platform')
        self.tagline = tenant_data.get('tagline', 'AI-Powered Business Automation')
        self.description = tenant_data.get('description', 'Complete AI automation suite')
        
        # Feature configuration
        self.enabled_features = tenant_data.get('enabled_features', [])
        self.agent_limits = tenant_data.get('agent_limits', {'max_agents': 5})
        self.api_limits = tenant_data.get('api_limits', {'requests_per_day': 10000})
        
        # Contact & support
        self.contact_info = tenant_data.get('contact_info', {})
        self.support_email = self.contact_info.get('support_email', '')
        self.sales_email = self.contact_info.get('sales_email', '')
        self.phone = self.contact_info.get('phone', '')
        self.address = self.contact_info.get('address', '')
        
        # Subscription & billing
        self.subscription_tier = tenant_data.get('subscription_tier', 'starter')
        self.billing_info = tenant_data.get('billing_info', {})
        
        # Metadata
        self.created_at = tenant_data.get('created_at', datetime.now(timezone.utc).isoformat())
        self.updated_at = tenant_data.get('updated_at', datetime.now(timezone.utc).isoformat())
        self.status = tenant_data.get('status', 'active')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'tenant_id': self.tenant_id,
            'name': self.name,
            'domain': self.domain,
            'subdomain': self.subdomain,
            'branding': self.branding,
            'platform_name': self.platform_name,
            'tagline': self.tagline,
            'description': self.description,
            'enabled_features': self.enabled_features,
            'agent_limits': self.agent_limits,
            'api_limits': self.api_limits,
            'contact_info': self.contact_info,
            'subscription_tier': self.subscription_tier,
            'billing_info': self.billing_info,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status
        }

class WhiteLabelManager:
    """
    Manages white-label configurations and multi-tenancy
    FIXED VERSION with proper async database operations
    """
    
    def __init__(self):
        self.tenants: Dict[str, TenantConfig] = {}
        self.domain_mappings: Dict[str, str] = {}  # domain -> tenant_id
        
        # Subscription tiers and limits
        self.subscription_tiers = {
            "starter": {
                "max_agents": 3,
                "max_users": 10,
                "api_requests_per_day": 5000,
                "features": ["basic_agents", "templates", "support"],
                "price": 99,  # USD per month
                "plugins_limit": 5
            },
            "professional": {
                "max_agents": 10,
                "max_users": 50,
                "api_requests_per_day": 25000,
                "features": ["all_agents", "templates", "plugins", "white_label", "priority_support"],
                "price": 299,
                "plugins_limit": 20
            },
            "enterprise": {
                "max_agents": -1,  # unlimited
                "max_users": -1,   # unlimited  
                "api_requests_per_day": 100000,
                "features": ["all_agents", "templates", "plugins", "white_label", "custom_development", "dedicated_support"],
                "price": 999,
                "plugins_limit": -1  # unlimited
            }
        }
        
        logger.info("White Label Manager initialized (FIXED VERSION)")
    
    async def create_tenant(self, tenant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new white-label tenant - FIXED VERSION"""
        try:
            tenant_config = TenantConfig(tenant_data)
            
            # Validate domain/subdomain uniqueness
            domain = tenant_config.domain or f"{tenant_config.subdomain}.nowhere.digital"
            
            # Check domain uniqueness in database
            db = get_database()
            existing_tenant = await db.tenants.find_one({"config.domain": domain})
            if existing_tenant:
                logger.warning(f"Domain already exists: {domain}")
                return {"error": "Domain already exists"}
            
            # Store tenant configuration in memory
            self.tenants[tenant_config.tenant_id] = tenant_config
            self.domain_mappings[domain] = tenant_config.tenant_id
            
            # Save to database - FIXED: Properly handle async insert_one
            try:
                result = await db.tenants.insert_one({
                    "tenant_id": tenant_config.tenant_id,
                    "config": tenant_config.to_dict(),
                    "created_at": tenant_config.created_at
                })
                logger.info(f"Tenant saved to database with ID: {result.inserted_id}")
            except Exception as db_error:
                logger.error(f"Database insert error: {db_error}")
                # Rollback in-memory changes
                del self.tenants[tenant_config.tenant_id]
                del self.domain_mappings[domain]
                return {"error": f"Database error: {str(db_error)}"}
            
            # Generate deployment package
            deployment_package = await self._generate_deployment_package(tenant_config)
            
            logger.info(f"Created white-label tenant: {tenant_config.tenant_id}")
            
            return {
                "tenant_id": tenant_config.tenant_id,
                "domain": domain,
                "deployment_package": deployment_package,
                "setup_instructions": self._get_setup_instructions(tenant_config),
                "estimated_setup_time": "2-4 hours"
            }
            
        except Exception as e:
            logger.error(f"Error creating tenant: {e}", exc_info=True)
            return {"error": f"Failed to create tenant: {str(e)}"}
    
    async def get_tenant_config(self, tenant_id: str = None, domain: str = None) -> Optional[TenantConfig]:
        """Get tenant configuration by ID or domain - FIXED VERSION"""
        try:
            if domain and domain in self.domain_mappings:
                tenant_id = self.domain_mappings[domain]
            
            if tenant_id in self.tenants:
                return self.tenants[tenant_id]
            
            # Try loading from database - FIXED: Properly handle async find_one
            if tenant_id:
                db = get_database()
                tenant_doc = await db.tenants.find_one({"tenant_id": tenant_id})
                if tenant_doc:
                    config = TenantConfig(tenant_doc.get('config', {}))
                    self.tenants[tenant_id] = config
                    # Update domain mapping
                    if config.domain:
                        self.domain_mappings[config.domain] = tenant_id
                    return config
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting tenant config: {e}", exc_info=True)
            return None
    
    async def update_tenant(self, tenant_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update tenant configuration - FIXED VERSION"""
        try:
            tenant = await self.get_tenant_config(tenant_id)
            if not tenant:
                return {"error": "Tenant not found"}
            
            # Update configuration
            current_config = tenant.to_dict()
            current_config.update(updates)
            current_config["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            # Create updated tenant config
            updated_tenant = TenantConfig(current_config)
            self.tenants[tenant_id] = updated_tenant
            
            # Update database - FIXED: Properly handle async update_one
            db = get_database()
            result = await db.tenants.update_one(
                {"tenant_id": tenant_id},
                {"$set": {"config": current_config, "updated_at": current_config["updated_at"]}}
            )
            
            if result.matched_count == 0:
                return {"error": "Tenant not found in database"}
            
            logger.info(f"Updated tenant: {tenant_id}")
            return {"success": True, "message": "Tenant updated successfully"}
            
        except Exception as e:
            logger.error(f"Error updating tenant: {e}", exc_info=True)
            return {"error": f"Failed to update tenant: {str(e)}"}
    
    async def get_tenant_branding(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant-specific branding configuration - FIXED VERSION"""
        try:
            tenant = await self.get_tenant_config(tenant_id)
            if not tenant:
                logger.warning(f"Tenant not found, returning default branding: {tenant_id}")
                return self._get_default_branding()
            
            return {
                "platform_name": tenant.platform_name,
                "tagline": tenant.tagline,
                "logo_url": tenant.logo_url,
                "colors": {
                    "primary": tenant.primary_color,
                    "secondary": tenant.secondary_color,
                    "background": tenant.background_color
                },
                "font_family": tenant.font_family,
                "contact_info": {
                    "support_email": tenant.support_email,
                    "sales_email": tenant.sales_email,
                    "phone": tenant.phone,
                    "address": tenant.address
                }
            }
        except Exception as e:
            logger.error(f"Error getting tenant branding: {e}", exc_info=True)
            return self._get_default_branding()
    
    async def get_tenant_features(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant-specific feature configuration"""
        tenant = await self.get_tenant_config(tenant_id)
        if not tenant:
            return {"features": [], "limits": {}}
        
        tier_config = self.subscription_tiers.get(tenant.subscription_tier, self.subscription_tiers["starter"])
        
        return {
            "enabled_features": tenant.enabled_features,
            "subscription_tier": tenant.subscription_tier,
            "limits": {
                "max_agents": tier_config["max_agents"],
                "max_users": tier_config["max_users"],
                "api_requests_per_day": tier_config["api_requests_per_day"],
                "plugins_limit": tier_config["plugins_limit"]
            },
            "tier_features": tier_config["features"]
        }
    
    async def validate_tenant_access(self, tenant_id: str, feature: str) -> bool:
        """Validate if tenant has access to a specific feature"""
        tenant = await self.get_tenant_config(tenant_id)
        if not tenant:
            return False
        
        tier_config = self.subscription_tiers.get(tenant.subscription_tier, self.subscription_tiers["starter"])
        return feature in tier_config["features"] or feature in tenant.enabled_features
    
    async def get_all_tenants(self, status: str = None) -> List[Dict[str, Any]]:
        """Get list of all tenants - FIXED VERSION"""
        try:
            db = get_database()
            query = {}
            if status:
                query["config.status"] = status
            
            tenants = []
            # FIXED: Properly handle async cursor iteration
            cursor = db.tenants.find(query)
            async for tenant_doc in cursor:
                config = tenant_doc.get('config', {})
                tenants.append({
                    "tenant_id": config.get('tenant_id'),
                    "name": config.get('name'),
                    "domain": config.get('domain'),
                    "subscription_tier": config.get('subscription_tier', 'starter'),
                    "status": config.get('status', 'active'),
                    "created_at": config.get('created_at')
                })
            
            logger.info(f"Retrieved {len(tenants)} tenants")
            return tenants
            
        except Exception as e:
            logger.error(f"Error getting tenants: {e}", exc_info=True)
            return []
    
    async def create_reseller_package(self, reseller_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a reseller package with custom branding and features - FIXED VERSION"""
        try:
            # Generate domain if not provided
            domain = reseller_data.get('domain', '')
            if not domain:
                # Generate domain from company name or use UUID
                company_name = reseller_data.get('company_name', reseller_data.get('reseller_name', ''))
                if company_name:
                    domain = f"{company_name.lower().replace(' ', '-').replace('_', '-')}.nowheredigital.ae"
                else:
                    domain = f"reseller-{uuid.uuid4().hex[:8]}.nowheredigital.ae"
            
            db = get_database()
            existing = await db.tenants.find_one({"config.domain": domain})
            if existing:
                # If domain exists, append random suffix
                domain = f"{domain.split('.')[0]}-{uuid.uuid4().hex[:4]}.nowheredigital.ae"
            
            # Create base tenant configuration for reseller
            tenant_data = {
                "name": reseller_data.get('company_name', ''),
                "domain": domain,
                "platform_name": reseller_data.get('platform_name', 'AI Business Platform'),
                "tagline": reseller_data.get('tagline', 'AI-Powered Business Automation'),
                "branding": reseller_data.get('branding', {}),
                "contact_info": reseller_data.get('contact_info', {}),
                "subscription_tier": "enterprise",  # Resellers get enterprise features
                "enabled_features": [
                    "white_label", "reseller_dashboard", "multi_tenant", 
                    "custom_branding", "partner_api", "revenue_sharing"
                ]
            }
            
            tenant_result = await self.create_tenant(tenant_data)
            if "error" in tenant_result:
                return tenant_result
            
            # Generate reseller-specific resources
            reseller_package = {
                "tenant_id": tenant_result["tenant_id"],
                "reseller_dashboard_url": f"https://{domain}/reseller",
                "api_credentials": {
                    "api_key": f"pk_reseller_{tenant_result['tenant_id'][:8]}",
                    "secret_key": f"sk_reseller_{uuid.uuid4().hex[:16]}"
                },
                "documentation": {
                    "setup_guide": "Complete reseller setup documentation",
                    "api_docs": "Partner API documentation",
                    "branding_guide": "White-label branding guidelines"
                },
                "revenue_sharing": {
                    "commission_rate": reseller_data.get('commission_rate', 20),  # 20% default
                    "payment_terms": "Monthly via bank transfer",
                    "minimum_payout": 1000  # USD
                }
            }
            
            return {
                "success": True,
                "reseller_package": reseller_package,
                "setup_time": "4-8 hours",
                "go_live_estimate": "2-3 business days"
            }
            
        except Exception as e:
            logger.error(f"Error creating reseller package: {e}", exc_info=True)
            return {"error": f"Failed to create reseller package: {str(e)}"}
    
    def _get_default_branding(self) -> Dict[str, Any]:
        """Get default NOWHERE.AI branding"""
        return {
            "platform_name": "NOWHERE.AI",
            "tagline": "AI-Powered Business Operating System",
            "logo_url": "/assets/logo-matrix.svg",
            "colors": {
                "primary": "#00FF41",
                "secondary": "#00FFFF", 
                "background": "#000000"
            },
            "font_family": "Inter",
            "contact_info": {
                "support_email": "support@nowhere.ai",
                "sales_email": "sales@nowhere.ai",
                "phone": "+971567148469",
                "address": "Boulevard Tower, Downtown Dubai"
            }
        }
    
    async def _generate_deployment_package(self, tenant: TenantConfig) -> Dict[str, Any]:
        """Generate deployment package for tenant"""
        return {
            "docker_compose": "Custom Docker configuration for tenant deployment",
            "environment_variables": {
                "TENANT_ID": tenant.tenant_id,
                "PLATFORM_NAME": tenant.platform_name,
                "PRIMARY_COLOR": tenant.primary_color,
                "DOMAIN": tenant.domain
            },
            "kubernetes_manifests": "Kubernetes deployment manifests",
            "nginx_config": "Custom Nginx configuration for domain routing",
            "database_setup": "Tenant-specific database configuration"
        }
    
    def _get_setup_instructions(self, tenant: TenantConfig) -> List[str]:
        """Get setup instructions for tenant"""
        return [
            "1. Configure DNS to point domain to platform servers",
            "2. Deploy Docker containers with provided configuration",
            "3. Run database migration scripts",
            "4. Upload custom branding assets",
            "5. Configure agent settings and integrations",
            "6. Test all functionality and go live"
        ]

# Global white label manager instance
white_label_manager = WhiteLabelManager()
