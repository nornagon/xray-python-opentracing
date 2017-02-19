"""Connection class marshals data over UDP to daemon."""
import threading
import socket
import json

CONSECUTIVE_ERRORS_BEFORE_RECONNECT = 200

class _Connection(object):
    """Instances of _Connection are used to establish a connection to the
    daemon via UDP.
    """
    def __init__(self, collector_url):
        self._collector_url = collector_url
        self._lock = threading.Lock()
        self._socket = None
        self.ready = False
        # TODO: which of these are relevant?
        self._open_exceptions_count = 0
        self._report_eof_count = 0
        self._report_socket_errors = 0
        self._report_exceptions_count = 0
        self._report_consecutive_errors = 0

    def open(self):
        """Open a UDP socket to the server."""
        self._lock.acquire()
        # TODO: exceptions
        self.ready = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(self._collector_url)
        self._socket = sock
        self._lock.release()

    def _format(self, msg):
        return ('{"format": "json", "version": 1}\n' + json.dumps(msg)).encode('utf8')

    # May throw an Exception on failure.
    def report(self, msg):
        """Report to the server."""
        with self._lock:
            try:
                if self._socket:
                    for m in msg:
                        self._socket.send(self._format(m))
                    self._report_consecutive_errors = 0
            except EOFError: # TODO: relevant?
                self._report_consecutive_errors += 1
                self._report_eof_count += 1
                raise Exception('EOFError')
            finally:
                if self._report_consecutive_errors == CONSECUTIVE_ERRORS_BEFORE_RECONNECT:
                    self._report_consecutive_errors = 0
                    self.ready = False

    def close(self):
        """Discard UDP socket."""
        with self._lock:
            self._socket = None
            self.ready = False
