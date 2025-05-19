import re
from flask import abort


def sanitise_path(filename):
    # Check for valid characters in the filename
    if not re.match(r'^[\w\-/\.]+$', filename):
        abort(400, description="Invalid filename")
    # Prevent path traversal
    if '..' in filename or filename.startswith('/'):
        abort(400, description="Invalid filename")
    # Always redirect to a relative path within the app
    new_path = f"/{filename.lstrip('/')}"
    return new_path
