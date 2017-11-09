# WIP: xray-python-opentracing

[![MIT license](http://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)

Python [OpenTracing](http://opentracing.io/) implementation for [AWS X-Ray](http://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html), a distributed tracing system.

WIP (but it works for [us](http://lexy.io)). Heavily based on the excellent [LightStep Tracer](https://github.com/lightstep/lightstep-tracer-python).

## Installation

xray-python-opentracing is not yet on PyPI, but you can add the following line
to your requirements.txt:

```
git+git://github.com/nornagon/xray-python-opentracing.git@9a40fbc
```

## Getting started

Please see the [example programs](examples/) for examples of how to use this library. In particular:

* [Trivial Example](examples/trivial/main.py) shows how to use the library on a single host.
* [Context in Headers](examples/http/context_in_headers.py) shows how to pass a `TraceContext` through `HTTP` headers.

Or if your python code is already instrumented for OpenTracing, you can simply switch to this implementation with:

```python
import opentracing
import xray_ot

if __name__ == "__main__":
  opentracing.tracer = xray_ot.Tracer(
    component_name='your_microservice_name',
    collector_host='127.0.0.1',
    collector_port=2000)

  with opentracing.tracer.start_span('TestSpan') as span:
    span.log_event('test message', payload={'life': 42})

  opentracing.tracer.flush()
```

This library is an AWS X-Ray binding for [OpenTracing](http://opentracing.io/). See the [OpenTracing Python API](https://github.com/opentracing/opentracing-python) for additional detail.

