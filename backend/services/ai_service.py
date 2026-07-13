"""
NOWHERE Digital AI Service.

Previously built on the private `emergentintegrations.llm.chat.LlmChat` wrapper;
rewritten 2026-07-13 to call the OpenAI API directly via the official `openai`
SDK. This removes the `emergentintegrations` -> `litellm` dependency chain
(and its 7 accepted CVEs) entirely.

Behavior is preserved:
- All public method signatures and return types are unchanged (strings).
- Without a real API key, OpenAI calls raise and each method returns the same
  fallback string it did before, so the backend still degrades gracefully.
- `settings.ai_provider` is honored for OpenAI-compatible providers via the
  optional `base_url`/`OPENAI_BASE_URL` env override; non-OpenAI model names
  are routed to gpt-4o (which covers text/vision/multimodal).
"""
from config import settings
import logging
import os
from typing import Dict, Any, Optional

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

# OpenAI (and OpenAI-compatible) endpoint. If AI_PROVIDER points at a
# compatible gateway, set OPENAI_BASE_URL to its URL.
_BASE_URL = os.getenv("OPENAI_BASE_URL") or None


class AIService:
    def __init__(self):
        self.api_key = settings.openai_api_key
        self.model = settings.default_ai_model
        self.provider = settings.ai_provider
        self._client: Optional[AsyncOpenAI] = None

    def _get_client(self) -> AsyncOpenAI:
        """Lazily build the AsyncOpenAI client (reuse across calls)."""
        if self._client is None:
            self._client = AsyncOpenAI(api_key=self.api_key, base_url=_BASE_URL)
        return self._client

    def _resolve_model(self, requested: Optional[str] = None) -> str:
        """Resolve the model name to one the OpenAI API accepts.

        emergentintegrations routed claude-*/gemini-* via litellm; we no longer
        have that bridge, so non-OpenAI model names fall back to gpt-4o, which
        handles reasoning, vision, and general text.
        """
        model = requested or self.model
        if not model or model.startswith(("claude-", "gemini-")):
            return "gpt-4o"
        return model

    async def _complete(
        self,
        system_message: str,
        user_text: str,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """Single-turn completion against the OpenAI Chat Completions API."""
        client = self._get_client()
        resolved = self._resolve_model(model)
        # o1/o3 reasoning models only accept temperature=1 and don't honor
        # max_tokens the same way; keep the call valid for them.
        kwargs: Dict[str, Any] = {
            "model": resolved,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_text},
            ],
        }
        if resolved.startswith(("o1", "o3")):
            kwargs["temperature"] = 1
        else:
            kwargs["max_tokens"] = max_tokens
            kwargs["temperature"] = temperature
        resp = await client.chat.completions.create(**kwargs)
        return resp.choices[0].message.content or ""

    async def send_chat_message(self, session_id: str, message: str) -> str:
        """Send a message to the AI chat and get response"""
        try:
            system_message = """You are a helpful AI assistant for NOWHERE Digital, a leading digital marketing agency in Dubai, UAE.

            You help with:
            - Digital marketing strategy
            - Social media marketing
            - Web development
            - AI solutions
            - SEO and content marketing
            - WhatsApp business solutions
            - E-commerce development
            - Lead generation

            Always be professional, helpful, and provide actionable insights specific to the UAE market.
            Use a friendly but professional tone and include relevant examples when possible.

            If users ask about services, pricing, or want to book a consultation, guide them to use the booking system or contact form."""
            return await self._complete(system_message, message)
        except Exception as e:
            logger.error(f"Error sending chat message: {e}")
            return "I'm sorry, I'm having trouble processing your request right now. Please try again later or contact our support team."

    async def generate_content(self, content_type: str, prompt: str, additional_context: Dict[str, Any] = None) -> str:
        """Generate content using AI"""
        try:
            system_messages = {
                "blog_post": """You are a content writer for NOWHERE Digital. Create engaging blog posts about digital marketing,
                web development, and business growth in the UAE market. Include actionable tips and local insights.""",

                "social_media": """You are a social media expert for NOWHERE Digital. Create engaging social media content
                that resonates with UAE audiences. Include relevant hashtags and call-to-actions.""",

                "ad_copy": """You are an advertising copywriter for NOWHERE Digital. Create compelling ad copy that converts
                for the UAE market. Focus on benefits, urgency, and clear call-to-actions.""",

                "email_campaign": """You are an email marketing specialist for NOWHERE Digital. Create email campaigns that
                engage UAE customers and drive conversions. Include personalization and clear CTAs.""",

                "web_copy": """You are a web copywriter for NOWHERE Digital. Create website copy that converts visitors
                into customers. Focus on benefits, credibility, and clear value propositions.""",

                "seo_content": """You are an SEO content specialist for NOWHERE Digital. Create SEO-optimized content
                that ranks well in UAE search results and provides value to readers."""
            }

            system_message = system_messages.get(content_type,
                "You are a content creator for NOWHERE Digital. Create high-quality content based on the given prompt.")

            if additional_context:
                system_message += f"\n\nAdditional context: {additional_context}"

            return await self._complete(system_message, prompt)
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return "I'm sorry, I couldn't generate the content right now. Please try again later."

    async def generate_service_recommendations(self, user_input: str) -> str:
        """Generate service recommendations based on user input"""
        try:
            system_message = """You are a digital marketing consultant for NOWHERE Digital. Based on the user's business
            needs, recommend the most suitable services from our portfolio:

            Services available:
            - Social Media Marketing (Instagram, TikTok, LinkedIn, YouTube)
            - WhatsApp Business Solutions
            - Web & App Development
            - AI Solutions & Chatbots
            - SEO & Search Marketing
            - Content Marketing
            - E-commerce Solutions
            - Lead Generation
            - Marketing Automation
            - AR/VR Marketing
            - Voice & Audio Marketing
            - Event Marketing

            Provide specific recommendations with explanations and suggest next steps."""
            return await self._complete(system_message, user_input)
        except Exception as e:
            logger.error(f"Error generating service recommendations: {e}")
            return "I'm sorry, I couldn't generate recommendations right now. Please contact our team directly for personalized service recommendations."

    async def analyze_market_trends(self, industry: str, location: str = "UAE") -> str:
        """Analyze market trends for a specific industry"""
        try:
            system_message = f"""You are a market research analyst for NOWHERE Digital. Analyze current digital marketing
            trends for the {industry} industry in {location}. Provide insights on:

            - Current market trends
            - Digital marketing opportunities
            - Competitive landscape
            - Consumer behavior patterns
            - Recommended strategies
            - ROI potential

            Focus on actionable insights that can help businesses grow."""
            prompt = f"Analyze the current digital marketing trends and opportunities for {industry} businesses in {location}."
            return await self._complete(system_message, prompt)
        except Exception as e:
            logger.error(f"Error analyzing market trends: {e}")
            return "I'm sorry, I couldn't analyze the market trends right now. Please try again later."

    async def generate_strategy_proposal(self, business_info: Dict[str, Any]) -> str:
        """Generate a digital marketing strategy proposal"""
        try:
            system_message = """You are a digital marketing strategist for NOWHERE Digital. Create comprehensive
            digital marketing strategy proposals tailored to the UAE market. Include:

            - Situation analysis
            - Target audience identification
            - Recommended channels and tactics
            - Timeline and milestones
            - Budget considerations
            - Expected outcomes
            - Next steps

            Make the proposal professional and actionable."""
            prompt = f"""Create a digital marketing strategy proposal for:
Business: {business_info.get('business_name', 'Not specified')}
Industry: {business_info.get('industry', 'Not specified')}
Target Market: {business_info.get('target_market', 'UAE')}
Current Challenges: {business_info.get('challenges', 'Not specified')}
Goals: {business_info.get('goals', 'Not specified')}
Budget Range: {business_info.get('budget', 'Not specified')}
"""
            return await self._complete(system_message, prompt)
        except Exception as e:
            logger.error(f"Error generating strategy proposal: {e}")
            return "I'm sorry, I couldn't generate the strategy proposal right now. Please contact our team for a personalized proposal."

# Create global AI service instance
ai_service = AIService()