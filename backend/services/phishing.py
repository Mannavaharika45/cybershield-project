import re
from urllib.parse import urlparse

# Known legitimate high-traffic domains — reduce false positives
TRUSTED_DOMAINS = {
    'google.com',
    'youtube.com',
    'facebook.com',
    'twitter.com',
    'x.com',
    'instagram.com',
    'linkedin.com',
    'amazon.com',
    'microsoft.com',
    'apple.com',
    'netflix.com',
    'github.com',
    'wikipedia.org',
    'reddit.com',
    'paypal.com',
    'ebay.com',
    'yahoo.com',
    'bing.com',
    'dropbox.com',
    'zoom.us',
}

# Brand names commonly mimicked in phishing
BRAND_LOOKALIKES = [
    'paypa1', 'amaz0n', 'g00gle', 'micros0ft', 'faceb00k', 'app1e',
    'netfl1x', 'yourbank', 'bank-of', 'secure-login', 'account-update',
]

# High-risk path/query keywords
SUSPICIOUS_KEYWORDS = [
    'login',
    'signin',
    'verify',
    'verification',
    'update',
    'secure',
    'security',
    'account',
    'banking',
    'billing',
    'payment',
    'invoice',
    'confirm',
    'suspend',
    'validate',
    'credential',
    'wallet',
    'recover',
    'unlock',
    'reset',
    'authorize',
    'auth',
    'password',
    'passwd',
    'credential',
    'click-here',
    'urgent',
    'alert',
]


def analyze_url(url: str) -> dict:
    risk_score = 0
    reasons = []
    flags = []

    try:
        parsed = urlparse(url)
    except Exception:
        return {
            "is_phishing": True, "risk_score": 100,
            "reasons": ["URL could not be parsed — highly suspicious."],
            "label": "Likely Phishing"
        }

    domain = parsed.netloc.lower().replace("www.", "")
    path = (
        parsed.path +
        "?" +
        parsed.query).lower() if parsed.query else parsed.path.lower()
    full_url = url.lower()

    # ── 1. Scheme check ─────────────────────────────────────────────────────
    if parsed.scheme == 'http':
        risk_score += 20
        flags.append("Uses HTTP (not encrypted)")
        reasons.append(
            "⚠️  Connection is not encrypted (HTTP instead of HTTPS).")

    # ── 2. Trusted domain check (fast-pass for known legit) ──────────────────
    base_domain = ".".join(domain.split(
        ".")[-2:]) if domain.count(".") >= 1 else domain
    if base_domain in TRUSTED_DOMAINS and risk_score < 20:
        reasons.append("✅ Domain is a well-known, trusted service.")
        return {
            "is_phishing": False, "risk_score": max(0, risk_score),
            "reasons": reasons, "label": "Likely Safe"
        }

    # ── 3. IP address as domain ─────────────────────────────────────────────
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$", domain):
        risk_score += 55
        flags.append("IP address as domain")
        reasons.append(
            "🚨 URL uses a raw IP address instead of a proper domain name.")

    # ── 4. Brand lookalike / typosquatting ───────────────────────────────────
    for lookalike in BRAND_LOOKALIKES:
        if lookalike in domain:
            risk_score += 45
            flags.append(f"Brand lookalike: '{lookalike}'")
            reasons.append(
                f"🚨 Domain contains a brand lookalike pattern: '{lookalike}'.")
            break

    # ── 5. Excessive hyphens in domain ───────────────────────────────────────
    hyphen_count = domain.count('-')
    if hyphen_count >= 3:
        risk_score += 25
        reasons.append(
            f"⚠️  Domain has {hyphen_count} hyphens — common in phishing domains.")
    elif hyphen_count == 2:
        risk_score += 10
        reasons.append("ℹ️  Domain contains multiple hyphens.")

    # ── 6. Too many subdomains ──────────────────────────────────────────────
    subdomain_count = domain.count('.')
    if subdomain_count >= 4:
        risk_score += 25
        reasons.append(
            f"⚠️  URL has {subdomain_count} subdomains — unusually complex structure.")
    elif subdomain_count == 3:
        risk_score += 10
        reasons.append("ℹ️  URL contains a high number of subdomains.")

    # ── 7. Suspicious keywords in path/query ─────────────────────────────────
    found_keywords = [
        kw for kw in SUSPICIOUS_KEYWORDS if kw in path or kw in domain]
    for kw in found_keywords[:3]:  # cap at 3 triggers
        risk_score += 15
        reasons.append(f"⚠️  URL contains a suspicious keyword: '{kw}'.")

    # ── 8. Encoded characters / obfuscation ──────────────────────────────────
    if '%' in url and url.count('%') > 3:
        risk_score += 20
        reasons.append(
            "⚠️  URL contains heavy URL-encoding (possible obfuscation).")

    # ── 9. Long URL ─────────────────────────────────────────────────────────
    if len(url) > 150:
        risk_score += 15
        reasons.append(f"ℹ️  URL is very long ({len(url)} characters).")
    elif len(url) > 100:
        risk_score += 8
        reasons.append(
            f"ℹ️  URL is longer than average ({
                len(url)} characters).")

    # ── 10. Misleading redirect patterns ─────────────────────────────────────
    if 'redirect' in full_url or 'url=' in full_url or 'link=' in full_url:
        risk_score += 20
        reasons.append(
            "⚠️  URL contains a redirect parameter — could mask true destination.")

    # ── 11. Non-standard TLD ─────────────────────────────────────────────────
    tld = domain.split('.')[-1] if '.' in domain else ''
    suspicious_tlds = {
        'xyz',
        'top',
        'click',
        'gq',
        'ml',
        'tk',
        'cf',
        'pw',
        'work',
        'rest',
        'icu'}
    if tld in suspicious_tlds:
        risk_score += 20
        reasons.append(
            f"⚠️  Domain uses an unusual top-level domain (.{tld}).")

    # ── Final assessment ────────────────────────────────────────────────────
    risk_score = min(risk_score, 100)
    is_phishing = risk_score >= 45

    if not reasons:
        reasons.append(
            "✅ No significant phishing indicators detected in this URL.")

    return {
        "is_phishing": is_phishing,
        "risk_score": risk_score,
        "reasons": reasons,
        "label": "Likely Phishing" if is_phishing else "Likely Safe"
    }
