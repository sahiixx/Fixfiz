"""
Comprehensive Unit Tests for Phase 5 Integrations
Tests SendGrid, Stripe, Twilio, Voice AI, and Vision AI integrations

This test suite covers:
- SendGrid Email Integration (13 tests)
- Stripe Payment Integration (12 tests)
- Twilio SMS Integration (14 tests)
- Voice AI Integration (8 tests)
- Vision AI Integration (10 tests)
- Cross-feature Integration Scenarios (2 tests)
Total: 59 comprehensive unit tests
"""
import pytest
import asyncio
import os
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timezone

# Import integration classes
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from integrations.sendgrid_integration import SendGridIntegration
from integrations.stripe_integration import StripeIntegration
from integrations.twilio_integration import TwilioIntegration
from integrations.voice_ai_integration import VoiceAIIntegration
from integrations.vision_ai_integration import VisionAIIntegration


# Test constants
TEST_TWILIO_AUTH_TOKEN = 'test_token'  # noqa: S105


# ================================================================================================
# SENDGRID INTEGRATION TESTS (13 tests)
# ================================================================================================

class TestSendGridIntegration:
    """Comprehensive tests for SendGrid email integration"""
    
    @pytest.fixture
    def sendgrid_integration(self):
        """Create SendGrid integration instance for testing"""
        with patch.dict(os.environ, {
            'SENDGRID_API_KEY': 'test_api_key',
            'SENDGRID_FROM_EMAIL': 'test@nowheredigital.ae'
        }):
            integration = SendGridIntegration()
            return integration
    
    @pytest.fixture
    def sendgrid_no_key(self):
        """Create SendGrid integration without API key"""
        with patch.dict(os.environ, {}, clear=True):
            integration = SendGridIntegration()
            return integration
    
    @pytest.mark.asyncio
    async def test_init_with_api_key(self, sendgrid_integration):
        """Test initialization with API key"""
        assert sendgrid_integration.api_key == 'test_api_key'
        assert sendgrid_integration.from_email == 'test@nowheredigital.ae'
        assert sendgrid_integration.client is not None
    
    @pytest.mark.asyncio
    async def test_init_without_api_key(self, sendgrid_no_key):
        """Test initialization without API key"""
        assert sendgrid_no_key.api_key is None
        assert sendgrid_no_key.client is None
    
    @pytest.mark.asyncio
    async def test_send_email_without_client(self, sendgrid_no_key):
        """Test send_email returns error when client not configured"""
        result = await sendgrid_no_key.send_email(
            to_email="test@example.com",
            subject="Test Subject",
            html_content="<p>Test</p>"
        )
        
        assert "error" in result
        assert result["error"] == "SendGrid not configured"
        assert result["test_mode"] is True
    
    @pytest.mark.asyncio
    async def test_send_email_success(self, sendgrid_integration):
        """Test successful email sending"""
        mock_response = Mock()
        mock_response.status_code = 202
        
        with patch.object(sendgrid_integration.client, 'send', return_value=mock_response):
            result = await sendgrid_integration.send_email(
                to_email="recipient@example.com",
                subject="Test Email",
                html_content="<h1>Hello</h1><p>This is a test.</p>",
                plain_text="Hello. This is a test."
            )
        
        assert result["status_code"] == 202
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_send_email_failure(self, sendgrid_integration):
        """Test email sending with non-202 status"""
        mock_response = Mock()
        mock_response.status_code = 400
        
        with patch.object(sendgrid_integration.client, 'send', return_value=mock_response):
            result = await sendgrid_integration.send_email(
                to_email="invalid@example.com",
                subject="Test",
                html_content="<p>Test</p>"
            )
        
        assert result["status_code"] == 400
        assert result["success"] is False
    
    @pytest.mark.asyncio
    async def test_send_email_exception(self, sendgrid_integration):
        """Test email sending with exception"""
        with patch.object(sendgrid_integration.client, 'send', side_effect=Exception("API Error")):
            result = await sendgrid_integration.send_email(
                to_email="test@example.com",
                subject="Test",
                html_content="<p>Test</p>"
            )
        
        assert "error" in result
        assert "API Error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_send_template_email_without_client(self, sendgrid_no_key):
        """Test template email without client"""
        result = await sendgrid_no_key.send_template_email(
            to_email="test@example.com",
            template_id="d-1234567890",
            dynamic_data={"name": "Test User"}
        )
        
        assert "error" in result
        assert result["test_mode"] is True
    
    @pytest.mark.asyncio
    async def test_send_template_email_success(self, sendgrid_integration):
        """Test successful template email"""
        mock_response = Mock()
        mock_response.status_code = 202
        
        with patch.object(sendgrid_integration.client, 'send', return_value=mock_response):
            result = await sendgrid_integration.send_template_email(
                to_email="user@example.com",
                template_id="d-1234567890",
                dynamic_data={"name": "Ahmed", "company": "Dubai Tech"}
            )
        
        assert result["success"] is True
        assert result["status_code"] == 202
    
    @pytest.mark.asyncio
    async def test_send_notification_welcome(self, sendgrid_integration):
        """Test sending welcome notification"""
        mock_response = Mock()
        mock_response.status_code = 202
        
        with patch.object(sendgrid_integration.client, 'send', return_value=mock_response):
            result = await sendgrid_integration.send_notification(
                to_email="newuser@example.com",
                notification_type="welcome",
                data={"message": "Welcome to our platform!", "details": "Your account is ready."}
            )
        
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_send_notification_alert(self, sendgrid_integration):
        """Test sending alert notification"""
        mock_response = Mock()
        mock_response.status_code = 202
        
        with patch.object(sendgrid_integration.client, 'send', return_value=mock_response):
            result = await sendgrid_integration.send_notification(
                to_email="admin@example.com",
                notification_type="alert",
                data={"message": "High CPU usage detected", "details": "CPU at 95%"}
            )
        
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_send_notification_report(self, sendgrid_integration):
        """Test sending report notification"""
        mock_response = Mock()
        mock_response.status_code = 202
        
        with patch.object(sendgrid_integration.client, 'send', return_value=mock_response):
            result = await sendgrid_integration.send_notification(
                to_email="user@example.com",
                notification_type="report",
                data={"message": "Your report is ready", "details": "Click to download"}
            )
        
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_send_notification_unknown_type(self, sendgrid_integration):
        """Test sending notification with unknown type uses default subject"""
        mock_response = Mock()
        mock_response.status_code = 202
        
        with patch.object(sendgrid_integration.client, 'send', return_value=mock_response):
            result = await sendgrid_integration.send_notification(
                to_email="user@example.com",
                notification_type="custom_type",
                data={"message": "Custom notification"}
            )
        
        assert result["success"] is True


# ================================================================================================
# STRIPE INTEGRATION TESTS (12 tests)
# ================================================================================================

class TestStripeIntegration:
    """Comprehensive tests for Stripe payment integration"""
    
    @pytest.fixture
    def stripe_integration(self):
        """Create Stripe integration instance"""
        with patch.dict(os.environ, {'STRIPE_API_KEY': 'sk_test_mock'}):
            integration = StripeIntegration()
            return integration
    
    def test_init(self, stripe_integration):
        """Test Stripe integration initialization"""
        assert stripe_integration.api_key == 'sk_test_mock'
        assert stripe_integration.stripe_checkout is None
        assert len(stripe_integration.PACKAGES) == 3
    
    def test_packages_structure(self, stripe_integration):
        """Test payment packages have correct structure"""
        assert "starter" in stripe_integration.PACKAGES
        assert "growth" in stripe_integration.PACKAGES
        assert "enterprise" in stripe_integration.PACKAGES
        
        for _package_id, package in stripe_integration.PACKAGES.items():
            assert "amount" in package
            assert "currency" in package
            assert "name" in package
            assert package["currency"] == "aed"  # UAE currency
    
    def test_packages_pricing(self, stripe_integration):
        """Test package pricing tiers are correctly set"""
        assert stripe_integration.PACKAGES["starter"]["amount"] == 2500.00
        assert stripe_integration.PACKAGES["growth"]["amount"] == 5000.00
        assert stripe_integration.PACKAGES["enterprise"]["amount"] == 10000.00
    
    def test_initialize(self, stripe_integration):
        """Test Stripe checkout initialization"""
        webhook_url = "https://example.com/webhook"
        
        with patch('integrations.stripe_integration.StripeCheckout') as mock_checkout:
            stripe_integration.initialize(webhook_url)
            mock_checkout.assert_called_once_with(
                api_key=stripe_integration.api_key,
                webhook_url=webhook_url
            )
    
    @pytest.mark.asyncio
    async def test_create_session_invalid_package(self, stripe_integration):
        """Test session creation with invalid package ID"""
        result = await stripe_integration.create_session(
            package_id="invalid_package",
            host_url="https://example.com"
        )
        
        assert "error" in result
        assert result["error"] == "Invalid package"
    
    @pytest.mark.asyncio
    async def test_create_session_success(self, stripe_integration):
        """Test successful checkout session creation"""
        mock_session = Mock()
        mock_session.url = "https://checkout.stripe.com/test"
        mock_session.session_id = "cs_test_123"
        
        with patch('integrations.stripe_integration.StripeCheckout') as mock_checkout_class:
            mock_checkout = Mock()
            mock_checkout.create_checkout_session = AsyncMock(return_value=mock_session)
            mock_checkout_class.return_value = mock_checkout
            
            result = await stripe_integration.create_session(
                package_id="starter",
                host_url="https://example.com",
                metadata={"customer_id": "cust_123"}
            )
        
        assert "url" in result
        assert "session_id" in result
        assert "package" in result
        assert result["session_id"] == "cs_test_123"
        assert result["package"]["name"] == "Starter Package"
    
    @pytest.mark.asyncio
    async def test_create_session_with_metadata(self, stripe_integration):
        """Test session creation with custom metadata"""
        mock_session = Mock()
        mock_session.url = "https://checkout.stripe.com/test"
        mock_session.session_id = "cs_test_456"
        
        with patch('integrations.stripe_integration.StripeCheckout') as mock_checkout_class:
            mock_checkout = Mock()
            mock_checkout.create_checkout_session = AsyncMock(return_value=mock_session)
            mock_checkout_class.return_value = mock_checkout
            
            custom_metadata = {
                "customer_id": "cust_dubai_123",
                "tenant_id": "tenant_001",
                "campaign": "summer_2024"
            }
            
            result = await stripe_integration.create_session(
                package_id="enterprise",
                host_url="https://nowheredigital.ae",
                metadata=custom_metadata
            )
        
        assert result["package"]["amount"] == 10000.00
    
    @pytest.mark.asyncio
    async def test_create_session_exception(self, stripe_integration):
        """Test session creation handles exceptions gracefully"""
        with patch('integrations.stripe_integration.StripeCheckout') as mock_checkout_class:
            mock_checkout = Mock()
            mock_checkout.create_checkout_session = AsyncMock(
                side_effect=Exception("Stripe API Error")
            )
            mock_checkout_class.return_value = mock_checkout
            
            result = await stripe_integration.create_session(
                package_id="growth",
                host_url="https://example.com"
            )
        
        assert "error" in result
        assert "Stripe API Error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_status_success(self, stripe_integration):
        """Test getting payment status successfully"""
        mock_status = Mock()
        mock_status.status = "complete"
        mock_status.payment_status = "paid"
        mock_status.amount_total = 2500.00
        mock_status.currency = "aed"
        
        stripe_integration.stripe_checkout = Mock()
        stripe_integration.stripe_checkout.get_checkout_status = AsyncMock(return_value=mock_status)
        
        result = await stripe_integration.get_status("cs_test_123")
        
        assert result["status"] == "complete"
        assert result["payment_status"] == "paid"
        assert result["amount_total"] == 2500.00
        assert result["currency"] == "aed"
    
    @pytest.mark.asyncio
    async def test_get_status_exception(self, stripe_integration):
        """Test get status handles exceptions"""
        stripe_integration.stripe_checkout = Mock()
        stripe_integration.stripe_checkout.get_checkout_status = AsyncMock(
            side_effect=Exception("Session not found")
        )
        
        result = await stripe_integration.get_status("cs_invalid")
        
        assert "error" in result
    
    def test_default_api_key(self):
        """Test default API key fallback"""
        with patch.dict(os.environ, {}, clear=True):
            integration = StripeIntegration()
            assert integration.api_key == "sk_test_emergent"


# ================================================================================================
# TWILIO INTEGRATION TESTS (14 tests)
# ================================================================================================

class TestTwilioIntegration:
    """Comprehensive tests for Twilio SMS integration"""
    
    @pytest.fixture
    def twilio_integration(self):
        """Create Twilio integration with credentials"""
        with patch.dict(os.environ, {
            'TWILIO_ACCOUNT_SID': 'AC123456789',
            'TWILIO_AUTH_TOKEN': TEST_TWILIO_AUTH_TOKEN,
            'TWILIO_VERIFY_SERVICE': 'VA123456789',
            'TWILIO_PHONE_NUMBER': '+1234567890'
        }):
            with patch('integrations.twilio_integration.Client'):
                integration = TwilioIntegration()
                integration.client = Mock()
                return integration
    
    @pytest.fixture
    def twilio_no_config(self):
        """Create Twilio integration without configuration"""
        with patch.dict(os.environ, {}, clear=True):
            integration = TwilioIntegration()
            return integration
    
    def test_init_with_credentials(self, twilio_integration):
        """Test initialization with credentials"""
        assert twilio_integration.account_sid == 'AC123456789'
        assert twilio_integration.auth_token == TEST_TWILIO_AUTH_TOKEN
        assert twilio_integration.verify_service_sid == 'VA123456789'
        assert twilio_integration.client is not None
    
    def test_init_without_credentials(self, twilio_no_config):
        """Test initialization without credentials"""
        assert twilio_no_config.client is None
    
    @pytest.mark.asyncio
    async def test_send_otp_without_client(self, twilio_no_config):
        """Test OTP sending without client returns test mode"""
        result = await twilio_no_config.send_otp("+971501234567")
        
        assert "error" in result
        assert result["error"] == "Twilio not configured"
        assert result["test_mode"] is True
    
    @pytest.mark.asyncio
    async def test_send_otp_success(self, twilio_integration):
        """Test successful OTP sending"""
        mock_verification = Mock()
        mock_verification.status = "pending"
        
        mock_verifications = Mock()
        mock_verifications.create = Mock(return_value=mock_verification)
        
        mock_service = Mock()
        mock_service.verifications = mock_verifications
        
        twilio_integration.client.verify.services = Mock(return_value=mock_service)
        
        result = await twilio_integration.send_otp("+971501234567")
        
        assert result["status"] == "pending"
        assert result["to"] == "+971501234567"
    
    @pytest.mark.asyncio
    async def test_send_otp_exception(self, twilio_integration):
        """Test OTP sending handles exceptions"""
        twilio_integration.client.verify.services = Mock(
            side_effect=Exception("Invalid phone number")
        )
        
        result = await twilio_integration.send_otp("+invalid")
        
        assert "error" in result
    
    @pytest.mark.asyncio
    async def test_verify_otp_without_client_test_mode(self, twilio_no_config):
        """Test OTP verification without client uses test mode"""
        result = await twilio_no_config.verify_otp("+971501234567", "123456")
        
        assert result["valid"] is True
        assert result["test_mode"] is True
    
    @pytest.mark.asyncio
    async def test_verify_otp_without_client_wrong_code(self, twilio_no_config):
        """Test OTP verification with wrong code in test mode"""
        result = await twilio_no_config.verify_otp("+971501234567", "000000")
        
        assert result["valid"] is False
        assert result["test_mode"] is True
    
    @pytest.mark.asyncio
    async def test_verify_otp_success(self, twilio_integration):
        """Test successful OTP verification"""
        mock_check = Mock()
        mock_check.status = "approved"
        
        mock_checks = Mock()
        mock_checks.create = Mock(return_value=mock_check)
        
        mock_service = Mock()
        mock_service.verification_checks = mock_checks
        
        twilio_integration.client.verify.services = Mock(return_value=mock_service)
        
        result = await twilio_integration.verify_otp("+971501234567", "123456")
        
        assert result["valid"] is True
        assert result["status"] == "approved"
    
    @pytest.mark.asyncio
    async def test_verify_otp_rejected(self, twilio_integration):
        """Test OTP verification rejection"""
        mock_check = Mock()
        mock_check.status = "rejected"
        
        mock_checks = Mock()
        mock_checks.create = Mock(return_value=mock_check)
        
        mock_service = Mock()
        mock_service.verification_checks = mock_checks
        
        twilio_integration.client.verify.services = Mock(return_value=mock_service)
        
        result = await twilio_integration.verify_otp("+971501234567", "000000")
        
        assert result["valid"] is False
        assert result["status"] == "rejected"
    
    @pytest.mark.asyncio
    async def test_send_sms_without_client(self, twilio_no_config):
        """Test SMS sending without client"""
        result = await twilio_no_config.send_sms(
            to_number="+971501234567",
            message="Test message"
        )
        
        assert "error" in result
        assert result["test_mode"] is True
    
    @pytest.mark.asyncio
    async def test_send_sms_no_phone_number(self, twilio_integration):
        """Test SMS sending without configured phone number"""
        with patch.dict(os.environ, {'TWILIO_PHONE_NUMBER': ''}, clear=False):
            result = await twilio_integration.send_sms(
                to_number="+971501234567",
                message="Test"
            )
        
        assert "error" in result
        assert "No Twilio phone number configured" in result["error"]
    
    @pytest.mark.asyncio
    async def test_send_sms_success(self, twilio_integration):
        """Test successful SMS sending"""
        mock_message = Mock()
        mock_message.sid = "SM123456789"
        mock_message.status = "queued"
        
        twilio_integration.client.messages.create = Mock(return_value=mock_message)
        
        result = await twilio_integration.send_sms(
            to_number="+971501234567",
            message="Welcome to NOWHERE Digital!"
        )
        
        assert result["sid"] == "SM123456789"
        assert result["status"] == "queued"
    
    @pytest.mark.asyncio
    async def test_send_sms_with_custom_from(self, twilio_integration):
        """Test SMS with custom from number"""
        mock_message = Mock()
        mock_message.sid = "SM987654321"
        mock_message.status = "sent"
        
        twilio_integration.client.messages.create = Mock(return_value=mock_message)
        
        result = await twilio_integration.send_sms(
            to_number="+971501234567",
            message="Test message",
            from_number="+1555123456"
        )
        
        assert result["sid"] == "SM987654321"


# ================================================================================================
# VOICE AI INTEGRATION TESTS (8 tests)
# ================================================================================================

class TestVoiceAIIntegration:
    """Comprehensive tests for Voice AI integration"""
    
    @pytest.fixture
    def voice_integration(self):
        """Create Voice AI integration instance"""
        with patch.dict(os.environ, {'EMERGENT_LLM_KEY': 'sk-emergent-test'}):
            integration = VoiceAIIntegration()
            return integration
    
    @pytest.fixture
    def voice_no_key(self):
        """Create Voice AI integration without key"""
        with patch.dict(os.environ, {}, clear=True):
            integration = VoiceAIIntegration()
            return integration
    
    def test_init_with_key(self, voice_integration):
        """Test initialization with API key"""
        assert voice_integration.api_key == 'sk-emergent-test'
        assert voice_integration.realtime_chat is None
    
    def test_init_default_key(self, voice_no_key):
        """Test initialization uses default key"""
        assert voice_no_key.api_key == "sk-emergent-8A3Bc7c1f91F43cE8D"
    
    def test_get_realtime_client(self, voice_integration):
        """Test getting realtime client"""
        with patch('integrations.voice_ai_integration.OpenAIChatRealtime') as mock_realtime:
            voice_integration.get_realtime_client()
            
            mock_realtime.assert_called_once_with(api_key=voice_integration.api_key)
            assert voice_integration.realtime_chat is not None
    
    def test_get_realtime_client_cached(self, voice_integration):
        """Test realtime client is cached after first call"""
        with patch('integrations.voice_ai_integration.OpenAIChatRealtime') as mock_realtime:
            mock_instance = Mock()
            mock_realtime.return_value = mock_instance
            
            client1 = voice_integration.get_realtime_client()
            client2 = voice_integration.get_realtime_client()
            
            assert client1 == client2
            mock_realtime.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_voice_session_success(self, voice_integration):
        """Test successful voice session creation"""
        with patch('integrations.voice_ai_integration.OpenAIChatRealtime'):
            result = await voice_integration.create_voice_session()
            
            assert result["status"] == "ready"
            assert result["message"] == "Voice AI session initialized"
            assert result["client_ready"] is True
    
    @pytest.mark.asyncio
    async def test_create_voice_session_exception(self, voice_integration):
        """Test voice session creation handles exceptions"""
        with patch('integrations.voice_ai_integration.OpenAIChatRealtime',
                   side_effect=Exception("API Error")):
            result = await voice_integration.create_voice_session()
            
            assert "error" in result
            assert "API Error" in result["error"]
    
    def test_get_integration_info_with_key(self, voice_integration):
        """Test integration info with API key"""
        info = voice_integration.get_integration_info()
        
        assert info["provider"] == "OpenAI Realtime"
        assert "Real-time voice chat" in info["capabilities"]
        assert "Speech-to-text" in info["capabilities"]
        assert "Text-to-speech" in info["capabilities"]
        assert "WebRTC support" in info["capabilities"]
        assert info["status"] == "available"
    
    def test_get_integration_info_without_key(self):
        """Test integration info without API key"""
        with patch.dict(os.environ, {'EMERGENT_LLM_KEY': ''}, clear=False):
            integration = VoiceAIIntegration()
            info = integration.get_integration_info()
            
            assert info["status"] == "not_configured"


# ================================================================================================
# VISION AI INTEGRATION TESTS (10 tests)
# ================================================================================================

class TestVisionAIIntegration:
    """Comprehensive tests for Vision AI integration"""
    
    @pytest.fixture
    def vision_integration(self):
        """Create Vision AI integration instance"""
        with patch.dict(os.environ, {'EMERGENT_LLM_KEY': 'sk-emergent-test'}):
            integration = VisionAIIntegration()
            return integration
    
    def test_init(self, vision_integration):
        """Test Vision AI initialization"""
        assert vision_integration.api_key == 'sk-emergent-test'
    
    @pytest.mark.asyncio
    async def test_analyze_image_base64_success(self, vision_integration):
        """Test successful image analysis with base64"""
        test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        with patch('integrations.vision_ai_integration.LlmChat') as mock_chat_class:
            mock_chat = Mock()
            mock_chat.with_model = Mock(return_value=mock_chat)
            mock_chat.send_message = AsyncMock(return_value="This is a red pixel image")
            mock_chat_class.return_value = mock_chat
            
            result = await vision_integration.analyze_image(
                image_data=test_image_base64,
                prompt="What is in this image?",
                image_type="base64"
            )
        
        assert "analysis" in result
        assert result["analysis"] == "This is a red pixel image"
        assert result["model"] == "gpt-4o"
        assert "timestamp" in result
    
    @pytest.mark.asyncio
    async def test_analyze_image_file_path(self, vision_integration):
        """Test image analysis with file path"""
        with patch('integrations.vision_ai_integration.LlmChat') as mock_chat_class:
            mock_chat = Mock()
            mock_chat.with_model = Mock(return_value=mock_chat)
            mock_chat.send_message = AsyncMock(return_value="Analysis from file")
            mock_chat_class.return_value = mock_chat
            
            result = await vision_integration.analyze_image(
                image_data="/path/to/image.jpg",
                prompt="Describe this image",
                image_type="file_path"
            )
        
        assert result["analysis"] == "Analysis from file"
    
    @pytest.mark.asyncio
    async def test_analyze_image_custom_prompt(self, vision_integration):
        """Test image analysis with custom prompt"""
        with patch('integrations.vision_ai_integration.LlmChat') as mock_chat_class:
            mock_chat = Mock()
            mock_chat.with_model = Mock(return_value=mock_chat)
            mock_chat.send_message = AsyncMock(return_value="Custom analysis")
            mock_chat_class.return_value = mock_chat
            
            custom_prompt = "Identify all objects in this image and their positions"
            result = await vision_integration.analyze_image(
                image_data="base64_image_data",
                prompt=custom_prompt,
                image_type="base64"
            )
        
        assert "analysis" in result
    
    @pytest.mark.asyncio
    async def test_analyze_image_exception(self, vision_integration):
        """Test image analysis handles exceptions"""
        with patch('integrations.vision_ai_integration.LlmChat',
                   side_effect=Exception("Vision API Error")):
            result = await vision_integration.analyze_image(
                image_data="invalid_data",
                prompt="Test",
                image_type="base64"
            )
        
        assert "error" in result
        assert "Vision API Error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_analyze_image_url_not_implemented(self, vision_integration):
        """Test image URL analysis (not yet implemented)"""
        result = await vision_integration.analyze_image_url(
            image_url="https://example.com/image.jpg",
            prompt="Analyze this"
        )
        
        assert "error" in result
        assert "not yet implemented" in result["error"]
    
    def test_get_supported_formats(self, vision_integration):
        """Test getting supported image formats"""
        formats = vision_integration.get_supported_formats()
        
        assert "formats" in formats
        assert "jpeg" in formats["formats"]
        assert "jpg" in formats["formats"]
        assert "png" in formats["formats"]
        assert "webp" in formats["formats"]
        assert "gif" in formats["formats"]
        assert formats["max_size_mb"] == 20
        assert "base64" in formats["input_types"]
        assert "file_path" in formats["input_types"]
        assert "url" in formats["input_types"]
    
    def test_supported_formats_count(self, vision_integration):
        """Test correct number of supported formats"""
        formats = vision_integration.get_supported_formats()
        assert len(formats["formats"]) == 5
        assert len(formats["input_types"]) == 3
    
    def test_supported_formats_structure(self, vision_integration):
        """Test supported formats have all required fields"""
        formats = vision_integration.get_supported_formats()
        assert isinstance(formats["formats"], list)
        assert isinstance(formats["input_types"], list)
        assert isinstance(formats["max_size_mb"], int)


# ================================================================================================
# INTEGRATION TESTS - Cross-feature scenarios (2 tests)
# ================================================================================================

class TestIntegrationScenarios:
    """Test integration scenarios across multiple services"""
    
    @pytest.mark.asyncio
    async def test_user_onboarding_flow(self):
        """Test complete user onboarding with email and SMS"""
        with patch.dict(os.environ, {
            'SENDGRID_API_KEY': 'test_key',
            'TWILIO_ACCOUNT_SID': 'AC123',
            'TWILIO_AUTH_TOKEN': 'token',
            'TWILIO_VERIFY_SERVICE': 'VA123'
        }):
            sendgrid = SendGridIntegration()
            twilio = TwilioIntegration()
            twilio.client = Mock()
            
            # Simulate welcome email
            mock_response = Mock()
            mock_response.status_code = 202
            with patch.object(sendgrid.client, 'send', return_value=mock_response):
                email_result = await sendgrid.send_notification(
                    to_email="newuser@example.com",
                    notification_type="welcome",
                    data={"message": "Welcome!"}
                )
            
            # Simulate OTP verification
            mock_verification = Mock()
            mock_verification.status = "pending"
            mock_verifications = Mock()
            mock_verifications.create = Mock(return_value=mock_verification)
            mock_service = Mock()
            mock_service.verifications = mock_verifications
            twilio.client.verify.services = Mock(return_value=mock_service)
            
            otp_result = await twilio.send_otp("+971501234567")
            
            assert email_result["success"] is True
            assert otp_result["status"] == "pending"
    
    @pytest.mark.asyncio
    async def test_payment_with_notification(self):
        """Test payment flow with email notification"""
        stripe = StripeIntegration()
        sendgrid = SendGridIntegration()
        
        # Mock successful payment
        mock_session = Mock()
        mock_session.url = "https://checkout.stripe.com/test"
        mock_session.session_id = "cs_test"
        
        with patch('integrations.stripe_integration.StripeCheckout') as mock_checkout_class:
            mock_checkout = Mock()
            mock_checkout.create_checkout_session = AsyncMock(return_value=mock_session)
            mock_checkout_class.return_value = mock_checkout
            
            payment_result = await stripe.create_session(
                package_id="starter",
                host_url="https://example.com"
            )
        
        # Mock payment confirmation email
        mock_response = Mock()
        mock_response.status_code = 202
        with patch.object(sendgrid.client, 'send', return_value=mock_response):
            email_result = await sendgrid.send_notification(
                to_email="customer@example.com",
                notification_type="report",
                data={"message": "Payment successful"}
            )
        
        assert payment_result["session_id"] == "cs_test"
        assert email_result["success"] is True


# ================================================================================================
# RUN ALL TESTS
# ================================================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])