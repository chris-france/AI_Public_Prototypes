"""Scanner API routes with SSE progress."""

import json
from typing import Optional

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from database import save_scan, get_scan_history, get_scan_by_id
from providers import get_ollama_models, query_ollama, query_claude
from security_tests import SECURITY_TESTS, evaluate_response, get_test_list

router = APIRouter(prefix="/api")

CLAUDE_MODELS = [
    "claude-sonnet-4-5-20250929",
    "claude-opus-4-5-20251101",
    "claude-haiku-4-5-20251001",
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514",
]


@router.get("/models")
def list_models():
    ollama = get_ollama_models()
    return {"ollama": ollama, "claude": CLAUDE_MODELS}


@router.get("/tests")
def list_tests():
    return get_test_list()


class ScanRequest(BaseModel):
    models: list[str]
    claude_api_key: Optional[str] = None


@router.post("/scan")
def run_scan(req: ScanRequest):
    """SSE endpoint that streams scan progress and results."""

    def generate():
        for model_idx, model_name in enumerate(req.models):
            yield f"data: {json.dumps({'type': 'model_start', 'model': model_name, 'model_index': model_idx, 'total_models': len(req.models)})}\n\n"

            results = []
            for i, test in enumerate(SECURITY_TESTS):
                yield f"data: {json.dumps({'type': 'test_start', 'model': model_name, 'test_index': i, 'total_tests': len(SECURITY_TESTS), 'test_name': test['name']})}\n\n"

                if model_name.startswith("claude-"):
                    response = query_claude(req.claude_api_key or "", test["prompt"], model_name)
                else:
                    response = query_ollama(model_name, test["prompt"])

                status, points, explanation = evaluate_response(test, response)

                result = {
                    "test_id": test["id"],
                    "test_name": test["name"],
                    "description": test["description"],
                    "prompt": test["prompt"],
                    "response": response[:2000],
                    "status": status,
                    "points": points,
                    "max_points": 10,
                    "explanation": explanation,
                }
                results.append(result)

                yield f"data: {json.dumps({'type': 'test_result', 'model': model_name, 'result': result})}\n\n"

            total_score = sum(r["points"] for r in results)
            max_score = sum(r["max_points"] for r in results)
            save_scan(model_name, total_score, max_score, results)

            yield f"data: {json.dumps({'type': 'model_done', 'model': model_name, 'total_score': total_score, 'max_score': max_score})}\n\n"

        yield f"data: {json.dumps({'type': 'scan_complete'})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/history")
def scan_history(limit: int = Query(default=200)):
    return get_scan_history(limit)


@router.get("/history/{scan_id}")
def scan_detail(scan_id: int):
    result = get_scan_by_id(scan_id)
    if not result:
        return {"error": "Scan not found"}
    return result


@router.get("/export/json")
def export_json():
    history = get_scan_history(100)
    return history


@router.get("/export/csv")
def export_csv():
    history = get_scan_history(100)
    lines = ["id,model_name,scan_date,total_score,max_score,percentage"]
    for h in history:
        pct = (h["total_score"] / h["max_score"] * 100) if h["max_score"] > 0 else 0
        lines.append(f"{h['id']},{h['model_name']},{h['scan_date']},{h['total_score']},{h['max_score']},{pct:.0f}%")
    return StreamingResponse(
        iter(["\n".join(lines)]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=scan_history.csv"},
    )
