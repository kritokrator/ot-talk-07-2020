import datetime
import time

from flask import Flask, render_template

# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor


trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(CloudTraceSpanExporter())
)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)

@app.route('/')
def root():
    with tracer.start_as_current_span("root"):
        print("Hello world from OpenTelemetry Python!")
        time.sleep(1)
        foo("going deeper", "underdark")
        return "It works!"


def foo(value1, value2):
    with tracer.start_as_current_span(f"Span for foo: {value2}"):
        time.sleep(1)
        print(f"value1: {value1}")
        bar("going even deeper", "moria")


def bar(value1, value2):
    with tracer.start_as_current_span(f"Span for bar {value2}"):
        time.sleep(2)
        print(f"value1: {value1}")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
