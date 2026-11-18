import re
import html
from typing import Dict, Any, List


class SecurityGuard:
    """Enterprise Prompt Injection, XSS, and Adversarial Input Sanitization Engine."""

    FORBIDDEN_PATTERNS = [
        r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>",
        r"javascript:",
        r"onerror\s*=",
        r"onload\s*=",
        r"eval\s*\(",
        r"union\s+select",
        r"drop\s+table"
    ]

    @classmethod
    def sanitize(cls, text: str, max_chars: int = 1500) -> str:
        if not text:
            return ""
        cleaned = text.strip()[:max_chars]
        cleaned = html.escape(cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    @classmethod
    def audit_security(cls, text: str) -> Dict[str, Any]:
        if not text or len(text.strip()) < 4:
            return {"safe": False, "reason": "Query string is too short or empty."}
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return {"safe": False, "reason": "Potential malicious payload/script detected in query payload."}
        return {"safe": True, "reason": "Passed security boundary inspection."}


# Backward-compatible alias for existing tests and utilities
class InputSanitizer:
    @staticmethod
    def clean_text(text: str, max_length: int = 1500) -> str:
        return SecurityGuard.sanitize(text, max_chars=max_length)

    @staticmethod
    def validate_claim_text(text: str) -> bool:
        return SecurityGuard.audit_security(text)["safe"]
