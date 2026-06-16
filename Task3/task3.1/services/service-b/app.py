import random
import time

from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "payer"})))
otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger.observability:4317",
    insecure=True,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter))
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)


@app.route("/pay")
def pay():
    with trace.get_tracer(__name__).start_as_current_span("pay"):
        random_pay_number = random.randint(1, 500)
        time.sleep(random_pay_number * 0.001)  #задержка
        return str(random_pay_number)
