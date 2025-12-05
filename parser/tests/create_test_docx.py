#!/usr/bin/env python3
"""
Helper script to create a minimal test .docx file for testing the parser.

This creates a valid Word document with 2 questions using only standard library.
.docx files are ZIP archives containing XML files.
"""

import zipfile
import os
from pathlib import Path

# Minimal Word document XML structure
CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""


def create_paragraph(text: str, is_list: bool = False) -> str:
    """Create a Word XML paragraph element."""
    num_pr = ""
    if is_list:
        num_pr = """<w:numPr>
          <w:ilvl w:val="0"/>
          <w:numId w:val="1"/>
        </w:numPr>"""
    
    return f"""<w:p>
      <w:pPr>{num_pr}</w:pPr>
      <w:r>
        <w:t>{text}</w:t>
      </w:r>
    </w:p>"""


def create_document_xml(questions: list[dict]) -> str:
    """
    Create the main document.xml content.
    
    Each question dict should have:
    - header: "Question 1", "Question 2", etc.
    - text: The question text
    - choices: List of 4 answer choice strings
    """
    paragraphs = []
    
    for q in questions:
        # Question header paragraph
        paragraphs.append(create_paragraph(q["header"]))
        # Question text paragraph
        paragraphs.append(create_paragraph(q["text"]))
        # Answer choices as list items
        for choice in q["choices"]:
            paragraphs.append(create_paragraph(choice, is_list=True))
        # Empty paragraph between questions
        paragraphs.append(create_paragraph(""))
    
    body_content = "\n".join(paragraphs)
    
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {body_content}
  </w:body>
</w:document>"""


def create_test_docx(output_path: str, questions: list[dict]) -> None:
    """Create a minimal .docx file with the specified questions."""
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
        zf.writestr("_rels/.rels", RELS_XML)
        zf.writestr("word/document.xml", create_document_xml(questions))
    
    print(f"Created test document: {output_path}")


if __name__ == "__main__":
    # Create a test document with 2 questions
    test_questions = [
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
    
    script_dir = Path(__file__).parent
    output_path = script_dir / "fixtures" / "test_quiz.docx"
    
    create_test_docx(str(output_path), test_questions)

