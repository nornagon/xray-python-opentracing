from __future__ import absolute_import

import struct
from basictracer.context import SpanContext
from basictracer.propagator import Propagator
from opentracing import InvalidCarrierException


class BinaryPropagator(Propagator):
    """A BasicTracer Propagator for Format.BINARY."""

    def inject(self, span_context, carrier):
        if type(carrier) is not bytearray:
            raise InvalidCarrierException()
        _wstr(carrier, span_context.trace_id)
        _wstr(carrier, span_context.span_id)
        carrier.extend(struct.pack('?', span_context.sampled))
        carrier.extend(struct.pack('>I',
            len(span_context.baggage) if span_context.baggage is not None else 0))
        if span_context.baggage is not None:
            for key in span_context.baggage:
                _wstr(carrier, key)
                _wstr(carrier, span_context.baggage[key])

    def extract(self, carrier):
        if type(carrier) is not bytearray:
            raise InvalidCarrierException()
        m = memoryview(carrier)
        m, trace_id = _rstr(m)
        m, span_id = _rstr(m)
        sampled = struct.unpack('?', m[:1])[0]
        m = m[1:]
        bl = struct.unpack('>I', m[:4])[0]
        m = m[4:]
        baggage = {}
        for _ in range(bl):
            m, k = _rstr(m)
            m, v = _rstr(m)
            baggage[k] = v

        return SpanContext(
            span_id=span_id,
            trace_id=trace_id,
            baggage=baggage,
            sampled=sampled)


def _wstr(buf, s):
    buf.extend(struct.pack('>I', len(s)))
    buf.extend(s.encode('utf8'))


def _rstr(buf):
    l = struct.unpack('>I', buf[:4])[0]
    s = bytes(buf[4:4+l]).decode('utf8')
    return buf[4+l:], s
