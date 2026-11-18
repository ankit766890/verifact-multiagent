import re
import html


class InputSanitizer:
    """Security utility to sanitize user input and prevent prompt/XSS injection attacks."""

    @staticmethod
    def clean_text(text: str, max_length: int = 1500) -> str:
        if not text:
            return ""
        # Strip trailing/leading whitespace
        cleaned = text.strip()
        # Truncate to maximum permissible length
        cleaned = cleaned[:max_length]
        # HTML entity encode to defeat XSS in rendered outputs
        cleaned = html.escape(cleaned)
        # Normalize continuous whitespaces
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    @staticmethod
    def validate_claim_text(text: str) -> bool:
        if not text or len(text.strip()) < 5:
            return False
        # Filter dangerous binary or script tags
        dangerous_patterns = [
            r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>",
            r"javascript:",
            r"onerror=",
            r"onload="
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        return True
