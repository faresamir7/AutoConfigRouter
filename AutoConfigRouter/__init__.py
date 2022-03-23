"""Top-level package for AutoConfigRouter."""
# AutoConfigRouter/__init__.py

__app_name__ = "AutoConfigRouter"
__version__ = "0.1.0"

(
    SUCCESS,
    CONNECTION_ERROR,
    CREDENTIAL_ERROR,
    SESSION_ERROR,
    VENDOR_ERROR,
    OBJECT_ERROR,
    FILEREAD_ERROR,
    DIR_ERROR
) = range(8)

ERRORS = {
    CONNECTION_ERROR: "connection to router error",
    CREDENTIAL_ERROR: "credentials error",
    SESSION_ERROR: "session error",
    VENDOR_ERROR: "vendor error",
    OBJECT_ERROR: "object error",
    FILEREAD_ERROR: "file read error",
    DIR_ERROR: "directory error"
}