"""Entrypoint of backend API exposing the FastAPI `app` to be served by an application server such as uvicorn."""

from .api.user import api as user_api
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
    ResourceExistsException,
)


from .api import (
    user,
    organization,
    static_files,
)

description = """
Welcome to the **Secondary School Portal** RESTful Application Programming Interface.
"""

# Metadata to improve the usefulness of OpenAPI Docs /docs API Explorer
app = FastAPI(
    title="Senior Secondary School (SSS) Portal",
    version="0.0.1",
    description=description,
    openapi_tags=[
        user.openapi_tags,
        organization.openapi_tags,
        # post.openapi_tags,
        # google_auth.openapi_tags
    ],
)

# Use GZip middleware for compressing HTML responses over the network
app.add_middleware(GZipMiddleware)

# Define CORS settings
origins = [
    "http://localhost:1601",  # Another example if React is on a different port
]

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Plugging in each of the router APIs
feature_apis = [user, organization]

for feature_api in feature_apis:
    app.include_router(feature_api.api)

# Static file mount used for serving React front-end in production, as well as static assets
app.mount("/", static_files.StaticFileMiddleware(directory=Path("./static")))


@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_exception_handler(
    request: Request, exc: ResourceNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(UserPermissionException)
async def user_permission_exception_handler(
    request: Request, exc: UserPermissionException
):
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc)},
    )


@app.exception_handler(ResourceExistsException)
async def resource_exists_exception_handler(
    request: Request, exc: ResourceExistsException
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


app.include_router(user_api)
