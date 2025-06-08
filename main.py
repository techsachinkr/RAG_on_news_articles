from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
import os # Import os module
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from services.rag_utils import get_RAG_response
from services.evaluation_runner import get_metrics_no_ground_truth


print

app = FastAPI()

# --- CORS Middleware (keep this if you still plan to run React separately during development) ---
origins = [
    "http://localhost:3000",  # For React dev server
    "http://localhost:8000",  # For the served frontend
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["GOOGLE_API_KEY"] = ""

# --- API Model ---
class RAGQuery(BaseModel):
    question: str

# --- API Routes ---
@app.get("/api/hello") # Renamed to avoid conflict with root for frontend
async def read_root_api():
    return {"Hello": "World"}


@app.post("/api/rag_query/") # Prefix with /api/
async def execute_rag_query(query: RAGQuery):
    context, response = get_RAG_response(question=query.question)
    metrics = get_metrics_no_ground_truth(query.question, context, response)

    context_relevance_metric = metrics.get("context_relevance")
    context_relevance_score = float(context_relevance_metric.score) if context_relevance_metric and hasattr(context_relevance_metric, 'score') and context_relevance_metric.score is not None else 0.0
    context_relevance_reasoning = context_relevance_metric.reasoning if context_relevance_metric and hasattr(context_relevance_metric, 'reasoning') and context_relevance_metric.reasoning is not None else ""

    faithfulness_metric = metrics.get("faithfulness")
    faithfulness_score = float(faithfulness_metric.score) if faithfulness_metric and hasattr(faithfulness_metric, 'score') and faithfulness_metric.score is not None else 0.0
    faithfulness_reasoning = str(faithfulness_metric.reasoning) if faithfulness_metric and hasattr(faithfulness_metric, 'reasoning') and faithfulness_metric.reasoning is not None else ""

    answer_relevance_q_metric = metrics.get("answer_relevance_q")
    answer_relevance_q_score = float(answer_relevance_q_metric.score) if answer_relevance_q_metric and hasattr(answer_relevance_q_metric, 'score') and answer_relevance_q_metric.score is not None else 0.0
    answer_relevance_q_reasoning = answer_relevance_q_metric.reasoning if answer_relevance_q_metric and hasattr(answer_relevance_q_metric, 'reasoning') and answer_relevance_q_metric.reasoning is not None else ""

    return {"context": context,
             "response": response,
             "evaluation_metrics": {
                 "context_relevance": context_relevance_score,
                 "context_relevance_reasoning":context_relevance_reasoning,
                 "faithfulness": faithfulness_score,
                 "faithfulness_reasoning":faithfulness_reasoning,
                 "answer_relevance_q": answer_relevance_q_score,
                 "answer_relevance_q_reasoning":answer_relevance_q_reasoning,
             }
        }

# --- Static Files and Frontend Serving ---

# Define the path to the static frontend build files
# This assumes your 'static_frontend/build' directory is at the same level as main.py
STATIC_BUILD_DIR = os.path.join(os.path.dirname(__file__), "static_frontend", "build")

# Mount static files (CSS, JS, images from React build's 'static' folder)
# The path "/static" here means that files in STATIC_BUILD_DIR/static will be accessible at http://localhost:8000/static/...
# This is standard for create-react-app builds.
app.mount("/static", StaticFiles(directory=os.path.join(STATIC_BUILD_DIR, "static")), name="spa-static")

# Catch-all route to serve 'index.html' for any other path, enabling client-side routing
# This must be defined AFTER your API routes and specific static file mounts.
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_react_app_catch_all(request: Request, full_path: str):
    index_path = os.path.join(STATIC_BUILD_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse(content="Frontend not found. Please build the React app and ensure it's in the 'static_frontend/build' directory.", status_code=404)

if __name__ == "__main__":
    print(f"FastAPI version (if available): {FastAPI.__version__ if hasattr(FastAPI, '__version__') else 'unknown'}")
    print(f"FileResponse object: {FileResponse}") # Debug print: Check what FileResponse is
    print(f"Serving static files from: {STATIC_BUILD_DIR}")
    if not os.path.exists(STATIC_BUILD_DIR):
        print(f"Error: Static build directory not found at {STATIC_BUILD_DIR}")
        print("Please ensure you have run 'npm run build' in the 'static_frontend' directory.")
    elif not os.path.exists(os.path.join(STATIC_BUILD_DIR, "index.html")):
        print(f"Error: 'index.html' not found in {STATIC_BUILD_DIR}")
        print("Please check your React build output.")

    uvicorn.run(app, host="0.0.0.0", port=8000)