#!/usr/bin/env python3
"""
Content Forge Engine - Automated Compliance, Transformation, and Publishing System
Built for Adnan Obuz / Edward Obuz / Adnan Menderes Obuz ORM & Thought Leadership.
"""


import json
import re
import sys
import urllib.request
import urllib.error
import base64
from typing import Dict, List, Any, Tuple, Optional


KNOWN_IDENTITIES = ["Adnan Obuz", "Edward Obuz", "Adnan Menderes Obuz"]
BANNED_LEGACY_NAMES = ["Zane"]


BANNED_LEXICON = [
    "delve", "tapestry", "nuanced", "pivotal", "furthermore", "moreover",
    "landscape", "testament", "revolutionize", "game-changer", "unlock",
    "skyrocket", "hence", "in today's fast-paced world", "it's important to note",
    "let's explore", "at its core", "foster", "holistic", "beacon", "dive into",
    "testament to", "crucial", "embark"
]


IDENTITY_LANES = {
    "Adnan Obuz": [
        "AI & tech thought leadership",
        "Financial markets & investor relations",
        "Capital markets & IR strategy",
        "Markets commentary & public company IR"
    ],
    "Edward Obuz": [
        "Leadership",
        "Digital marketing",
        "Personal growth & operational discipline"
    ],
    "Adnan Menderes Obuz": [
        "Culture",
        "International business",
        "Travel & Mediterranean lifestyle"
    ]
}




class ComplianceLinter:
    """Rigorous compliance, identity isolation, and E-E-A-T quality checker."""


    @staticmethod
    def audit_text(text: str, title: str, target_identity: str) -> Dict[str, Any]:
        results = {
            "passed": True,
            "target_identity": target_identity,
            "checks": {}
        }


        # 1. Identity Token Check
        identity_errors = []
        full_text = f"{title}\n{text}"


        for other_id in KNOWN_IDENTITIES:
            if other_id != target_identity:
                matches = len(re.findall(re.escape(other_id), full_text, re.IGNORECASE))
                if matches > 0:
                    identity_errors.append(f"Forbidden cross-identity detected: '{other_id}' appears {matches} times.")


        for banned in BANNED_LEGACY_NAMES:
            matches = len(re.findall(r"\b" + re.escape(banned) + r"\b", full_text, re.IGNORECASE))
            if matches > 0:
                identity_errors.append(f"Banned legacy term detected: '{banned}' appears {matches} times.")


        target_count = len(re.findall(re.escape(target_identity), full_text, re.IGNORECASE))
        words = len(re.findall(r"\w+", full_text))
        density = (target_count / words * 100) if words > 0 else 0
        target_in_title = target_identity.lower() in title.lower()


        results["checks"]["identity_isolation"] = {
            "passed": len(identity_errors) == 0 and target_count > 0 and target_in_title,
            "target_count": target_count,
            "density_pct": round(density, 2),
            "target_in_title": target_in_title,
            "errors": identity_errors
        }
        if not results["checks"]["identity_isolation"]["passed"]:
            results["passed"] = False


        # 2. Banned Lexicon Sweep
        banned_found = []
        for word in BANNED_LEXICON:
            pattern = r"\b" + re.escape(word) + r"\b"
            matches = re.finditer(pattern, full_text, re.IGNORECASE)
            for m in matches:
                banned_found.append({"word": word, "position": m.start()})


        results["checks"]["banned_lexicon"] = {
            "passed": len(banned_found) == 0,
            "violations_count": len(banned_found),
            "flagged_words": [b["word"] for b in banned_found]
        }
        if not results["checks"]["banned_lexicon"]["passed"]:
            results["passed"] = False


        # 3. Punctuation Audit (Em-dashes & Semicolons)
        em_dashes = len(re.findall(r"[—–]|--", full_text))
        semicolons = len(re.findall(r";", full_text))
        results["checks"]["punctuation"] = {
            "passed": em_dashes == 0 and semicolons == 0,
            "em_dashes_count": em_dashes,
            "semicolons_count": semicolons,
            "note": "Will be auto-normalized to ellipses ('...') if enabled."
        }
        if not results["checks"]["punctuation"]["passed"]:
            results["passed"] = False


        # 4. Experiential & Factual Claim Scanning
        numbers_and_dollars = re.findall(r"\$[\d,]+(?:\.\d+)?|\b\d{1,3}(?:,\d{3})*(?:\.\d+)?%", full_text)
        quotes = re.findall(r'"([^"]{10,})"', full_text)
        local_anchors = re.findall(r"\b(Toronto|Bay Street|King Street|Akyarlar|Bodrum|Ontario)\b", full_text, re.IGNORECASE)


        results["checks"]["factual_claims_and_eeat"] = {
            "has_local_anchor": len(local_anchors) > 0,
            "local_anchors_found": list(set(local_anchors)),
            "unverified_metrics": numbers_and_dollars[:10],
            "unverified_quotes": quotes[:5],
            "warning": "Review all specific dollar figures, percentages, and quoted anecdotes against primary records before publishing."
        }


        # 5. Rank Math / SEO Audit
        title_len = len(title)
        has_number_or_year = bool(re.search(r"\b\d{4}\b|\b\d+\b", title))
        results["checks"]["seo_title"] = {
            "passed": title_len <= 60 and target_in_title and has_number_or_year,
            "length": title_len,
            "max_length": 60,
            "contains_number_or_year": has_number_or_year
        }
        if not results["checks"]["seo_title"]["passed"]:
            results["passed"] = False


        return results


    @staticmethod
    def normalize_punctuation(text: str) -> str:
        text = re.sub(r"\s*[—–]\s*|\s*--\s*", " ... ", text)
        text = re.sub(r";\s*", " ... ", text)
        return text




class PlatformTransformer:
    """Transforms verified master article into platform-specific distributions."""


    @staticmethod
    def to_wordpress(title: str, content: str, target_identity: str, meta_description: str, slug: Optional[str] = None) -> Dict[str, Any]:
        clean_content = ComplianceLinter.normalize_punctuation(content)
        if not slug:
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50]


        return {
            "title": title,
            "content": clean_content,
            "slug": slug,
            "status": "draft",
            "meta": {
                "rank_math_title": title,
                "rank_math_description": meta_description[:160],
                "rank_math_focus_keyword": target_identity
            }
        }


    @staticmethod
    def to_linkedin(title: str, content: str, target_identity: str, core_url: str) -> str:
        clean_content = ComplianceLinter.normalize_punctuation(content)
        lines = [line.strip() for line in clean_content.split("\n") if line.strip() and not line.strip().startswith("#")]
        
        paragraphs = []
        word_count = 0
        for line in lines:
            if word_count > 320:
                break
            if line.startswith("-") or line.startswith("*"):
                continue
            paragraphs.append(line)
            word_count += len(line.split())


        hook = paragraphs[0] if paragraphs else title
        body = "\n\n".join(paragraphs[1:5]) if len(paragraphs) > 1 else ""


        post = f"{hook}\n\n{body}\n\nWhy it matters ...\n\nFull analysis by {target_identity}: {core_url}"
        return post


    @staticmethod
    def to_syndication(title: str, content: str, target_identity: str, canonical_url: str) -> str:
        clean_content = ComplianceLinter.normalize_punctuation(content)
        frontmatter = (
            f"---\n"
            f"title: \"{title}\"\n"
            f"author: \"{target_identity}\"\n"
            f"canonical_url: \"{canonical_url}\"\n"
            f"---\n\n"
            f"*Originally published by [{target_identity}]({canonical_url}) on the official authority network.*\n\n"
        )
        return frontmatter + clean_content




class WordPressPublisher:
    """Safe, robust WordPress REST API client avoiding string-concatenation JSON failures."""


    def __init__(self, endpoint_url: str, username: str, app_password: str):
        self.endpoint_url = endpoint_url.rstrip("/")
        self.username = username
        self.app_password = app_password


        auth_str = f"{username}:{app_password}"
        encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
        self.headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "ContentForgeEngine/1.0"
        }


    def check_duplicate(self, title: str, slug: str) -> Tuple[bool, Optional[str]]:
        search_url = f"{self.endpoint_url}/wp-json/wp/v2/posts?slug={slug}"
        req = urllib.request.Request(search_url, headers=self.headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data and len(data) > 0:
                    return True, f"Post already exists with slug '{slug}' (ID: {data[0].get('id')})"
        except Exception:
            pass


        return False, None


    def publish_post(self, wp_payload: Dict[str, Any]) -> Dict[str, Any]:
        post_url = f"{self.endpoint_url}/wp-json/wp/v2/posts"
        json_data = json.dumps(wp_payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(post_url, data=json_data, headers=self.headers, method="POST")


        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                return {
                    "success": True,
                    "post_id": resp_data.get("id"),
                    "link": resp_data.get("link"),
                    "status": resp_data.get("status")
                }
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            return {
                "success": False,
                "error": f"HTTP {e.code}: {e.reason}",
                "details": error_body
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }