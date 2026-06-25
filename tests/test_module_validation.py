#!/usr/bin/env python3
"""Tests for module validation helpers."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from build import parse_module_selection, validate_module_selection, list_modules, MODULES


class TestParseModuleSelection(unittest.TestCase):
    def test_single_module(self):
        self.assertEqual(parse_module_selection("backend"), ["backend"])
    
    def test_multiple_modules(self):
        self.assertEqual(parse_module_selection("backend,frontend"), ["backend", "frontend"])
    
    def test_with_spaces(self):
        self.assertEqual(parse_module_selection("backend , frontend , market"), ["backend", "frontend", "market"])
    
    def test_all_keyword(self):
        self.assertEqual(parse_module_selection("all"), ["all"])
    
    def test_empty_string(self):
        self.assertEqual(parse_module_selection(""), ["all"])
    
    def test_whitespace_only(self):
        self.assertEqual(parse_module_selection("  "), ["all"])


class TestValidateModuleNames(unittest.TestCase):
    def test_valid_module(self):
        valid, invalid = validate_module_selection(["backend"], MODULES)
        self.assertEqual(len(valid), 1)
        self.assertEqual(valid[0].name, "backend")
        self.assertEqual(invalid, [])
    
    def test_invalid_module(self):
        valid, invalid = validate_module_selection(["nonexistent"], MODULES)
        self.assertEqual(valid, [])
        self.assertEqual(invalid, ["nonexistent"])
    
    def test_mixed_valid_invalid(self):
        valid, invalid = validate_module_selection(["backend", "nonexistent"], MODULES)
        self.assertEqual(len(valid), 1)
        self.assertEqual(invalid, ["nonexistent"])
    
    def test_all_keyword(self):
        valid, invalid = validate_module_selection(["all"], MODULES)
        self.assertEqual(len(valid), len(MODULES))
        self.assertEqual(invalid, [])


if __name__ == "__main__":
    unittest.main()
