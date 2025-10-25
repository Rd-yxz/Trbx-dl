
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl
from typing import Optional
from app.backends import resolve_any
from app.utils import normalize_share_url

app = FastAPI(title="Terabox API (Vercel-ready)", version="1.1.0")

class Req(BaseModel):
    url: HttpUrl
    pwd: Optional[str] = None  # optional extract code if your link requires it

@app.get("/api/health")
def health():
    return {"ok": True, "version": "1.1.0"}

@app.get("/api/dl")
def get_dl(url: str = Query(..., description="Terabox share URL"),
           pwd: Optional[str] = Query(None, description="Optional extract code/password")):
    share_url = normalize_share_url(url, pwd)
    data = resolve_any(share_url)
    if not data.get("ok"):
        raise HTTPException(status_code=data.get("status", 500), detail=data.get("error", "Failed"))
    return data

@app.post("/api/dl")
def post_dl(req: Req):
    share_url = normalize_share_url(str(req.url), req.pwd)
    data = resolve_any(share_url)
    if not data.get("ok"):
        raise HTTPException(status_code=data.get("status", 500), detail=data.get("error", "Failed"))
    return data

# (Optional) Info endpoint returns raw upstream response for troubleshooting
@app.get("/api/info")
def info(url: str = Query(...), pwd: Optional[str] = Query(None)):
    share_url = normalize_share_url(url, pwd)
    data = resolve_any(share_url, return_raw=True)
    if not data.get("ok"):
        raise HTTPException(status_code=data.get("status", 500), detail=data.get("error", "Failed"))
    return data
      
