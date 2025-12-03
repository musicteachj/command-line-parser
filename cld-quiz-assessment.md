# CLD Technical Assessment Plan

## Part 1: Command-Line Parser (Python)

Create a Python CLI tool that:

1. **Extracts the .docx file** - Since .docx is a ZIP archive, use Python's `zipfile` module to extract `word/document.xml`

2. **Parses the XML** - Use `xml.etree.ElementTree` to navigate the Word document structure and extract paragraph text

3. **Identifies questions** - Detect paragraphs starting with "Question" and capture subsequent answer choices (A, B, C, D)

4. **Validates structure** - Error and halt if any question doesn't have exactly 4 answer choices labeled A, B, C, D

5. **Outputs JSON** - Write a clean JSON file with structure like:

```json
{
  "questions": [
    {
      "id": 1,
      "text": "What color is the sky?",
      "choices": [
        { "label": "A", "text": "Blue" },
        { "label": "B", "text": "Purple" },
        { "label": "C", "text": "None of the above" },
        { "label": "D", "text": "It depends" }
      ]
    }
  ]
}
```

**Files to create:**

- `parser/parse_docx.py` - Main CLI script
- `parser/requirements.txt` - Dependencies (minimal, just standard library)

---

## Part 2: Vue3 Quiz Web Application

Create a modern Vue3 application using Vite:

1. **Project structure:**

   - `quiz-app/` - Vue3 + Vite project
   - Copy generated `questions.json` into `quiz-app/public/`

2. **Core features:**

   - Load questions from JSON file
   - Display one question at a time with radio button choices
   - Navigation between questions (next/previous or question list)
   - Persist user's answers to localStorage on each selection
   - Resume from localStorage if user returns to page
   - Submit quiz and display results showing correct/incorrect answers

3. **Components:**

   - `App.vue` - Main app with quiz state management
   - `QuizQuestion.vue` - Single question display with choices
   - `QuizResults.vue` - Final results summary

4. **Key implementation details:**

   - Use Vue3 Composition API with `<script setup>`
   - Use `ref` and `reactive` for state management
   - Watch for answer changes to persist to localStorage
   - Clean, professional UI with clear visual feedback

**Files to create:**

- Standard Vite + Vue3 project structure
- Custom components for quiz functionality
- Minimal styling for a clean, professional look

---

## Part 3: GitHub Actions & GitHub Pages Deployment

Automate the build pipeline and deploy the quiz as a static site:

1. **GitHub Actions workflow** (`.github/workflows/deploy.yml`):

   - Trigger on push to `main` branch
   - Run Python parser to generate `questions.json` from `.docx`
   - Build Vue3 app with Vite
   - Deploy static files to GitHub Pages

2. **Workflow configuration:**

```yaml
name: Build and Deploy Quiz

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Run Python parser to generate questions.json
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Generate questions JSON
        run: python parser/parse_docx.py "CLD TECH ASSESSMENT.docx" -o quiz-app/public/questions.json

      # Build Vue3 app
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install and Build
        working-directory: quiz-app
        run: |
          npm ci
          npm run build

      # Deploy to GitHub Pages
      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./quiz-app/dist

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

3. **Vite configuration for GitHub Pages:**

```javascript
// quiz-app/vite.config.js
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  base: "/command-line-parser/", // repository name
});
```

4. **GitHub repo settings:**
   - Enable GitHub Pages under Settings → Pages
   - Set source to "GitHub Actions"

**Files to create:**

- `.github/workflows/deploy.yml` - CI/CD pipeline
- Update `quiz-app/vite.config.js` with correct `base` path

---

## Deliverables

1. `parser/` - Python CLI tool
2. `quiz-app/` - Vue3 web application
3. `.github/workflows/deploy.yml` - CI/CD pipeline
4. `README.md` - Brief instructions for running both parts
5. **Live demo** - Deployed quiz at `https://musicteachj.github.io/command-line-parser/`

---

## Technical Choices (for discussion)

- **Python for parser**: Matches CLD's stack, clean stdlib approach with `zipfile` and `xml.etree`
- **Vue3 Composition API**: Modern Vue best practices, matches what CLD uses
- **Vite**: Fast, modern build tool recommended for Vue3
- **Minimal dependencies**: Shows ability to work efficiently without over-engineering
- **GitHub Actions**: Industry-standard CI/CD, demonstrates DevOps knowledge
- **GitHub Pages**: Free static hosting, perfect for Vue3/Vite apps, zero config deployment

### To-dos

- [ ] Create Python CLI parser to extract questions from .docx to JSON
- [ ] Initialize Vue3 + Vite project
- [ ] Build quiz components with localStorage persistence
- [ ] Implement results display showing answers
- [ ] Configure Vite base path for GitHub Pages
- [ ] Create GitHub Actions workflow for automated deployment
- [ ] Add README with setup/run instructions
