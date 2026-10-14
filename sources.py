"""
Where the monitor reads tools from: GitHub, GitLab (gitlab.com and self-hosted instances such as
the ETSI Forge), Zenodo, PyPI and, for discovery of packages, Libraries.io.

Every source can say whether a link is one of its own (`key`), read one tool (`tool`) and search
for new ones (`search`). A tool is a dict with the fields below; a field the source cannot know
is None and is left alone in the Excel file.

  url, archived, stars, language, license (SPDX ID), last_commit (YYYY-MM-DD), release
  ("v1.2 (YYYY-MM-DD)"), activity (date of the last commit or release), docker (Dockerfile or
  compose file in the root), keys (other keys of the same tool, e.g. its GitHub repository)

A search result is a dict: key, name, url, description, language, license, stars, pushed, fork,
archived, topics, source, keys.
"""
from __future__ import annotations

import html
import re
import time
from urllib.parse import quote, urlsplit

import httpx

UA = {"User-Agent": "harmoniqci-t51-monitor"}
DOCKER = re.compile(r"^(dockerfile.*|.*\.dockerfile|(docker-)?compose(\.[\w-]+)?\.ya?ml)$", re.I)
GITHUB = re.compile(r"^https?://(?:www\.)?github\.com/([^/\s]+)/([^/\s#?]+)", re.I)
ZENODO = re.compile(r"^https?://(?:www\.)?zenodo\.org/(?:records?|record)/(\d+)", re.I)
ZENODO_DOI = re.compile(r"10\.5281/zenodo\.(\d+)", re.I)
PYPI = re.compile(r"^https?://(?:www\.)?pypi\.org/project/([^/\s#?]+)", re.I)
# GitLab licence keys -> SPDX IDs (the others are kept upper-cased)
GITLAB_LICENSES = {"mit": "MIT", "apache-2.0": "Apache-2.0", "gpl-2.0": "GPL-2.0", "gpl-3.0": "GPL-3.0",
                   "lgpl-2.1": "LGPL-2.1", "lgpl-3.0": "LGPL-3.0", "agpl-3.0": "AGPL-3.0",
                   "bsd-2-clause": "BSD-2-Clause", "bsd-3-clause": "BSD-3-Clause", "mpl-2.0": "MPL-2.0",
                   "eupl-1.2": "EUPL-1.2", "unlicense": "Unlicense", "epl-2.0": "EPL-2.0"}


class SourceError(Exception):
    """A source could not be reached or refused; the run goes on without it."""


def pypi_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def date(value) -> str:
    return str(value or "")[:10]


def url_key(url) -> str | None:
    """A key that identifies a tool whatever form its link has."""
    url = str(url or "").strip()
    if m := GITHUB.match(url):
        return f"github.com/{m.group(1)}/{m.group(2).removesuffix('.git')}".lower()
    if (m := ZENODO.match(url)) or (m := ZENODO_DOI.search(url)):
        return f"zenodo:{m.group(1)}"
    if m := PYPI.match(url):
        return f"pypi:{pypi_name(m.group(1))}"
    parts = urlsplit(url)
    if not parts.netloc:
        return None
    path = parts.path.split("/-/")[0].rstrip("/").removesuffix(".git")
    return f"{parts.netloc.lower().removeprefix('www.')}{path.lower()}"


class Http:
    def __init__(self, base: str, headers: dict | None = None, transport=None, name: str = "") -> None:
        self.name = name
        self.client = httpx.Client(base_url=base, headers={**UA, **(headers or {})}, timeout=30,
                                   transport=transport, follow_redirects=True)

    def get(self, path: str, missing=(404, 410, 451), **params):
        """JSON of a GET, None for a missing resource; SourceError when the source fails."""
        try:
            r = self.client.get(path, params=params or None)
        except httpx.HTTPError as exc:
            raise SourceError(f"{self.name} not reachable ({type(exc).__name__})") from exc
        if r.status_code in missing:
            return None
        if r.status_code >= 400:
            raise SourceError(f"{self.name} answered HTTP {r.status_code}")
        return r.json()


# ---------------------------------------------------------------------------------------- GitHub

class GitHub:
    name = "GitHub"

    def __init__(self, token: str | None = None, transport=None, sleep=time.sleep) -> None:
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", **UA}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.http = httpx.Client(base_url="https://api.github.com", headers=headers, timeout=30,
                                 transport=transport, follow_redirects=True)
        self.sleep = sleep

    def get(self, path: str, **params):
        """JSON of a GET, None on 404/409/451 (no such repo, empty repo, blocked). Waits out a
        rate limit when it resets within two minutes."""
        for _ in range(3):
            try:
                r = self.http.get(path, params=params or None)
            except httpx.HTTPError as exc:
                raise SourceError(f"GitHub not reachable ({type(exc).__name__})") from exc
            if r.status_code in (403, 429) and r.headers.get("x-ratelimit-remaining") == "0":
                wait = int(r.headers.get("x-ratelimit-reset", "0")) - int(time.time()) + 1
                if 0 < wait <= 120:
                    self.sleep(wait)
                    continue
                raise SystemExit("GitHub rate limit reached: set GITHUB_TOKEN and run again")
            if r.status_code in (404, 409, 451):
                return None
            if r.status_code >= 400:
                raise SourceError(f"GitHub answered HTTP {r.status_code} for {path}")
            return r.json()
        raise SystemExit(f"GitHub kept refusing {path}")

    @staticmethod
    def key(url) -> str | None:
        return url_key(url) if GITHUB.match(str(url or "").strip()) else None

    def tool(self, url: str) -> dict | None:
        name = self.key(url).removeprefix("github.com/")
        info = self.get(f"/repos/{name}")
        if info is None:
            return None
        commits = self.get(f"/repos/{name}/commits", sha=info.get("default_branch") or "HEAD", per_page=1) or []
        release = self.get(f"/repos/{name}/releases/latest")
        files = self.get(f"/repos/{name}/contents/") or []
        lic = (info.get("license") or {}).get("spdx_id")
        last = date(commits[0]["commit"]["committer"]["date"]) if commits else date(info.get("pushed_at"))
        return {"url": info.get("html_url"), "archived": bool(info.get("archived")),
                "stars": info.get("stargazers_count", 0), "language": info.get("language"),
                "license": None if lic in (None, "NOASSERTION") else lic, "last_commit": last,
                "release": f"{release['tag_name']} ({date(release['published_at'])})"
                if release and release.get("published_at") else "",
                "activity": last, "docker": any(DOCKER.match(f.get("name", "")) for f in files if isinstance(f, dict)),
                "keys": set()}

    def search(self, query: str, n: int) -> list[dict]:
        found = self.get("/search/repositories", q=query, sort="updated", order="desc", per_page=n) or {}
        out = []
        for item in found.get("items", []):
            lic = (item.get("license") or {}).get("spdx_id")
            out.append({"key": url_key(item["html_url"]), "name": item["full_name"], "url": item["html_url"],
                        "description": item.get("description") or "", "language": item.get("language") or "",
                        "license": "" if lic in (None, "NOASSERTION") else lic,
                        "stars": item.get("stargazers_count", 0), "pushed": date(item.get("pushed_at")),
                        "fork": bool(item.get("fork")), "archived": bool(item.get("archived")),
                        "topics": item.get("topics", []), "source": self.name, "keys": set()})
        return out


# ---------------------------------------------------------------------------------------- GitLab

class GitLab:
    """gitlab.com or a self-hosted GitLab, e.g. https://forge.etsi.org/rep (the ETSI Forge)."""

    def __init__(self, base: str, token: str | None = None, transport=None) -> None:
        self.base = base.rstrip("/")
        parts = urlsplit(self.base)
        self.prefix = f"{parts.netloc.lower().removeprefix('www.')}{parts.path.lower()}"
        self.name = f"GitLab ({parts.netloc}{parts.path})"
        self.http = Http(self.base + "/api/v4", {"PRIVATE-TOKEN": token} if token else None, transport, self.name)

    def key(self, url) -> str | None:
        k = url_key(url)
        return k if k and k.startswith(self.prefix + "/") and k.count("/") >= self.prefix.count("/") + 2 else None

    def _path(self, url: str) -> str:
        parts = urlsplit(str(url).strip())
        path = parts.path.split("/-/")[0].rstrip("/").removesuffix(".git")
        return path[len(urlsplit(self.base).path):].strip("/")

    def tool(self, url: str) -> dict | None:
        pid = quote(self._path(url), safe="")
        info = self.http.get(f"/projects/{pid}", license="true")
        if info is None:
            return None
        commits = self.http.get(f"/projects/{pid}/repository/commits", per_page=1) or []
        releases = self.http.get(f"/projects/{pid}/releases", per_page=1, missing=(403, 404)) or []
        files = self.http.get(f"/projects/{pid}/repository/tree", per_page=100) or []
        langs = self.http.get(f"/projects/{pid}/languages", missing=(403, 404)) or {}
        lic = (info.get("license") or {}).get("key")
        last = date(commits[0].get("committed_date")) if commits else date(info.get("last_activity_at"))
        rel = releases[0] if releases else None
        return {"url": info.get("web_url"), "archived": bool(info.get("archived")),
                "stars": info.get("star_count", 0), "language": max(langs, key=langs.get) if langs else None,
                "license": GITLAB_LICENSES.get(lic, lic.upper()) if lic and lic != "other" else None,
                "last_commit": last,
                "release": f"{rel['tag_name']} ({date(rel.get('released_at'))})" if rel else "",
                "activity": last, "docker": any(DOCKER.match(f.get("name", "")) for f in files if isinstance(f, dict)),
                "keys": set()}

    def search(self, query: str, n: int) -> list[dict]:
        found = self.http.get("/projects", search=query, order_by="last_activity_at", sort="desc",
                              per_page=n, visibility="public") or []
        return [{"key": url_key(p["web_url"]), "name": p.get("path_with_namespace") or p.get("name"),
                 "url": p["web_url"], "description": p.get("description") or "", "language": "",
                 "license": "", "stars": p.get("star_count", 0), "pushed": date(p.get("last_activity_at")),
                 "fork": bool(p.get("forked_from_project")), "archived": bool(p.get("archived")),
                 "topics": p.get("topics") or p.get("tag_list") or [], "source": self.name, "keys": set()}
                for p in found]


# ---------------------------------------------------------------------------------------- Zenodo

def _text(value) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", str(value or "")))).strip()


def _related(meta: dict) -> set[str]:
    """Keys of the repositories a Zenodo record points to (e.g. the GitHub release it archives)."""
    return {k for r in meta.get("related_identifiers") or [] if (k := url_key(r.get("identifier")))
            and k.startswith(("github.com/", "gitlab."))}


class Zenodo:
    name = "Zenodo"

    def __init__(self, token: str | None = None, transport=None) -> None:
        self.http = Http("https://zenodo.org/api", {"Authorization": f"Bearer {token}"} if token else None,
                         transport, self.name)

    @staticmethod
    def key(url) -> str | None:
        k = url_key(url)
        return k if k and k.startswith("zenodo:") else None

    def tool(self, url: str) -> dict | None:
        rec = self.http.get(f"/records/{self.key(url).split(':')[1]}")
        if rec is None:
            return None
        latest = (rec.get("links") or {}).get("latest")
        if latest and not latest.endswith(f"/{rec.get('id')}"):
            rec = self.http.get("/records/" + latest.rstrip("/").split("/")[-1]) or rec
        meta = rec.get("metadata") or {}
        lic = (meta.get("license") or {}).get("id")
        published = date(meta.get("publication_date"))
        return {"url": None, "archived": None, "stars": None, "language": None,
                "license": lic.upper() if lic and len(lic) <= 4 else (lic or None), "last_commit": None,
                "release": f"{meta.get('version') or 'record ' + str(rec.get('id'))} ({published})",
                "activity": published, "docker": None,
                "keys": {f"zenodo:{rec.get('conceptrecid')}"} | _related(meta) if rec.get("conceptrecid") else _related(meta)}

    def search(self, query: str, n: int) -> list[dict]:
        found = self.http.get("/records", q=query, type="software", sort="mostrecent", size=n) or {}
        out = []
        for rec in (found.get("hits") or {}).get("hits", []):
            meta = rec.get("metadata") or {}
            concept = rec.get("conceptrecid") or rec.get("id")
            lic = (meta.get("license") or {}).get("id")
            out.append({"key": f"zenodo:{concept}", "name": meta.get("title") or f"Zenodo {concept}",
                        "url": f"https://zenodo.org/records/{concept}", "description": _text(meta.get("description")),
                        "language": "", "license": lic or "", "stars": (rec.get("stats") or {}).get("unique_downloads", ""),
                        "pushed": date(meta.get("publication_date") or rec.get("updated")), "fork": False,
                        "archived": False, "topics": meta.get("keywords") or [], "source": self.name,
                        "keys": _related(meta)})
        return out


# ------------------------------------------------------------------------------------------ PyPI

class PyPI:
    """Python packages. PyPI has no search API: new packages come from Libraries.io."""
    name = "PyPI"

    def __init__(self, transport=None) -> None:
        self.http = Http("https://pypi.org", None, transport, self.name)

    @staticmethod
    def key(url) -> str | None:
        k = url_key(url)
        return k if k and k.startswith("pypi:") else None

    def tool(self, url: str) -> dict | None:
        data = self.http.get(f"/pypi/{self.key(url).split(':')[1]}/json")
        if data is None:
            return None
        info = data.get("info") or {}
        version = info.get("version") or ""
        files = (data.get("releases") or {}).get(version) or data.get("urls") or []
        uploaded = date(files[0].get("upload_time")) if files else ""
        lic = info.get("license_expression") or info.get("license") or ""
        repo = next((k for u in (info.get("project_urls") or {}).values()
                     if (k := url_key(u)) and k.startswith("github.com/")), None)
        return {"url": None, "archived": None, "stars": None, "language": "Python",
                "license": lic if lic and len(lic) <= 40 and "\n" not in lic else None, "last_commit": None,
                "release": f"{version} ({uploaded})" if version else "", "activity": uploaded, "docker": None,
                "keys": {repo} if repo else set()}


class LibrariesIO:
    """Search of packages (PyPI and others) through Libraries.io; needs a free API key."""
    name = "Libraries.io"

    def __init__(self, api_key: str, platforms: str = "PyPI", transport=None) -> None:
        self.http = Http("https://libraries.io/api", None, transport, self.name)
        self.api_key, self.platforms = api_key, platforms

    def search(self, query: str, n: int) -> list[dict]:
        found = self.http.get("/search", q=query, platforms=self.platforms, per_page=n, api_key=self.api_key) or []
        out = []
        for p in found:
            url = p.get("package_manager_url") or f"https://pypi.org/project/{p.get('name')}/"
            repo = url_key(p.get("repository_url")) if p.get("repository_url") else None
            out.append({"key": url_key(url), "name": f"{p.get('name')} ({p.get('platform', self.platforms)})",
                        "url": url, "description": p.get("description") or "", "language": p.get("language") or "",
                        "license": p.get("normalized_licenses", [""])[0] if p.get("normalized_licenses") else "",
                        "stars": p.get("stars", 0),
                        "pushed": date(p.get("latest_release_published_at") or p.get("latest_stable_release_published_at")),
                        "fork": False, "archived": False, "topics": p.get("keywords") or [],
                        "source": f"{self.name} ({p.get('platform', self.platforms)})", "keys": {repo} if repo else set()})
        return out


# ------------------------------------------------------------------------------------- all of them

class Sources:
    """The sources a run uses, built from config.yaml and the tokens in the environment."""

    def __init__(self, cfg: dict, env: dict, transport=None, sleep=time.sleep) -> None:
        disc = cfg.get("discovery") or {}
        self.github = GitHub(env.get("GITHUB_TOKEN"), transport, sleep)
        gl = disc.get("gitlab") or {}
        self.gitlabs = [GitLab(h, env.get("GITLAB_TOKEN") if "gitlab.com" in h else None, transport)
                        for h in gl.get("hosts", ["https://gitlab.com"])]
        self.zenodo = Zenodo(env.get("ZENODO_TOKEN"), transport)
        self.pypi = PyPI(transport)
        lib = disc.get("librariesio") or {}
        self.librariesio = (LibrariesIO(env["LIBRARIES_IO_KEY"], lib.get("platforms", "PyPI"), transport)
                            if env.get("LIBRARIES_IO_KEY") else None)
        self.transport = transport

    def for_url(self, url):
        """The source that knows this link, or None (then only the page is checked)."""
        for s in [self.github, *self.gitlabs, self.zenodo, self.pypi]:
            if s.key(url):
                return s
        return None

    def searches(self, cfg: dict) -> list[tuple[object, list[str]]]:
        disc = cfg.get("discovery") or {}
        github = disc.get("github") or disc.get("queries") or []
        out = [(self.github, github)]
        out += [(g, (disc.get("gitlab") or {}).get("queries", [])) for g in self.gitlabs]
        out.append((self.zenodo, disc.get("zenodo") or []))
        if self.librariesio:
            out.append((self.librariesio, (disc.get("librariesio") or {}).get("queries", [])))
        return [(s, q) for s, q in out if q]


def page_status(url: str, transport=None) -> str:
    """'online' or why not, for a tool that no source knows."""
    try:
        with httpx.Client(timeout=20, follow_redirects=True, transport=transport, headers=UA) as c:
            r = c.get(url)
        return "online" if r.status_code < 400 else f"HTTP {r.status_code}"
    except httpx.HTTPError as exc:
        return f"not reachable ({type(exc).__name__})"
