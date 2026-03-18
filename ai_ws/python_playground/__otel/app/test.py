from typing import Any, Optional
from datetime import datetime, timedelta
import aiohttp
from opentelemetry.metrics._internal.instrument import (
    Counter,
    Histogram,
    Gauge,
    UpDownCounter,
)

BASE_URL = "http://localhost:9090"
_timeout = 5
max_retires = 3
import asyncio

from opentelemetry import metrics


from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


async def query_instant(
    query: str, time: Optional[datetime] = None
) -> Optional[dict[str, Any]]:
    """
    Execute instant query

    Args:
        query: PromQL query string
        time: Query timestamp (default: now)

    Returns:
        Query result or None on error
    """
    url = f"{BASE_URL}/api/v1/query"
    params: dict[str, Any] = {"query": query}

    if time:
        params["time"] = time.timestamp()

    return await _query(url, params)


async def query_range(
    query: str, start: datetime, end: datetime, step: str = "1m"
) -> Optional[dict[str, Any]]:
    """
    Execute range query

    Args:
        query: PromQL query string
        start: Start timestamp
        end: End timestamp
        step: Query resolution (e.g., "10s", "1m", "5m")

    Returns:
        Query result or None on error
    """
    url = f"{BASE_URL}/api/v1/query_range"
    params: dict[str, Any] = {
        "query": query,
        "start": start.timestamp(),
        "end": end.timestamp(),
        "step": step,
    }

    return await _query(url, params)


async def _query(url: str, params: dict[str, Any]) -> Optional[dict[str, Any]]:
    """
    Execute query with retry and timeout

    Args:
        url: Query URL
        params: Query parameters

    Returns:
        Query result or None on error
    """
    print("DEBUG ", params)
    for attempt in range(max_retires + 1):
        try:
            timeout = aiohttp.ClientTimeout(total=_timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "success":
                            return data.get("data")
                        else:
                            print(f"Prometheus query failed: {data.get('error')}")
                            return None
                    else:
                        print(
                            f"Prometheus returned status {response.status}, body={data}"
                        )
                        if attempt < max_retires:
                            await asyncio.sleep(
                                0.1 * (2**attempt)
                            )  # Exponential backoff
                            continue
                        return None
        except asyncio.TimeoutError:
            print(f"Prometheus query timeout (attempt {attempt + 1}/{max_retires + 1})")
            if attempt < max_retires:
                await asyncio.sleep(0.1 * (2**attempt))
                continue
            return None
        except Exception as e:
            print(f"Prometheus query error: {e}")
            if attempt < max_retires:
                await asyncio.sleep(0.1 * (2**attempt))
                continue
            return None

    return None


async def run():
    otlp_endpoint = "http://localhost:4318"
    resource = Resource.create(
        {
            "service.name": "vaultcx-api",
            "service.version": "1.0",
            "deployment.env": "dev",
        }
    )

    # meta configuration
    meta_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=f"{otlp_endpoint}/v1/metrics"),
        export_interval_millis=5000,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[meta_reader])
    metrics.set_meter_provider(meter_provider)
    meter = metrics.get_meter("demo-meter")
    OTEL_REQS: UpDownCounter = meter.create_up_down_counter("ws_connections_1")
    for i in range(30):
        connect = i % 2 == 0
        print("is connect ", connect)
        OTEL_REQS.add(1 if connect else -1)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
