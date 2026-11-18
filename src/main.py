import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.core.config import settings
from src.agents.orchestrator import Orchestrator
from src.models.schemas import ResearchDossier, ExecutionMode


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Multi-Agent Autonomous Research & Fact Verification Platform"
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
        description="Discourse, news excerpt, or factual proposition to verify",
        examples=["NASA Apollo 11 landed humans on the Moon in July 1969."]
    )
    mode: ExecutionMode = Field(
        default=ExecutionMode.PIPELINE,
        description="Execution mode: PIPELINE (Full Swarm), PLANNER, EVIDENCE, or REDTEAM"
    )


@app.get("/health", tags=["System"])
def health_check():
    """Enterprise readiness and health probe."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "supported_modes": ["PIPELINE", "PLANNER", "EVIDENCE", "REDTEAM"],
        "agents": [
            "LeadPlannerAgent",
            "EvidenceHubAgent",
            "RedTeamVerifierAgent",
            "ChiefSynthesizerAgent"
        ]
    }


@app.post("/api/v1/verify", response_model=ResearchDossier, tags=["Intelligence & Verification"])
def verify_statement(request: FactCheckRequest):
    """
    Core verification endpoint dispatching discourse to the multi-agent cognitive pipeline.
    """
    try:
        dossier = orchestrator.run(request.statement, mode=request.mode)
        return dossier
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(val_err)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification pipeline error: {str(exc)}"
        )


@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def render_dashboard():
    """Renders the enterprise intelligence dashboard."""
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>VeriFact Enterprise</h1><p>API is active. Visit /docs for OpenAPI documentation.</p>")
