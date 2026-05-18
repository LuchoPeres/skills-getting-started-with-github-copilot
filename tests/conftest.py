import copy

import httpx
import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = original_activities


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client