"""
Development server launcher.

Usage:
    uv run python run.py
    python run.py          # debugger 直接启动也可以
"""
import uvicorn


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=8006)


if __name__ == "__main__":
    main()
