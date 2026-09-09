from pathlib import Path

from fastapi.responses import FileResponse, JSONResponse


def serve_frontend(build_dir: Path, full_path: str) -> FileResponse | JSONResponse:
    """Serve a frontend file or SPA fallback without escaping the build directory."""
    if full_path.startswith(("api/", "health")):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

    try:
        root = build_dir.resolve()
        static_file = (root / full_path).resolve()
        # Resolve first so both '..' and symlinks are checked against the real root.
        static_file.relative_to(root)
        if not static_file.is_file():
            static_file = (root / "index.html").resolve()
            static_file.relative_to(root)
            if not static_file.is_file():
                return JSONResponse(status_code=404, content={"detail": "Not Found"})
    except (OSError, RuntimeError, ValueError):
        # Includes invalid paths, symlink loops, and paths outside the build root.
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

    return FileResponse(str(static_file))
