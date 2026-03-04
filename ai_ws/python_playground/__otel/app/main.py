import random
import time
from typing import Any, Final

from fastapi import FastAPI, HTTPException, Response
from prometheus_client import generate_latest
from pydantic import BaseModel
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
import os
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
)
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
import logging
from opentelemetry.metrics._internal.instrument import Counter, Histogram, Gauge, UpDownCounter

logger = logging.getLogger(__name__)

# from prometheus_client import Counter

# # ---------------------------
# # Prometheus-client metrics
# # ---------------------------
# PROM_REQS = PCounter("demo_requests_total", "Total requests", ["route"])
# PROM_LAT = Histogram("demo_request_duration_seconds", "Request latency", ["route"])


# ---------------------------
# OpenTelemetry metrics (OTLP -> Collector)
# ---------------------------
service_name = os.getenv("OTEL_SERVICE_NAME", "demo-app")
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")

resource = Resource.create({"service.name": service_name})
logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter(endpoint=f"{otlp_endpoint}/v1/logs"))
)
log_handler = LoggingHandler(logger_provider=logger_provider)
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[log_handler, logging.StreamHandler(sys.stdout)],
)


tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces"))
)
trace.set_tracer_provider(tracer_provider)

tracer: trace.Tracer = trace.get_tracer("demo-tracer")

meta_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=f"{otlp_endpoint}/v1/metrics"),
    export_interval_millis=5000,
)
meter_provider = MeterProvider(resource=resource, metric_readers=[meta_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("demo-meter")
OTEL_REQS: UpDownCounter = meter.create_up_down_counter("demo_otel_requests_total")

OTEL_LAT: Histogram = meter.create_histogram("demo_otel_request_duration_ms")


app: Final[FastAPI] = FastAPI()
FastAPIInstrumentor().instrument_app(app)  # type: ignore

# @app.get("/metrics")
# def metrics_endpoint():
#     logger.info("metrics api called ")
#     data = generate_latest()
#     return Response(data)


from datetime import datetime


class SampleResponse(BaseModel):
    msg: str
    status: bool
    dt: datetime
    data: Any


@app.get("/")
async def root() -> dict[str, Any]:
    print("Testing")
    logger.info("root api called ")
    return {"ok": False}


@app.get("/work")
async def work() -> dict[str, Any]:
    logger.info("work api called ")
    from app.helper import help

    help()

    route = "/work"
    start = time.time()

    # simulate work
    time.sleep(random.uniform(0.02, 0.2))

    dur_s = time.time() - start
    dur_ms = dur_s * 1000.0

    status = random.choice([200, 400, 500])

    # OTel metrics
    
    OTEL_LAT.record(dur_ms, {f"status_histo_{status}": route})

    if status != 200:
        raise HTTPException(status_code=status, detail="Testing Failed")

    return {"ok": True, "duration_ms": round(dur_ms, 2)}


