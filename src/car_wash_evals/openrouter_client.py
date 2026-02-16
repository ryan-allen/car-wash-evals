from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


class OpenRouterError(RuntimeError):
    """Raised when OpenRouter returns an error or an invalid response."""


@dataclass(frozen=True)
class ChatResponse:
    text: str
    usage: dict[str, Any] | None


class OpenRouterClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://openrouter.ai/api/v1",
        timeout_seconds: int = 60,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def list_models(self) -> set[str]:
        url = f"{self._base_url}/models"
        try:
            resp = requests.get(url, headers=self._headers, timeout=self._timeout_seconds)
        except requests.RequestException as exc:
            raise OpenRouterError(f"Failed to fetch model list: {exc}") from exc

        if resp.status_code != 200:
            raise OpenRouterError(f"Model list request failed ({resp.status_code}): {resp.text}")

        payload = resp.json()
        models = payload.get("data")
        if not isinstance(models, list):
            raise OpenRouterError("Invalid model list response: missing data[]")

        ids: set[str] = set()
        for item in models:
            if isinstance(item, dict):
                model_id = item.get("id")
                if isinstance(model_id, str) and model_id:
                    ids.add(model_id)
        return ids

    def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> ChatResponse:
        url = f"{self._base_url}/chat/completions"
        body = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            resp = requests.post(
                url,
                headers=self._headers,
                json=body,
                timeout=self._timeout_seconds,
            )
        except requests.RequestException as exc:
            raise OpenRouterError(f"Chat completion failed for model {model}: {exc}") from exc

        if resp.status_code != 200:
            raise OpenRouterError(
                f"Chat completion request failed for {model} ({resp.status_code}): {resp.text}"
            )

        payload = resp.json()
        text = _extract_text(payload)
        usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else None
        return ChatResponse(text=text, usage=usage)


def _extract_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise OpenRouterError("Invalid chat response: missing choices[]")

    message = choices[0].get("message")
    if not isinstance(message, dict):
        raise OpenRouterError("Invalid chat response: missing message")

    content = message.get("content")
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
                parts.append(item["text"])
        if parts:
            return "\n".join(parts)

    raise OpenRouterError("Invalid chat response: unsupported message content format")
