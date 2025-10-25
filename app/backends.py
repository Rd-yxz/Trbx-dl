
import os, json
import requests
from urllib.parse import urlencode

# You can configure multiple upstream APIs via env var BACKENDS (comma-separated).
# Default includes one Cloudflare Worker endpoint known to be live as of packaging.
DEFAULT_BACKENDS = [
    "https://terabox-worker.robinkumarshakya103.workers.dev/api"
]

def _load_backends():
    raw = os.getenv("BACKENDS", "").strip()
    if not raw:
        return DEFAULT_BACKENDS
    return [x.strip() for x in raw.split(",") if x.strip()] or DEFAULT_BACKENDS

def resolve_via_worker(base: str, share_url: str):
    try:
        r = requests.get(base, params={"url": share_url}, timeout=45)
        j = r.json()
    except Exception as e:
        return {"ok": False, "status": 502, "error": f"Upstream error: {e}"}

    if not r.ok or not isinstance(j, dict):
        return {"ok": False, "status": r.status_code, "error": "Non-JSON or HTTP error from upstream"}

    if not j.get("success"):
        return {"ok": False, "status": 502, "error": j.get("error", "Upstream reported failure")}

    files = j.get("files") or []
    if not files:
        return {"ok": False, "status": 404, "error": "No files returned by upstream"}

    f0 = files[0]
    return {
        "ok": True,
        "filename": f0.get("file_name"),
        "size": f0.get("size"),
        "download_url": f0.get("download_url"),
        "streaming_url": f0.get("streaming_url"),
        "original_download_url": f0.get("original_download_url"),
        "raw": j,  # keep raw for /api/info
    }

def resolve_any(share_url: str, return_raw: bool = False) -> dict:
    last_err = None
    for base in _load_backends():
        res = resolve_via_worker(base, share_url)
        if res.get("ok"):
            if return_raw:
                return {"ok": True, "via": base, "raw": res.get("raw")}
            # strip raw for normal DL endpoint
            res.pop("raw", None)
            res["via"] = base
            return res
        last_err = res
    return last_err or {"ok": False, "status": 500, "error": "No backend succeeded"}
