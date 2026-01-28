import os, time, logging
from logging.handlers import TimedRotatingFileHandler

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse


# =========================================================
# LOGGING CONFIGURATION
# =========================================================

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app_errors.log")

# Pastikan folder logs tersedia
os.makedirs(LOG_DIR, exist_ok=True)

# Formatter log
LOG_FORMATTER = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# File handler (rotasi harian, simpan 7 hari)
file_handler = TimedRotatingFileHandler(
    LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8",
)
file_handler.setFormatter(LOG_FORMATTER)

# Stream handler (terminal)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(LOG_FORMATTER)

# Logger utama
logger = logging.getLogger("GlobalExceptionHandler")
logger.setLevel(logging.ERROR)

# Hindari duplicate handler saat reload (uvicorn --reload)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


# =========================================================
# EXCEPTION HANDLERS
# =========================================================

async def global_http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    """Handler untuk HTTPException (401, 403, 404, dll)."""

    # Hitung durasi request (jika middleware tersedia)
    duration = "N/A"
    if hasattr(request.state, "start_time"):
        duration = f"{time.perf_counter() - request.state.start_time:.4f}s"

    client_ip = request.client.host if request.client else "Unknown"
    user_agent = request.headers.get("user-agent", "Unknown")

    logger.error(
        "HTTP_ERROR | IP=%s | Method=%s | Path=%s | Status=%s | "
        "Detail=%s | Duration=%s | UA=%s",
        client_ip,
        request.method,
        request.url.path,
        exc.status_code,
        exc.detail,
        duration,
        user_agent,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "data": None,
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    """Handler untuk error tak terduga (500 Internal Server Error)."""

    client_ip = request.client.host if request.client else "Unknown"

    logger.critical(
        "CRITICAL_ERROR | IP=%s | Path=%s | ErrorType=%s | Message=%s",
        client_ip,
        request.url.path,
        type(exc).__name__,
        str(exc),
        exc_info=True,  # simpan traceback
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": (
                "Terjadi kesalahan internal pada server. "
                "Tim kami sedang menanganinya."
            ),
            "data": None,
        },
    )


# =========================================================
# SETUP FUNCTION
# =========================================================

def setup_exception_handlers(app: FastAPI) -> None:
    """Daftarkan seluruh global exception handler ke FastAPI."""
    app.add_exception_handler(HTTPException, global_http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)