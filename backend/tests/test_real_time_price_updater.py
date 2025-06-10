import pytest
import asyncio
from unittest.mock import AsyncMock, patch
import json
import sys
sys.path.append("../")
import aiohttp
from backend.app.services.real_time_price_updater import RealTimePriceUpdater

@pytest.fixture
async def updater():
    updater = RealTimePriceUpdater()
    yield updater
    await updater.close()

@pytest.mark.asyncio
async def test_initialize(updater):
    with patch('aiohttp.ClientSession.ws_connect', new_callable=AsyncMock) as mock_ws_connect:
        mock_ws = AsyncMock()
        mock_ws_connect.return_value = mock_ws
        await updater.initialize()
        assert updater.session is not None
        assert updater.ws is not None
        mock_ws_connect.assert_called_once_with(updater.websocket_url)

@pytest.mark.asyncio
async def test_close(updater):
    with patch('aiohttp.ClientSession.ws_connect', new_callable=AsyncMock) as mock_ws_connect:
        mock_ws = AsyncMock()
        mock_ws_connect.return_value = mock_ws
        await updater.initialize()
        await updater.close()
        assert updater.ws is None or updater.ws.closed
        assert updater.session is None or updater.session.closed
        mock_ws.close.assert_called_once()

@pytest.mark.asyncio
async def test_process_update(updater):
    test_data = {
        'product_id': 'TEST123',
        'price': 99.99,
        'timestamp': '2025-06-10T12:00:00Z',
        'source': 'TestSource'
    }
    with patch.object(updater, 'store_update', new_callable=AsyncMock) as mock_store:
        await updater.process_update(test_data)
        mock_store.assert_called_once_with('TEST123', 99.99, '2025-06-10T12:00:00Z', 'TestSource')

@pytest.mark.asyncio
async def test_listen_for_updates(updater):
    with patch('aiohttp.ClientSession.ws_connect', new_callable=AsyncMock) as mock_ws_connect:
        mock_ws = AsyncMock()
        mock_ws_connect.return_value = mock_ws
        mock_msg = AsyncMock()
        mock_msg.type = aiohttp.WSMsgType.TEXT
        mock_msg.data = json.dumps({
            'product_id': 'TEST123',
            'price': 99.99,
            'timestamp': '2025-06-10T12:00:00Z'
        })
        mock_ws.receive.side_effect = [mock_msg, AsyncMock(type=aiohttp.WSMsgType.CLOSED)]
        with patch.object(updater, 'process_update', new_callable=AsyncMock) as mock_process:
            await updater.listen_for_updates()
            mock_process.assert_called_once()
