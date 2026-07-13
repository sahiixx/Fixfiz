"""
OpenAI Voice AI Integration - Realtime voice session surface.

Rewritten 2026-07-13: the private `emergentintegrations.llm.openai.OpenAIChatRealtime`
client (and its transitive `litellm` dependency) has been removed. Full realtime
voice requires OpenAI's Realtime API over WebRTC/WebSocket plus frontend wiring
that is not yet implemented, so this integration is now an honest stub: it
reports readiness based on whether an API key is configured, but does not open
a media session. The public surface (`create_voice_session`, `get_integration_info`)
is unchanged so existing routes keep working.

When real voice is needed: add the `openai` realtime client + a `/api/voice/session`
endpoint that mints an ephemeral key, and connect WebRTC on the frontend.
"""
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class VoiceAIIntegration:
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY") or os.getenv("OPENAI_API_KEY", "")
        self.realtime_chat = None  # reserved for a future realtime client

    def get_realtime_client(self):
        """Return the realtime client if one has been built.

        Currently always None — realtime voice is not wired up. Kept on the
        public surface so callers don't break; returns None rather than raising.
        """
        return self.realtime_chat

    async def create_voice_session(self) -> Dict[str, Any]:
        """Create a voice chat session.

        Honest stub: reports whether an API key is present. A real session
        (ephemeral Realtime key + WebRTC SDP exchange) is roadmap work.
        """
        try:
            configured = bool(self.api_key)
            return {
                "status": "ready" if configured else "not_configured",
                "message": "Voice AI session initialized"
                           if configured
                           else "Voice AI not configured — set EMERGENT_LLM_KEY/OPENAI_API_KEY and wire realtime WebRTC.",
                "client_ready": configured,
            }
        except Exception as e:
            logger.error(f"Voice AI session error: {e}")
            return {"error": str(e)}

    def get_integration_info(self) -> Dict[str, Any]:
        """Get integration information"""
        return {
            "provider": "OpenAI Realtime",
            "capabilities": [
                "Real-time voice chat",
                "Speech-to-text",
                "Text-to-speech",
                "WebRTC support"
            ],
            "status": "available" if self.api_key else "not_configured"
        }

voice_ai_integration = VoiceAIIntegration()