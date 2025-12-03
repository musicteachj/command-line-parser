#!/usr/bin/env python3
"""
Command-line parser for extracting quiz questions from .docx files.

Usage:
    python parse_docx.py <input.docx> [-o output.json]

This script extracts questions and answer choices from a Word document
and outputs them as structured JSON.
"""

import argparse
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


# Word XML namespace
WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract_document_xml(docx_path: str) -> str:
    """Extract word/document.xml content from a .docx file."""
    try:
        with zipfile.ZipFile(docx_path, "r") as zf:
            return zf.read("word/document.xml").decode("utf-8")
    except zipfile.BadZipFile:
        raise ValueError(f"'{docx_path}' is not a valid .docx file")
    except KeyError:
        raise ValueError(f"'{docx_path}' does not contain word/document.xml")


def get_paragraph_text(para_elem: ET.Element) -> str:
    """Extract full text from a paragraph element by combining all text runs."""
    text_parts = []
    for text_elem in para_elem.iter(f"{WORD_NS}t"):
        if text_elem.text:
            text_parts.append(text_elem.text)
    return "".join(text_parts).strip()


def is_list_paragraph(para_elem: ET.Element) -> bool:
    """Check if a paragraph is a list item (has numbering properties)."""
    ppr = para_elem.find(f"{WORD_NS}pPr")
    if ppr is not None:
        num_pr = ppr.find(f"{WORD_NS}numPr")
        return num_pr is not None
    return False


def parse_paragraphs(xml_content: str) -> list[dict]:
    """Parse XML and extract paragraph info."""
    root = ET.fromstring(xml_content)
    body = root.find(f"{WORD_NS}body")
    if body is None:
        raise ValueError("Could not find document body in XML")

    paragraphs = []
    for para in body.findall(f"{WORD_NS}p"):
        text = get_paragraph_text(para)
        is_list = is_list_paragraph(para)
        paragraphs.append({"text": text, "is_list": is_list})

    return paragraphs


def extract_questions(paragraphs: list[dict]) -> list[dict]:
    """
    Extract questions and answer choices from parsed paragraphs.

    A question starts with a paragraph beginning with "Question".
    The next non-empty, non-list paragraph is the question text.
    The following 4 list paragraphs are the answer choices (A, B, C, D).
    """
    questions = []
    i = 0
    question_pattern = re.compile(r"^Question\s*\d*", re.IGNORECASE)
    choice_labels = ["A", "B", "C", "D"]

    while i < len(paragraphs):
        para = paragraphs[i]

        # Look for "Question X" paragraph
        if question_pattern.match(para["text"]):
            question_header = para["text"]
            i += 1

            # Skip empty paragraphs, find the question text
            question_text = None
            while i < len(paragraphs):
                if paragraphs[i]["text"] and not paragraphs[i]["is_list"]:
                    question_text = paragraphs[i]["text"]
                    i += 1
                    break
                elif paragraphs[i]["is_list"]:
                    # Question text might be in the header itself
                    break
                i += 1

            if question_text is None:
                raise ValueError(
                    f"Could not find question text after '{question_header}'"
                )

            # Collect exactly 4 answer choices (list items)
            choices = []
            while i < len(paragraphs) and len(choices) < 4:
                if paragraphs[i]["is_list"] and paragraphs[i]["text"]:
                    choices.append({
                        "label": choice_labels[len(choices)],
                        "text": paragraphs[i]["text"]
                    })
                    i += 1
                elif paragraphs[i]["text"] == "":
                    # Skip empty paragraphs
                    i += 1
                else:
                    # Non-list, non-empty paragraph - stop collecting choices
                    break

            # Validate exactly 4 choices
            if len(choices) != 4:
                raise ValueError(
                    f"'{question_header}' has {len(choices)} answer choices, "
                    f"expected exactly 4 labeled A, B, C, D. "
                    f"Found choices: {[c['text'] for c in choices]}"
                )

            # Extract question number from header
            num_match = re.search(r"\d+", question_header)
            question_id = int(num_match.group()) if num_match else len(questions) + 1

            questions.append({
                "id": question_id,
                "text": question_text,
                "choices": choices
            })
        else:
            i += 1

    return questions


def parse_docx(docx_path: str) -> dict:
    """
    Parse a .docx file and extract quiz questions.

    Args:
        docx_path: Path to the .docx file

    Returns:
        Dictionary with 'questions' key containing list of question objects
    """
    xml_content = extract_document_xml(docx_path)
    paragraphs = parse_paragraphs(xml_content)
    questions = extract_questions(paragraphs)

    if not questions:
        raise ValueError("No questions found in document")

    return {"questions": questions}


def main():
    parser = argparse.ArgumentParser(
        description="Parse quiz questions from a .docx file and output as JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python parse_docx.py quiz.docx
    python parse_docx.py quiz.docx -o questions.json
    python parse_docx.py "CLD TECH ASSESSMENT.docx" -o output/questions.json
        """
    )
    parser.add_argument(
        "input_file",
        help="Path to the .docx file to parse"
    )
    parser.add_argument(
        "-o", "--output",
        default="questions.json",
        help="Output JSON file path (default: questions.json)"
    )

    args = parser.parse_args()

    # Validate input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)

    if not input_path.suffix.lower() == ".docx":
        print(f"Warning: '{args.input_file}' does not have .docx extension", file=sys.stderr)

    try:
        # Parse the document
        result = parse_docx(args.input_file)

        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON output
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Successfully parsed {len(result['questions'])} questions")
        print(f"Output written to: {output_path}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

