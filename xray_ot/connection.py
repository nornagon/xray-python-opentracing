"""Connection class marshals data over UDP to daemon."""
import socket
import json


class _Connection(object):
    """Instances of _Connection are used to communicate with the X-Ray daemon
    via UDP.
    """
    def __init__(self, collector_url):
        self._collector_url = collector_url
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _format(self, msg):
        return ('{"format": "json", "version": 1}\n' + json.dumps(msg)).encode('utf8')

    def report(self, msg):
        """Report to the daemon."""
        for m in msg:
            self._socket.sendto(self._format(m), self._collector_url)
