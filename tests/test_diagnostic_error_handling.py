#!/usr/bin/env python3
"""Tests for diagnostic build error handling."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import build_diagnostic_report, write_diagnostic_report


class TestDiagnosticErrorHandling(unittest.TestCase):
    def test_report_with_empty_results(self):
        """Should handle empty results gracefully."""
        report = build_diagnostic_report([], "test1234")
        self.assertEqual(report["total_modules"], 0)
        self.assertEqual(report["passed"], 0)
        self.assertEqual(report["failed"], 0)
        self.assertEqual(report["modules"], [])
    
    def test_report_preserves_on_logd_error(self):
        """Should preserve report when logd generation fails."""
        results = [("backend", True, 1.0, "ok", None)]
        error = "encryptly binary not found"
        
        report = build_diagnostic_report(results, "test1234", logd_error=error)
        
        self.assertEqual(report["diagnostic_logd_error"], error)
        self.assertIsNone(report["diagnostic_logd"])
        self.assertEqual(report["total_modules"], 1)
    
    def test_write_report_creates_file(self):
        """Should create metadata file."""
        report = {"test": "data"}
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = Path(f.name)
        
        try:
            write_diagnostic_report(path, report)
            self.assertTrue(path.exists())
            with open(path) as f:
                loaded = json.load(f)
            self.assertEqual(loaded["test"], "data")
        finally:
            path.unlink()
    
    def test_report_with_none_password(self):
        """Should handle None password gracefully."""
        results = [("backend", True, 1.0, "ok", None)]
        report = build_diagnostic_report(results, "test1234")
        self.assertIsNone(report.get("password"))
        self.assertIsNone(report.get("decrypt_command"))


if __name__ == "__main__":
    unittest.main()
