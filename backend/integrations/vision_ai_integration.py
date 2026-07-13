"""
OpenAI Vision AI Integration - Image Analysis.

Rewritten 2026-07-13: the private `emergentintegrations.llm.chat` wrapper
(LlmChat / ImageContent / FileContentWithMimeType) has been removed along with
its transitive `litellm` dependency. We now call OpenAI's chat completions API
directly with the standard vision `image_url` content format. The public
surface is unchanged: `analyze_image(image_data, prompt, image_type)` ->
{"analysis","model","timestamp"}, `analyze_image_url`, `get_supported_formats`.
"""
import logging
import os
import base64
from typing import Dict, Any
from datetime import datetime, timezone

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

_BASE_URL = os.getenv("OPENAI_BASE_URL") or None
_VISION_MODEL = "gpt-4o"

# Sniff the data-URL mime from a base64 JPEG/PNG/etc header.
_MIME_BY_MAGIC = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"RIFF": "image/webp",  # WebP containers start with RIFF
    b"GIF8": "image/gif",
}


def _detect_mime(b64: str) -> str:
    try:
        raw = base64.b64decode(b64[:32])
    except Exception:
        return "image/jpeg"
    for magic, mime in _MIME_BY_MAGIC.items():
        if raw.startswith(magic):
            return mime
    return "image/jpeg"


class VisionAIIntegration:
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY") or os.getenv("OPENAI_API_KEY", "")
        self._client = None

    def _get_client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(api_key=self.api_key, base_url=_BASE_URL)
        return self._client

    async def analyze_image(
        self,
        image_data: str,
        prompt: str = "Analyze this image and describe what you see in detail.",
        image_type: str = "base64"
    ) -> Dict[str, Any]:
        """Analyze an image using OpenAI Vision (gpt-4o)."""
        try:
            client = self._get_client()

            if image_type == "base64":
                mime = _detect_mime(image_data)
                data_url = f"data:{mime};base64,{image_data}"
            else:
                # Treat as a file path on disk.
                path = image_data
                with open(path, "rb") as fh:
                    raw = fh.read()
                ext = os.path.splitext(path)[1].lower().lstrip(".")
                mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext or 'jpeg'}"
                data_url = f"data:{mime};base64,{base64.b64encode(raw).decode()}"

            resp = await client.chat.completions.create(
                model=_VISION_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert image analyst. Provide detailed, accurate analysis of images."},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ]},
                ],
                max_tokens=2048,
            )
            return {
                "analysis": resp.choices[0].message.content or "",
                "model": _VISION_MODEL,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error(f"Vision AI analysis error: {e}")
            return {"error": str(e)}

    async def analyze_image_url(self, image_url: str, prompt: str) -> Dict[str, Any]:
        """Analyze an image from a public URL."""
        try:
            client = self._get_client()
            resp = await client.chat.completions.create(
                model=_VISION_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert image analyst. Provide detailed, accurate analysis of images."},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ]},
                ],
                max_tokens=2048,
            )
            return {
                "analysis": resp.choices[0].message.content or "",
                "model": _VISION_MODEL,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.error(f"Vision AI URL analysis error: {e}")
            return {"error": str(e)}

    def get_supported_formats(self) -> Dict[str, Any]:
        """Get supported image formats"""
        return {
            "formats": ["jpeg", "jpg", "png", "webp", "gif"],
            "max_size_mb": 20,
            "input_types": ["base64", "file_path", "url"]
        }

vision_ai_integration = VisionAIIntegration()