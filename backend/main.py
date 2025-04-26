"""Entrypoint of backend API exposing the FastAPI `app` to be served by an application server such as uvicorn."""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from .api import (
    # user,
    static_files,
    # post,
    # google_auth
)

description = """
Welcome to the **My Fun App** RESTful Application Programming Interface.
"""

# Metadata to improve the usefulness of OpenAPI Docs /docs API Explorer
app = FastAPI(
    title="MyFun",
    version="0.0.1",
    description=description,
    openapi_tags=[
        # user.openapi_tags,
        # post.openapi_tags,
        # google_auth.openapi_tags
    ],
)

# Use GZip middleware for compressing HTML responses over the network
app.add_middleware(GZipMiddleware)

# Define CORS settings
origins = [
    "http://localhost:1532",   # Another example if React is on a different port
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
# feature_apis = [user, post, google_auth]
feature_apis = []

for feature_api in feature_apis:
    app.include_router(feature_api.api)

# Static file mount used for serving React front-end in production, as well as static assets
app.mount("/", static_files.StaticFileMiddleware(directory=Path("./static")))


# Add application-wide exception handling middleware for commonly encountered API Exceptions
# @app.exception_handler(UserPermissionException)
# def permission_exception_handler(request: Request, e: UserPermissionException):
#     return JSONResponse(status_code=403, content={"message": str(e)})


# @app.exception_handler(ResourceNotFoundException)
# def resource_not_found_exception_handler(
#     request: Request, e: ResourceNotFoundException
# ):
#     return JSONResponse(status_code=404, content={"message": str(e)})
