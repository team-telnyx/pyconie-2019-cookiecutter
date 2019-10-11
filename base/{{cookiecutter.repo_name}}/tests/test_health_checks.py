"""
Test the health check endpoints
"""

async def test_health_check(test_client):
    resp = await test_client.get("/health")
    assert resp.status == 200
    text = await resp.text()
    assert '{"status": "OK"}' in text
