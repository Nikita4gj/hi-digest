from fastapi import Request

from app.clients import HNClient

def _get_hn_client(request: Request) -> HNClient:
    return request.app.state.hn_cli
