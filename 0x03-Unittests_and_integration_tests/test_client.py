#!/usr/bin/env python3
"""
Test module for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected payload."""
        client = GithubOrgClient(org_name)
        client.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url property returns expected URL."""
        client = GithubOrgClient("testorg")
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/testorg/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )

            client = GithubOrgClient("google")
            repos = client.public_repos()

            expected_repo_names = ["repo1", "repo2", "repo3"]

            self.assertEqual(repos, expected_repo_names)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )


if __name__ == "__main__":
    unittest.main()
