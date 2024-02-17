#!/usr/bin/env python3
""" Unit Test for utility functions """
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):


    """ Access_nested_map function """


@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2)
])
def test_access_nested_map(self, nested_map, path, expected):
    """ Test access_nested_map with various input scenarios """
    self.assertEqual(access_nested_map(nested_map, path), expected)


@parameterized.expand([
    ({}, ("a",)),
    ({"a": 1}, ("a", "b"))
])
def test_access_nested_map_exception(self, nested_map, path):
    """ Test exception """
    with self.assertRaises(KeyError):
        access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):


    """ Tests for get_json function """


@parameterized.expand([
    ("http://example.com", {"payload": True}),
    ("http://holberton.io", {"payload": False})
])
def test_get_json(self, test_url, test_payload):
    """ Test get_json with different URLs and payloads """
    class Mocked(Mock):
        """ Mocked class for requests.get """

        def json(self):
            """ Mocked json method """
            return test_payload

    with patch('requests.get') as MockClass:
        MockClass.return_value = Mocked()
        self.assertEqual(get_json(test_url), test_payload)


class TestMemoize(unittest.TestCase):


    """ Tests for memoize decorator """


def test_memoize(self):
    """ Test the memoize decorator with a method """

    class TestClass:
        """ Class with a memoized property """

        def a_method(self):
            """ Method to be memoized """
            return 42

        @memoize
        def a_property(self):
            """ Memoized property calling a_method """
            return self.a_method()

    with patch.object(TestClass, 'a_method') as mocked:
        instance = TestClass()
        instance.a_property
        instance.a_property
        mocked.assert_called_once()
