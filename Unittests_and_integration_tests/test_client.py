#!/usr/bin/env python3
"""
Unittests for utils
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Unittests for GithubOrgClient
    """


@patch('client.GithubOrgClient.org')
def test_org(self, mock_org):
    """
    Test _public_repos_url method
    """
    # Set up the mock response for org
    mock_org.return_value = {
        "repos_url": "https://api.github.com/orgs/testorg/repos"}

    # Create an instance of GithubOrgClient
    github_client = GithubOrgClient("testorg")

    # Call the method under test (_public_repos_url)
    result = github_client._public_repos_url()

    # Assertions
    mock_org.assert_called_once()
    mock_org.return_value.__getitem__.assert_called_once_with('repos_url')
    self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
    pass
    
    @patch('client.GithubOrgClient._public_repos_url', return_value='https://api.github.com/orgs/testorg/repos')
@patch('client.get_json')
def test_public_repos(self, mock_get_json, mock_public_repos_url):
    """
    Test public_repos method
    """
    # Set up the mock response for get_json
    mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

    # Create an instance of GithubOrgClient
    github_client = GithubOrgClient("testorg")

    # Call the method under test (public_repos)
    result = github_client.public_repos()

    # Assertions
    mock_public_repos_url.assert_called_once()
    mock_get_json.assert_called_once_with(
        'https://api.github.com/orgs/testorg/repos')
    self.assertEqual(result, [{"name": "repo1"}, {"name": "repo2"}])
    pass
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test has_license method
        """
        # Create an instance of GithubOrgClient
        github_client = GithubOrgClient("testorg")

        # Call the method under test (has_license)
        result = github_client.has_license(repo, license_key)

        # Assertion
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
