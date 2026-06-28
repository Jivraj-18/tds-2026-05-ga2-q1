import time
import uuid

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

EMAIL = "22f3002542@ds.study.iitm.ac.in"
ALLOWED_ORIGINS = ["https://dash-jwofiv.example.com"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


class HeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
        return response


app.add_middleware(HeadersMiddleware)


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        nums = [int(x.strip()) for x in values.split(",")]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid input")

    if not nums:
        raise HTTPException(status_code=400, detail="No values")

    s = sum(nums)

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": s,
        "min": min(nums),
        "max": max(nums),
        "mean": s / len(nums),
    }