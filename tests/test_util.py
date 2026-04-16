"""Tests for zipcodelib utility functions"""

import pytest
import os
from unittest.mock import patch, mock_open
from zipcodelib.util import download


class TestDownloadFunction:
    """Test cases for the download function"""
    
    def test_download_function_exists(self):
        """Test that download function is available"""
        assert callable(download)
        
    @patch("zipcodelib.util.requests.get")
    @patch("zipcodelib.util.open", new_callable=mock_open)
    def test_download_with_mocked_requests(self, mock_file, mock_get):
        """Test download function with mocked requests"""
        # Mock response
        mock_response = mock_get.return_value
        mock_response.headers = {"content-length": "100"}
        mock_response.iter_content.return_value = [b"data"]
        
        # Test the download function
        result = download(
            url="http://example.com/test.txt",
            fname="test.txt",
            use_cached=False
        )
        
        # Verify the function was called correctly
        assert mock_get.called
        assert mock_file.called