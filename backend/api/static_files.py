"""Single-page application middleware.

Our application is organized as a single-page application (SPA). This middleware class
extends the functionality of the StaticFiles middleware and was inspired by: 
<https://stackoverflow.com/questions/63069190/how-to-capture-arbitrary-paths-at-one-route-in-fastapi>
"""

import os

from fastapi.staticfiles import StaticFiles


class StaticFileMiddleware(StaticFiles):
    def __init__(self, directory: os.PathLike, index: str = "index.html") -> None:
        self.index = index
        super().__init__(directory=directory, packages=None, html=True, check_dir=True)

    def lookup_path(self, path: str) -> tuple[str, os.stat_result | None]:
        """Returns the index file when no match is found.

        Args:
            path (str): Resource path.

        Returns:
            tuple[str, os.stat_result | None]: Returns a full path and stat result or None if file not found.
        """
        full_path, stat_result = super().lookup_path(path)

        if stat_result is None:
            full_path, stat_result = super().lookup_path(self.index)
            return (full_path, stat_result)
        else:
            return (full_path, stat_result)
