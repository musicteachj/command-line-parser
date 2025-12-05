#!/usr/bin/env python3
"""
Automated tests for the .docx quiz parser.

Run with: python -m pytest tests/test_parser.py -v
Or simply: python tests/test_parser.py
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parse_docx import (
    parse_docx,
    extract_questions,
    parse_paragraphs,
    get_paragraph_text,
)
from tests.create_test_docx import create_test_docx


class TestParseDocx(unittest.TestCase):
    """Tests for the parse_docx.py module."""

    @classmethod
    def setUpClass(cls):
        """Create test fixtures once before all tests."""
        cls.test_dir = Path(tempfile.mkdtemp())
        
        # Create a test document with 2 questions
        cls.test_questions = [
            {
                "header": "Question 1",
                "text": "What is the capital of France?",
                "choices": ["Paris", "London", "Berlin", "Madrid"]
            },
            {
                "header": "Question 2",
                "text": "What is 2 + 2?",
                "choices": ["3", "4", "5", "6"]
            }
        ]
        
        cls.test_docx_path = cls.test_dir / "test_quiz.docx"
        create_test_docx(str(cls.test_docx_path), cls.test_questions)

    def test_parse_docx_returns_correct_structure(self):
        """Test that parse_docx returns the expected JSON structure."""
        result = parse_docx(str(self.test_docx_path))
        
        # Check top-level structure
        self.assertIn("questions", result)
        self.assertIsInstance(result["questions"], list)

    def test_parse_docx_extracts_correct_question_count(self):
        """Test that the parser extracts exactly 2 questions."""
        result = parse_docx(str(self.test_docx_path))
        
        self.assertEqual(len(result["questions"]), 2)

    def test_parse_docx_extracts_question_text(self):
        """Test that question text is correctly extracted."""
        result = parse_docx(str(self.test_docx_path))
        
        question_texts = [q["text"] for q in result["questions"]]
        self.assertIn("What is the capital of France?", question_texts)
        self.assertIn("What is 2 + 2?", question_texts)

    def test_parse_docx_extracts_four_choices_per_question(self):
        """Test that each question has exactly 4 choices."""
        result = parse_docx(str(self.test_docx_path))
        
        for question in result["questions"]:
            self.assertEqual(len(question["choices"]), 4)

    def test_parse_docx_assigns_correct_labels(self):
        """Test that choices are labeled A, B, C, D."""
        result = parse_docx(str(self.test_docx_path))
        
        expected_labels = ["A", "B", "C", "D"]
        for question in result["questions"]:
            labels = [c["label"] for c in question["choices"]]
            self.assertEqual(labels, expected_labels)

    def test_parse_docx_extracts_choice_text(self):
        """Test that choice text is correctly extracted."""
        result = parse_docx(str(self.test_docx_path))
        
        # Find Question 1 and check its choices
        q1 = next(q for q in result["questions"] if q["id"] == 1)
        choice_texts = [c["text"] for c in q1["choices"]]
        
        self.assertEqual(choice_texts, ["Paris", "London", "Berlin", "Madrid"])

    def test_parse_docx_assigns_question_ids(self):
        """Test that questions have sequential IDs."""
        result = parse_docx(str(self.test_docx_path))
        
        ids = [q["id"] for q in result["questions"]]
        self.assertEqual(ids, [1, 2])

    def test_parse_docx_invalid_file_raises_error(self):
        """Test that parsing an invalid file raises ValueError."""
        invalid_path = self.test_dir / "not_a_docx.txt"
        invalid_path.write_text("This is not a docx file")
        
        with self.assertRaises(ValueError):
            parse_docx(str(invalid_path))

    def test_json_output_is_valid(self):
        """Test that the output can be serialized to valid JSON."""
        result = parse_docx(str(self.test_docx_path))
        
        # Should not raise
        json_str = json.dumps(result, indent=2)
        
        # Should be able to parse back
        parsed = json.loads(json_str)
        self.assertEqual(parsed, result)


class TestExtractQuestions(unittest.TestCase):
    """Tests for the extract_questions function."""

    def test_extract_questions_from_paragraphs(self):
        """Test that extract_questions correctly processes paragraph data."""
        paragraphs = [
            {"text": "Question 1", "is_list": False},
            {"text": "What is Python?", "is_list": False},
            {"text": "A programming language", "is_list": True},
            {"text": "A snake", "is_list": True},
            {"text": "A movie", "is_list": True},
            {"text": "A car brand", "is_list": True},
        ]
        
        questions = extract_questions(paragraphs)
        
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0]["text"], "What is Python?")
        self.assertEqual(len(questions[0]["choices"]), 4)


class TestParserIntegration(unittest.TestCase):
    """Integration tests that verify end-to-end parsing."""

    def test_parse_three_questions(self):
        """Test parsing a document with 3 questions."""
        test_dir = Path(tempfile.mkdtemp())
        
        questions = [
            {
                "header": "Question 1",
                "text": "First question?",
                "choices": ["A1", "B1", "C1", "D1"]
            },
            {
                "header": "Question 2",
                "text": "Second question?",
                "choices": ["A2", "B2", "C2", "D2"]
            },
            {
                "header": "Question 3",
                "text": "Third question?",
                "choices": ["A3", "B3", "C3", "D3"]
            }
        ]
        
        docx_path = test_dir / "three_questions.docx"
        create_test_docx(str(docx_path), questions)
        
        result = parse_docx(str(docx_path))
        
        self.assertEqual(len(result["questions"]), 3)
        self.assertEqual(result["questions"][2]["text"], "Third question?")


def run_tests():
    """Run all tests and print summary."""
    print("=" * 60)
    print("Running Parser Tests")
    print("=" * 60)
    
    # Run tests with verbosity
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 60)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())

