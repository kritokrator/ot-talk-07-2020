# README
Code presented during the Python Medellín Meetup.

## Avialblable Branches

 - flask_simple - contains the localhost example that prints the spans to the the console
 - flask_simple_gae - contains the same code as the previous example however it use the CloudTrace exporter
 it is intended to be run as a GAE project
 - flask_integration_ge - Same code as before, uses the opentelemetry flask integration
 - aiohttp_gae - simple aiohttp server with 3 async aiohttpClient calls. Uses the opentelemetry 
 aiohttpClient integretion, intended tu be run as a GAE project
 
 - flask_simple_connected - simple flask app, intended to be run on local machine.
 Sends a trace id to a deployed app in a header. The user needs to connect the app to
 the CloudTrace service by himself.
 
 - aiohttp_gae_connected - Mostly the same code as in the aiohttp_gae branch. Remote SpanContext
 that get's the trace_id from a custom header is added to the code.
 
 All code samples were created using the examples available on https://opentelemetry-python.readthedocs.io/en/stable/
 
