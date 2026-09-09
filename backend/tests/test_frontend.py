import asyncio
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

from fastapi import FastAPI

from backend.app.frontend import serve_frontend


class FrontendServingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.build = self.base / "dist"
        self.build.mkdir()
        (self.build / "index.html").write_text("SPA page")
        (self.build / "robots.txt").write_text("public file")
        self.private = self.base / "private.txt"
        self.private.write_text("must not be served")
        self.app = FastAPI()

        @self.app.get("/{full_path:path}")
        async def frontend(full_path: str):
            return serve_frontend(self.build, full_path)

    def request(self, raw_path):
        async def run():
            messages = []

            async def receive():
                return {"type": "http.request", "body": b"", "more_body": False}

            async def send(message):
                messages.append(message)

            # ASGI servers supply a decoded path and the original raw_path.
            scope = {
                "type": "http", "asgi": {"version": "3.0"},
                "http_version": "1.1", "method": "GET", "scheme": "http",
                "path": unquote(raw_path), "raw_path": raw_path.encode(),
                "query_string": b"", "root_path": "", "headers": [],
                "client": ("127.0.0.1", 1234), "server": ("test", 80),
            }
            await self.app(scope, receive, send)
            status = next(m["status"] for m in messages if m["type"] == "http.response.start")
            body = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
            return status, body

        return asyncio.run(run())

    def test_public_file(self):
        self.assertEqual(self.request("/robots.txt"), (200, b"public file"))

    def test_spa_routes(self):
        for path in ("/", "/shop", "/product/123"):
            with self.subTest(path=path):
                self.assertEqual(self.request(path), (200, b"SPA page"))

    def test_parent_traversal(self):
        for path in ("/../private.txt", "/%2e%2e/private.txt", "/..%2fprivate.txt"):
            with self.subTest(path=path):
                status, body = self.request(path)
                self.assertEqual(status, 404)
                self.assertNotIn(b"must not be served", body)

    def test_absolute_path(self):
        self.assertEqual(self.request("/" + str(self.private))[0], 404)

    def test_sibling_directory_with_same_prefix(self):
        sibling = self.base / "dist-private"
        sibling.mkdir()
        (sibling / "private.txt").write_text("must not be served")
        self.assertEqual(self.request("/../dist-private/private.txt")[0], 404)

    def test_symlink_outside_build(self):
        (self.build / "linked.txt").symlink_to(self.private)
        self.assertEqual(self.request("/linked.txt")[0], 404)

    def test_symlink_inside_build(self):
        (self.build / "linked.txt").symlink_to(self.build / "robots.txt")
        self.assertEqual(self.request("/linked.txt"), (200, b"public file"))

    def test_fallback_symlink_outside_build(self):
        index = self.build / "index.html"
        index.unlink()
        index.symlink_to(self.private)
        self.assertEqual(self.request("/shop")[0], 404)

    def test_api_and_health_do_not_fall_back(self):
        for path in ("/api/missing", "/health/missing"):
            with self.subTest(path=path):
                self.assertEqual(self.request(path)[0], 404)

    def test_invalid_path(self):
        self.assertEqual(self.request("/bad%00path")[0], 404)

    def test_missing_index(self):
        (self.build / "index.html").unlink()
        self.assertEqual(self.request("/shop")[0], 404)


if __name__ == "__main__":
    unittest.main()
