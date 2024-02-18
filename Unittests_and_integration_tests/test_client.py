#!/usr/bin/env python3
"""
Unittests for client
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
import client
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unittests for GithubOrgClient
    """
    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json')
    def test_org(self, url, my_mock):
        """
        Test GithubOrgClient.org
        """
        my_mock.return_value = True
        g = client.GithubOrgClient(url)
        self.assertEqual(g.org, True)
        my_mock.assert_called_once()

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    def test_public_repos_url(self, org):
        """
        Test _public_repos_url
        """
        url = 'https://api.github.com/orgs/{}/repos'.format(org)
        payload = {'repos_url': url}
        with patch('client.GithubOrgClient.org',
                   PropertyMock(return_value=payload)):
            g = client.GithubOrgClient(org)
            self.assertEqual(g._public_repos_url, url)

    @patch('client.get_json')
    def test_public_repos(self, my_mock):
        """
        Test public_repos
        """
        return_value = [{'name': 'google'}, {'name': 'abc'}]
        my_mock.return_value = return_value
        with patch('client.GithubOrgClient._public_repos_url',
                   PropertyMock(return_value=return_value)) as public:
            g = client.GithubOrgClient('test')
            self.assertEqual(g.public_repos(), ['google', 'abc'])
            my_mock.assert_called_once()
            public.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, has_license):
        """
        Test has_license
        """
        g = client.GithubOrgClient('test')
        self.assertEqual(g.has_license(repo, license_key), has_license)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for GithubOrgClient
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up class
        """
        config = {
            'return_value.json.side_effect': [
                cls.org_payload, cls.repos_payload,
                cls.org_payload, cls.repos_payload
            ]
        }
        cls.get_patcher = patch('requests.get', **config)
        cls.mock = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test public_repos
        """
        g = client.GithubOrgClient('test')
        self.assertEqual(g.org, self.org_payload)
        self.assertEqual(g.repos_payload, self.repos_payload)
        self.assertEqual(g.public_repos(), self.expected_repos)
        self.assertEqual(g.public_repos('test'), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """
        Test public_repos with license 'apache-2.0'
        """
        g = client.GithubOrgClient('test')
        self.assertEqual(g.org, self.org_payload)
        self.assertEqual(g.repos_payload, self.repos_payload)
        self.assertEqual(g.public_repos(), self.expected_repos)
        self.assertEqual(g.public_repos('test'), [])
        self.assertEqual(g.public_repos('apache-2.0'), self.apache2_repos)
        self.mock.assert_called()


if __name__ == '__main__':
    unittest.main()
