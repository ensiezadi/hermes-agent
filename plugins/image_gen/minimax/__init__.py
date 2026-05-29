"""MiniMax image generation backend.

Exposes MiniMax's ``image-01`` model.
"""

from __future__ import annotations

import logging
import os
import httpx
from typing import Any, Dict, List, Optional, Tuple

from agent.image_gen_provider import (
    DEFAULT_ASPECT_RATIO,
    ImageGenProvider,
    error_response,
    resolve_aspect_ratio,
    save_b64_image,
    success_response,
)
from hermes_cli.config import get_env_value

logger = logging.getLogger(__name__)

API_MODEL = "image-01"

_MODELS: Dict[str, Dict[str, Any]] = {
    "image-01": {
        "display": "MiniMax Image-01",
        "speed": "~10s",
        "strengths": "Fast, high quality",
    },
}

DEFAULT_MODEL = "image-01"

_SIZES = {
    "landscape": "16:9",
    "square": "1:1",
    "portrait": "9:16",
}

class MiniMaxImageGenProvider(ImageGenProvider):
    """MiniMax ``image_generation`` backend."""

    @property
    def name(self) -> str:
        return "minimax"

    @property
    def display_name(self) -> str:
        return "MiniMax"

    def is_available(self) -> bool:
        return bool(get_env_value("MINIMAX_API_KEY") or get_env_value("MINIMAX_CN_API_KEY"))

    def list_models(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": model_id,
                "display": meta["display"],
                "speed": meta["speed"],
                "strengths": meta["strengths"],
                "price": "varies",
            }
            for model_id, meta in _MODELS.items()
        ]

    def default_model(self) -> Optional[str]:
        return DEFAULT_MODEL

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "MiniMax",
            "badge": "paid",
            "tag": "image-01",
            "env_vars": [
                {
                    "key": "MINIMAX_API_KEY",
                    "prompt": "MiniMax API key",
                    "url": "https://platform.minimaxi.com",
                },
            ],
        }

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = DEFAULT_ASPECT_RATIO,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        prompt = (prompt or "").strip()
        aspect = resolve_aspect_ratio(aspect_ratio)

        if not prompt:
            return error_response(
                error="Prompt is required and must be a non-empty string",
                error_type="invalid_argument",
                provider="minimax",
                aspect_ratio=aspect,
            )

        api_key = get_env_value("MINIMAX_API_KEY") or get_env_value("MINIMAX_CN_API_KEY")
        if not api_key:
            return error_response(
                error=(
                    "MINIMAX_API_KEY not set. Run `hermes tools` → Image "
                    "Generation → MiniMax to configure, or set MINIMAX_API_KEY."
                ),
                error_type="auth_required",
                provider="minimax",
                aspect_ratio=aspect,
            )

        api_host = get_env_value("MINIMAX_API_HOST")
        if not api_host:
            # Fallback to extracting from MINIMAX_CN_BASE_URL if it exists
            cn_base = get_env_value("MINIMAX_CN_BASE_URL")
            if cn_base and cn_base.startswith("http"):
                # Extract just the host part (e.g. https://api.minimaxi.com)
                from urllib.parse import urlparse
                parsed = urlparse(cn_base)
                api_host = f"{parsed.scheme}://{parsed.netloc}"
            else:
                api_host = "https://api.minimaxi.com"
                
        url = f"{api_host.rstrip('/')}/v1/image_generation"
        size = _SIZES.get(aspect, "1:1")

        payload = {
            "model": API_MODEL,
            "prompt": prompt,
            "aspect_ratio": size,
            "num_images": 1,
            "response_format": "url",
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
        except Exception as exc:
            logger.debug("MiniMax image generation failed", exc_info=True)
            # Try to extract detailed error from httpx response
            error_details = str(exc)
            if hasattr(exc, "response") and exc.response is not None:
                try:
                    resp_json = exc.response.json()
                    if "base_resp" in resp_json:
                        error_details = resp_json["base_resp"].get("status_msg", error_details)
                except Exception:
                    pass
            return error_response(
                error=f"MiniMax image generation failed: {error_details}",
                error_type="api_error",
                provider="minimax",
                model=DEFAULT_MODEL,
                prompt=prompt,
                aspect_ratio=aspect,
            )

        # Defensive parsing
        base_resp = data.get("base_resp", {})
        if base_resp.get("status_code") != 0:
            err_msg = base_resp.get("status_msg", "unknown error")
            return error_response(
                error=f"MiniMax API error ({base_resp.get('status_code')}): {err_msg}",
                error_type="api_error",
                provider="minimax",
                model=DEFAULT_MODEL,
                prompt=prompt,
                aspect_ratio=aspect,
            )

        image_url = None
        b64 = None

        if "data" in data and isinstance(data["data"], dict):
            # Check for image_urls or b64_image
            image_urls = data["data"].get("image_urls", [])
            b64_image = data["data"].get("b64_image")
            
            if image_urls and len(image_urls) > 0:
                image_url = image_urls[0]
            elif b64_image:
                b64 = b64_image

        if not image_url and not b64:
            # Fallback for standard formats
            if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
                item = data["data"][0]
                if "url" in item:
                    image_url = item["url"]
                elif "base64" in item:
                    b64 = item["base64"]
                elif "image" in item:
                    image_url = item["image"]
            elif "url" in data:
                image_url = data["url"]
            elif "base64_data" in data and isinstance(data["base64_data"], list) and len(data["base64_data"]) > 0:
                b64 = data["base64_data"][0]
            elif "images" in data and isinstance(data["images"], list) and len(data["images"]) > 0:
                item = data["images"][0]
                image_url = item.get("url")

        if b64:
            try:
                saved_path = save_b64_image(b64, prefix="minimax_image")
                image_url = str(saved_path)
            except Exception as exc:
                return error_response(
                    error=f"Could not save image to cache: {exc}",
                    error_type="io_error",
                    provider="minimax",
                    model=DEFAULT_MODEL,
                    prompt=prompt,
                    aspect_ratio=aspect,
                )

        if not image_url:
            return error_response(
                error=f"MiniMax returned no image data: {list(data.keys())}",
                error_type="empty_response",
                provider="minimax",
                model=DEFAULT_MODEL,
                prompt=prompt,
                aspect_ratio=aspect,
            )

        return success_response(
            image=image_url,
            model=DEFAULT_MODEL,
            prompt=prompt,
            aspect_ratio=aspect,
            provider="minimax",
            extra={"size": size},
        )

def register(ctx) -> None:
    """Plugin entry point — wire ``MiniMaxImageGenProvider`` into the registry."""
    ctx.register_image_gen_provider(MiniMaxImageGenProvider())
