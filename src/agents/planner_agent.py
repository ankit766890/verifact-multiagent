import re
import uuid
from typing import List, Dict, Any
from src.agents.base_agent import BaseAgent
from src.models.schemas import AtomicClaim


class PlannerAgent(BaseAgent):
    """
    Agent 1: Lead Planner Agent.
    Deconstructs complex, ambiguous, or multi-faceted input statements into
    isolated, testable, atomic factual claims.
    """

    def __init__(self):
        super().__init__(
            name="LeadPlannerAgent",
            role_description="Deconstructs raw text into atomic verifiable claims with semantic tagging."
        )

    def execute(self, payload: str, context: Dict[str, Any]) -> List[AtomicClaim]:
        raw_text = payload.strip()
        if not raw_text:
            return []

        # Split sentences and clauses around conjunctions (and, but, whereas, however, also)
        split_pattern = r"(?<=[.!?])\s+|(?<=[,;])\s+(?:and|but|whereas|however|while|moreover|also)\s+"
        parts = re.split(split_pattern, raw_text, flags=re.IGNORECASE)

        claims: List[AtomicClaim] = []
        for index, part in enumerate(parts):
            cleaned = part.strip().strip(".!?,; ")
            if len(cleaned) < 8:
                continue

            # Determine category heuristics
            category = "General"
            lower_c = cleaned.lower()
            if any(w in lower_c for w in ["percent", "%", "dollar", "$", "gdp", "market", "revenue", "inflation", "economy"]):
                category = "Economics & Finance"
            elif any(w in lower_c for w in ["vaccine", "health", "cancer", "cure", "virus", "disease", "diet", "who"]):
                category = "Health & Medicine"
            elif any(w in lower_c for w in ["ai", "quantum", "software", "tech", "algorithm", "launch", "space", "mars", "moon"]):
                category = "Science & Technology"
            elif any(w in lower_c for w in ["election", "president", "minister", "parliament", "congress", "law", "court"]):
                category = "Politics & Governance"

            # Check for temporal anchors (years, months, recent, currently)
            has_temporal = bool(re.search(r"\b(19\d{2}|20\d{2}|yesterday|today|current|recent|decade)\b", cleaned, re.IGNORECASE))

            # Extract named entities (Capitalized words)
            entities = list(set(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", cleaned)))

            claims.append(AtomicClaim(
                claim_id=f"CLM-{uuid.uuid4().hex[:6].upper()}",
                original_text=part.strip(),
                normalized_claim=cleaned,
                topic_category=category,
                requires_temporal_context=has_temporal,
                entities=entities
            ))

        # Fallback if sentence splitter yields nothing
        if not claims:
            claims.append(AtomicClaim(
                claim_id=f"CLM-{uuid.uuid4().hex[:6].upper()}",
                original_text=raw_text,
                normalized_claim=raw_text,
                topic_category="General",
                requires_temporal_context=False,
                entities=[]
            ))

        return claims[:8]
