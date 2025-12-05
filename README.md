# QuizMaster - Document-to-Quiz Pipeline

A full-stack solution that transforms Word documents into an interactive web-based quiz application, complete with automated CI/CD deployment.

🔗 **[Live Demo](https://musicteachj.github.io/command-line-parser/)**

![QuizMaster Application Screenshot](CommandLineParser.png)

---

## Overview

This project demonstrates an end-to-end technical workflow: parsing structured data from a `.docx` file, rendering it in a modern web application, and deploying everything automatically via GitHub Actions. The result is a polished quiz experience that persists user progress and provides immediate feedback.

---

## Features

- **Document Parsing**: Python CLI tool extracts quiz questions from Word documents
- **Interactive Quiz UI**: Clean, responsive interface with real-time progress tracking
- **State Persistence**: Answers saved to localStorage—users can leave and return without losing progress
- **Automated Deployment**: Push to `main` triggers the full build pipeline and deploys to GitHub Pages
- **Automated Tests**: Includes tests for both parsing logic and UI behavior

---

## Tech Stack

| Layer               | Technology                                                 |
| ------------------- | ---------------------------------------------------------- |
| **Document Parser** | Python 3 (stdlib only: `zipfile`, `xml.etree`, `argparse`) |
| **Frontend**        | Vue 3 with Composition API, TypeScript                     |
| **Build Tool**      | Vite                                                       |
| **Testing**         | Python `unittest`, Vitest                                  |
| **CI/CD**           | GitHub Actions                                             |
| **Hosting**         | GitHub Pages                                               |

---

## Project Structure

```
command-line-parser/
├── parser/
│   ├── parse_docx.py       # CLI tool for .docx → JSON conversion
│   ├── requirements.txt    # Dependencies (stdlib only)
│   └── tests/
│       ├── test_parser.py      # Parser unit tests
│       └── create_test_docx.py # Test fixture generator
├── quiz-app/
│   ├── src/
│   │   ├── App.vue              # Main application with quiz logic
│   │   ├── components/
│   │   │   ├── QuizQuestion.vue # Question display component
│   │   │   └── QuizResults.vue  # Results summary component
│   │   ├── types/
│   │   │   └── quiz.ts          # TypeScript interfaces
│   │   ├── utils/
│   │   │   └── quiz-helpers.ts  # Testable helper functions
│   │   └── __tests__/
│   │       └── quiz-helpers.test.ts # Frontend unit tests
│   ├── public/
│   │   └── questions.json       # Generated quiz data
│   └── vite.config.ts           # Vite + Vitest configuration
├── .github/
│   └── workflows/
│       └── deploy.yml           # CI/CD pipeline
└── CLD TECH ASSESSMENT.docx     # Source document
```

---

## Development Approach

I broke this project into three distinct phases, each building on the last:

### Phase 1: Document Parser

The first challenge was extracting structured data from a Word document. Since `.docx` files are actually ZIP archives containing XML, I used Python's standard library to:

1. Open the archive and extract `word/document.xml`
2. Parse the XML to identify paragraphs and list items
3. Pattern-match to find questions (paragraphs starting with "Question")
4. Validate that each question has exactly 4 answer choices
5. Output clean JSON ready for the frontend

```bash
python parser/parse_docx.py "CLD TECH ASSESSMENT.docx" -o quiz-app/public/questions.json
```

### Phase 2: Vue 3 Quiz Application

With the data layer solved, I built the frontend using Vue 3's Composition API with TypeScript. Key implementation decisions:

- **Reactive state management** using `ref` and `reactive` for questions, answers, and navigation
- **localStorage persistence** with watchers that auto-save on every interaction
- **Component decomposition** separating concerns: `QuizQuestion` handles display logic, `QuizResults` handles scoring and review
- **Accessible UI** with keyboard navigation support and clear visual feedback

### Phase 3: CI/CD Pipeline

The final piece ties everything together with GitHub Actions:

1. On push to `main`, run the Python parser to regenerate `questions.json`
2. Build the Vue app with Vite
3. Deploy static assets to GitHub Pages

This means updating the source Word document automatically propagates to the live site—no manual intervention required.

---

## Running Locally

### Prerequisites

- Python 3.8+
- Node.js 18+

### Parser

```bash
cd parser
python parse_docx.py "../CLD TECH ASSESSMENT.docx" -o ../quiz-app/public/questions.json
```

### Quiz App

```bash
cd quiz-app
npm install
npm run dev
```

The app will be available at `http://localhost:5173`

---

## Testing

This project includes automated tests for both the parser and frontend.

### Parser Tests

```bash
cd parser
python3 tests/test_parser.py
```

Runs **11 tests** covering:

- JSON structure validation
- Question extraction and counting
- Choice parsing and labeling
- Error handling for invalid files

### Frontend Tests

```bash
cd quiz-app
npm test
```

Runs **22 tests** using Vitest covering:

- Progress calculation
- Answer counting
- Quiz completion detection
- Question validation

---

## Build for Production

```bash
cd quiz-app
npm run build
```

Static files are output to `quiz-app/dist/`

---

## Technical Decisions

**Why Python for parsing?** Word's internal XML structure is well-documented, and Python's standard library handles both ZIP extraction and XML parsing cleanly. No external dependencies means zero configuration overhead.

**Why Vue 3 Composition API?** The Composition API provides better TypeScript integration and more flexible code organization than the Options API. Using `<script setup>` keeps components concise while maintaining full type safety.

**Why Vite?** Fast HMR during development, optimized production builds, and first-class Vue 3 support. The configuration for GitHub Pages deployment is straightforward.

**Why GitHub Actions + Pages?** Zero-cost hosting with automated deployments. The entire pipeline—from document parsing to live site—runs on push without any manual steps.

---

## Development Tools

This project was developed using [Cursor](https://cursor.com/) with Claude Opus 4.5 as an AI coding assistant. The AI helped accelerate development by suggesting implementations and catching edge cases, while I drove the architecture decisions, directed the technical approach, and ensured the final product met my quality standards.

---

## License

MIT
