"""test_rpc.py"""
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods

from unittest import TestCase, main
import itertools
import json

from jsonrpcclient import rpc
from jsonrpcclient.rpc import rpc_request, rpc_request_str, sort_request


class TestRPC(TestCase):

    def setUp(self):
        rpc.id_generator = itertools.count(1) # First generated is 1

    # sort_request
    def test_sort_request(self):
        self.assertEqual(
            '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 2}',
            json.dumps(sort_request({'id': 2, 'params': [2, 3], 'method': 'add', 'jsonrpc': '2.0'})),
        )

    # Notifications
    def test_request_no_arguments(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "get"},
            rpc_request('get')
        )

    def test_request_one_positional(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "sqrt", "params": [1]},
            rpc_request('sqrt', 1)
        )

    def test_request_two_positionals(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "add", "params": [1, 2]},
            rpc_request('add', 1, 2)
        )

    def test_request_one_keyword(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": {"name": "Foo"}},
            rpc_request('find', name='Foo')
        )

    def test_request_two_keywords(self):
        """Note that keyword arguments are sorted in alphabetical order by the
        keys. This is because they're not received in any order, so we sort
        them, to be sure of *some* order"""
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": {"age": 42, "name": "Foo"}},
            rpc_request('find', name='Foo', age=42)
        )

    def test_request_both_positional_and_keyword(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": ["Foo", {"age": 42}]},
            rpc_request('find', 'Foo', age=42)
        )

    def test_request_dict_params(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": {"age": 42, "name": "Foo"}},
            rpc_request('find', name='Foo', age=42)
        )

    def test_request_list_params(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "find", "params": ["Foo", 42]},
            rpc_request('find', ['Foo', 42])
        )

    # Requests (requiring a response)
    def test_request_method_only_requiring_response(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "go", "id": 1},
            rpc_request('go', response=True)
        )

    def test_request_both_positional_and_keyword_requiring_response(self):
        self.assertEqual(
            {"jsonrpc": "2.0", "method": "go", "params": ["positional", {"keyword": "foo"}], "id": 1},
            rpc_request('go', 'positional', keyword='foo', response=True)
        )

    # request_str
    def test_request_str(self):
        self.assertEqual(
            '{"jsonrpc": "2.0", "method": "get"}',
            rpc_request_str('get')
        )


if __name__ == '__main__':
    main()
