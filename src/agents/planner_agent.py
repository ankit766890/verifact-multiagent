import re
import uuid
from typing import List, Dict, Any
from src.agents.base_agent import BaseAgent
from src.models.schemas import AtomicClaim


class PlannerAgent(BaseAgent):
    """
    Agent 1: Lead Planner Agent.
    Deconstructs complex, compound discourse into atomic verifiable propositions,
    isolating entities, temporal bounds, and semantic domains.
    """

    def __init__(self):
        super().__init__(
            name="LeadPlannerAgent",
            role_description="Deconstructs raw text into atomic verifiable claims with semantic tagging and temporal anchoring."
        )

    def execute(self, payload: str, context: Dict[str, Any]) -> List[AtomicClaim]:
        raw_text = payload.strip()
        if not raw_text:
            return []

        # Sophisticated clause segmentation recognizing coordinating conjunctions & punctuation
        split_pattern = r"(?<=[.!?])\s+|(?<=[,;])\s+(?:and|but|whereas|however|while|moreover|also|despite|although)\s+"
        raw_parts = re.split(split_pattern, raw_text, flags=re.IGNORECASE)

        claims: List[AtomicClaim] = []
        for index, part in enumerate(raw_parts):
            cleaned = part.strip().strip(".!?,; ")
            if len(cleaned) < 6:
                continue

            # Semantic Topic Classification
            lower_c = cleaned.lower()
            category = "General Knowledge"
            if any(w in lower_c for w in ["percent", "%", "dollar", "$", "gdp", "market", "revenue", "inflation", "economy", "crypto", "bitcoin"]):
                category = "Economics & Finance"
            elif any(w in lower_c for w in ["vaccine", "health", "cancer", "cure", "virus", "disease", "diet", "who", "fda", "covid", "medicine"]):
                category = "Medical & Health Sciences"
            elif any(w in lower_c for w in ["ai", "quantum", "software", "tech", "algorithm", "launch", "space", "mars", "moon", "nasa", "physics", "climate"]):
                category = "Science & Technology"
            elif any(w in lower_c for w in ["election", "president", "minister", "parliament", "congress", "law", "court", "treaty", "vote", "bill"]):
                category = "Governance & Policy"
            elif any(w in lower_c for w in ["war", "treaty", "ancient", "century", "empire", "historic", "revolution", "19", "20"]):
                category = "Historical Analysis"

            # Temporal Anchoring
            temporal_match = re.search(r"\b(19\d{2}|20\d{2}|yesterday|today|current|recent|decade|century|in the year \d{4})\b", cleaned, re.IGNORECASE)
            has_temporal = bool(temporal_match)
            temporal_anchor = temporal_match.group(0) if temporal_match else None

            # Entity Extraction (Capitalized multi-word sequences)
            entities = list(dict.fromkeys(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", cleaned)))

            claims.append(AtomicClaim(
                claim_id=f"CLM-{uuid.uuid4().hex[:6].upper()}",
                original_text=part.strip(),
                normalized_claim=cleaned,
                topic_category=category,
                requires_temporal_context=has_temporal,
                temporal_anchor=temporal_anchor,
                entities=entities,
                confidence_weight=1.0 if not has_temporal else 1.2
            ))

        if not claims:
            claims.append(AtomicClaim(
                claim_id=f"CLM-{uuid.uuid4().hex[:6].upper()}",
                original_text=raw_text,
                normalized_claim=raw_text,
                topic_category="General Knowledge",
                requires_temporal_context=False,
                entities=[]
            ))

        return claims[:8]
