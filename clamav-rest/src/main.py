import logging
import os
import tempfile
from typing import Annotated

import httpx
import pyclamd
from fastapi import Depends, FastAPI, Response, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, HttpUrl

from .config import Settings

logger = logging.getLogger(__name__)

app = FastAPI()
settings = Settings()
header_scheme = APIKeyHeader(name="x-api-key")


@app.get("/")
def root():
    return {"ok": True}


class Scan(BaseModel):
    url: HttpUrl


@app.post("/scan")
def scan(
    input: Scan, api_key: Annotated[str, Depends(header_scheme)], response: Response
):
    if api_key != settings.api_key.get_secret_value():
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "Invalid API key"}

    url = str(input.url)
    temp_file = tempfile.NamedTemporaryFile(prefix="/tmp/clamav/")

    with httpx.stream("GET", url) as response:
        response.raise_for_status()
        for chunk in response.iter_bytes():
            temp_file.write(chunk)
            file_path = temp_file.name

    try:
        virus_scanner = pyclamd.ClamdNetworkSocket(port=3310, timeout=10)
        os.chmod(file_path, 774)
        result = virus_scanner.scan_file(file_path)
        virus_found = bool(result and result[file_path][0] == "FOUND")
    except pyclamd.ConnectionError:
        logger.exception("Could not connect to clamd server")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Could not connect to clamd server"}
    finally:
        temp_file.close()

    return {"virus": virus_found}
