import aiohttp
from aiohttp import web
import asyncio
import yarl

# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor

from opentelemetry.ext.aiohttp_client import (
    create_trace_config,
    url_path_span_name
)


def strip_query_params(url: yarl.URL) -> str:
    return str(url.with_query(None))

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(CloudTraceSpanExporter())
)
tracer = trace.get_tracer(__name__)


async def hello_async(request):
    with tracer.start_as_current_span("root"):
        awaitables = [
            get_page('https://google.com', request),
            get_page('https://reddit.com', request),
            get_page('https://youtube.com', request),
        ]
        for future in asyncio.as_completed(awaitables):
            response = await future
            print(response.status)
        return web.Response(text="It works!")


async def get_page(url, request):
    with tracer.start_as_current_span(f"get page: {url}"):
        async with aiohttp.ClientSession(trace_configs=[request.app['trace_config']]) as session:
            response = await session.get(url)
            return response


def init_app(*args, **kwargs):
    app = web.Application()
    trace_config = create_trace_config(
        # Remove all query params from the URL attribute on the span.
        url_filter=strip_query_params,
        # Use the URL's path as the span name.
        span_name=url_path_span_name
    )
    app['trace_config'] = trace_config
    app.router.add_get('/', hello_async,
                       name='async_call')

    return app


app = init_app()
