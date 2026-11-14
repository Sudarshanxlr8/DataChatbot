import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi_app.routes import auth, account, portfolio, holdings, transactions, chatbot

app = FastAPI(
    title="DataChat Account & Portfolio API",
    description="Backend REST API for DataChat Account & Portfolio Chatbot project with JWT authentication & Gemini LLM tool calling.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local development and frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(account.router, prefix="/api")
app.include_router(portfolio.router, prefix="/api")
app.include_router(holdings.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")

@app.get("/health", tags=["Health Check"], summary="Service Health Check")
def health_check():
    """
    Health check endpoint returning system status. Public endpoint.
    """
    return {"status": "ok", "service": "DataChat FastAPI Backend"}

# Serve frontend static assets from root /
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app.main:app", host="127.0.0.1", port=8000, reload=True)
