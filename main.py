
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP


async def health(request):
    return JSONResponse({"status": "ok"})


mcp = FastMCP(
    "python-booking-mcp-server",
    json_response=True,
    streamable_http_path="/",
)


@mcp.tool()
def ping() -> str:
    """Simple test tool."""
    return "pong"


@asynccontextmanager
async def lifespan(app):
    async with mcp.session_manager.run():
        yield


app = Starlette(
    routes=[
        Route("/health", health),
        Mount("/mcp", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

app = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],
)
