"""test_zmq_server.py"""
#pylint:disable=missing-docstring,line-too-long

import json
from unittest import TestCase, main
import itertools

import zmq
from mock import patch, Mock

from jsonrpcclient import rpc
from jsonrpcclient.rpc import rpc_request_str
from jsonrpcclient.zmq_server import ZMQServer


class TestZMQServer(TestCase):

    def setUp(self):
        # Monkey patch id_iterator to ensure the request id is always 1
        rpc.id_iterator = itertools.count(1)

    @staticmethod
    def test_instantiate():
        ZMQServer('tcp://localhost:5555')

    @patch('zmq.Socket.send_string', Mock())
    @patch('zmq.Socket.recv', Mock())
    def test_send_message(self):
        server = ZMQServer('tcp://localhost:5555')
        server.send_message(json.dumps(rpc_request_str('go')))

    def test_send_message_with_connection_error(self):
        server = ZMQServer('tcp://localhost:5555')
        # Set timeouts
        server.socket.setsockopt(zmq.RCVTIMEO, 5)
        server.socket.setsockopt(zmq.SNDTIMEO, 5)
        server.socket.setsockopt(zmq.LINGER, 5)
        with self.assertRaises(zmq.error.ZMQError):
            server.send_message(json.dumps(rpc_request_str('go')))


if __name__ == '__main__':
    main()
