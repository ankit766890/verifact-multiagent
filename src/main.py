import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.core.config import settings
from src.agents.orchestrator import Orchestrator
from src.models.schemas import ResearchDossier


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production Multi-Agent Research & Fact-Checking Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()


class FactCheckRequest(BaseModel):
    statement: str = Field(
        ...,
        min_length=5,
        max_length=settings.MAX_CLAIM_LENGTH,
        description="Factual statement or claim to investigate",
        examples=["NASA Apollo 11 landed humans on the Moon in 1969."]
    )


@app.get("/health", tags=["System"])
def health_check():
    """Health and Readiness probe for container orchestrators."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "agents": ["LeadPlannerAgent", "EvidenceHubAgent", "RedTeamVerifierAgent", "ChiefSynthesizerAgent"]
    }


@app.post("/api/v1/verify", response_model=ResearchDossier, tags=["Fact-Checking"])
def verify_statement(request: FactCheckRequest):
    """
    Submits a query to the multi-agent pipeline for claim deconstruction,
    evidence retrieval, adversarial cross-examination, and synthesis.
    """
    try:
        dossier = orchestrator.run(request.statement)
        return dossier
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(val_err)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline processing failed: {str(exc)}"
        )


@app.get("/", response_class=HTMLResponse, tags=["UI"])
def render_dashboard():
    """Renders the accessible web dashboard."""
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>VeriFact Multi-Agent Platform</h1><p>API is active. Visit /docs for OpenAPI specs.</p>")
