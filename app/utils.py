
from urllib.parse import urlparse, urlencode, urlunparse, parse_qsl

def normalize_share_url(url: str, pwd: str | None = None) -> str:
    """
    Ensure URL uses a recognized host and include password if provided.
    Keeps original host if already terabox-like.
    """
    p = urlparse(url.strip())
    host = p.netloc.lower()
    if "terabox" not in host:
        # default to www.terabox.com if user pasted just a path or weird host
        netloc = "www.terabox.com"
        p = p._replace(netloc=netloc, scheme="https")
    # attach pwd if provided and not already present
    qs = dict(parse_qsl(p.query, keep_blank_values=True))
    if pwd and "pwd" not in qs:
        qs["pwd"] = pwd
    new_qs = urlencode(qs, doseq=True)
    return urlunparse((p.scheme or "https", p.netloc, p.path, p.params, new_qs, p.fragment))
