#!/usr/bin/env python3
"""Local LFS Batch API shim for the Claude Code on the Web (CCW) sandbox.

CCW pipes the repo's git remote through a local HTTP proxy
(127.0.0.1:<port>, sentinel auth `local_proxy@...`) that knows the git
smart-HTTP routes -- `info/refs`, `git-upload-pack`, `git-receive-pack`
-- and rejects everything else with HTTP 502 and "Proxy error: invalid
git path".  Git LFS adds two more routes on top of the same base URL
(`info/lfs/objects/batch`, `info/lfs/locks/verify`) which the proxy
doesn't recognise, so `git lfs pull` / `git lfs push` blow up before
any blob bytes move.

Direct HTTPS to github.com works from inside the sandbox (the proxy is
specifically for *git auth*, not general network egress), so the
workaround is to point `lfs.url` at a local shim that forwards the LFS
batch protocol direct to github.com and stays out of the local_proxy
entirely.  GitHub's LFS batch endpoint returns presigned URLs for the
actual blob storage at `*.githubusercontent.com`, which git-lfs then
fetches directly -- those don't need auth and don't need the proxy.

Anonymous LFS *download* of a public repo's objects works end-to-end
with this shim.  *Upload* requires a GitHub token (the local_proxy has
one but doesn't expose it); the shim forwards the upload batch request
verbatim and returns whatever github.com says, which for anonymous
requests is HTTP 401.  Set GITHUB_TOKEN in the environment to make
uploads work.

Usage:

    # foreground (Ctrl-C to stop):
    python3 tools/lfs_proxy.py --port 39946

    # configure git-lfs in this repo to use it:
    git config lfs.url http://127.0.0.1:39946/SupraSummus/hextrans-pak128.britain.git/info/lfs
    git config lfs.http://127.0.0.1:39946/SupraSummus/hextrans-pak128.britain.git/info/lfs.locksverify false

    # now `git lfs pull`, `git lfs fetch`, `git clone` (for an
    # LFS-using repo) work without going through local_proxy.

The shim is a single-file dependency-free HTTP server; it accepts paths
of the form `/<owner>/<repo>.git/info/lfs/...` so the same instance can
serve multiple repos.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG = logging.getLogger("lfs_proxy")

GITHUB_BASE = "https://github.com"
LFS_CONTENT_TYPE = "application/vnd.git-lfs+json"


def _forward_batch(owner: str, repo: str, body: bytes, token: str | None) -> tuple[int, bytes, str]:
    url = f"{GITHUB_BASE}/{owner}/{repo}.git/info/lfs/objects/batch"
    headers = {
        "Accept": LFS_CONTENT_TYPE,
        "Content-Type": LFS_CONTENT_TYPE,
    }
    if token:
        # GitHub accepts a PAT or installation token as Basic auth with
        # any non-empty username; `x-access-token` is the conventional
        # placeholder.
        import base64

        basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
        headers["Authorization"] = f"Basic {basic}"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read(), resp.headers.get("Content-Type", LFS_CONTENT_TYPE)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), exc.headers.get("Content-Type", LFS_CONTENT_TYPE)


class Handler(BaseHTTPRequestHandler):
    server_version = "lfs-proxy/0.1"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003 - stdlib hook name
        LOG.info("%s - " + fmt, self.address_string(), *args)

    def _split_path(self) -> tuple[str, str, str] | None:
        # /<owner>/<repo>.git/info/lfs/<rest>
        parts = self.path.lstrip("/").split("/", 3)
        if len(parts) < 4:
            return None
        owner, repo_dot_git, info, rest = parts
        if not repo_dot_git.endswith(".git") or info != "info":
            return None
        return owner, repo_dot_git[: -len(".git")], rest

    def _reply(self, status: int, body: bytes, content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802 - stdlib hook name
        split = self._split_path()
        if split is None:
            self._reply(404, b"unknown path\n", "text/plain")
            return
        owner, repo, rest = split

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b""

        if rest == "lfs/objects/batch":
            token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
            status, resp_body, ct = _forward_batch(owner, repo, body, token)
            LOG.info("batch %s/%s -> %s (%d bytes)", owner, repo, status, len(resp_body))
            self._reply(status, resp_body, ct)
            return

        if rest == "lfs/locks/verify":
            # git-lfs probes the locking API on every push; we don't
            # implement it.  Reply 200 with "locks disabled" payload so
            # git-lfs treats the remote as not-supporting-locking
            # without flagging it as a fatal error.  (See lfs-server
            # reference for the contract; an empty object also works.)
            self._reply(200, b'{"ours":[],"theirs":[]}', LFS_CONTENT_TYPE)
            return

        self._reply(404, f"unsupported route: {rest}\n".encode(), "text/plain")

    def do_GET(self) -> None:  # noqa: N802
        # Health check.
        if self.path == "/":
            self._reply(200, b"lfs-proxy ok\n", "text/plain")
            return
        self._reply(404, b"GET not implemented for LFS API\n", "text/plain")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=39946)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    LOG.info("listening on http://%s:%d", args.host, args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOG.info("stopping")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
