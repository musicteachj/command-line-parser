<script setup lang="ts">
import { ref, reactive, watch, onMounted, computed } from "vue";
import QuizQuestion from "./components/QuizQuestion.vue";
import QuizResults from "./components/QuizResults.vue";
import type { Question, QuizData, Answers } from "./types/quiz";

// State
const questions = ref<Question[]>([]);
const answers: Answers = reactive({});
const currentQuestionIndex = ref(0);
const quizCompleted = ref(false);
const hasStarted = ref(false);
const isLoading = ref(true);
const error = ref<string | null>(null);

// LocalStorage keys
const STORAGE_KEY_ANSWERS = "quiz-answers";
const STORAGE_KEY_INDEX = "quiz-current-index";
const STORAGE_KEY_COMPLETED = "quiz-completed";
const STORAGE_KEY_STARTED = "quiz-started";

// Computed
const currentQuestion = computed(
  () => questions.value[currentQuestionIndex.value]
);
const currentAnswer = computed(() => answers[currentQuestion.value?.id]);
const isFirstQuestion = computed(() => currentQuestionIndex.value === 0);
const isLastQuestion = computed(
  () => currentQuestionIndex.value === questions.value.length - 1
);
const progress = computed(() => {
  if (questions.value.length === 0) return 0;
  return Math.round(
    ((currentQuestionIndex.value + 1) / questions.value.length) * 100
  );
});
const answeredCount = computed(() => Object.keys(answers).length);

// Load questions from JSON
const loadQuestions = async (): Promise<void> => {
  try {
    const response = await fetch("./questions.json");
    if (!response.ok) throw new Error("Failed to load questions");
    const data: QuizData = await response.json();
    questions.value = data.questions;
  } catch (e) {
    error.value = "Failed to load quiz questions. Please try again.";
    console.error("Error loading questions:", e);
  } finally {
    isLoading.value = false;
  }
};

// Load saved state from localStorage
const loadSavedState = (): void => {
  try {
    const savedAnswers = localStorage.getItem(STORAGE_KEY_ANSWERS);
    const savedIndex = localStorage.getItem(STORAGE_KEY_INDEX);
    const savedCompleted = localStorage.getItem(STORAGE_KEY_COMPLETED);
    const savedStarted = localStorage.getItem(STORAGE_KEY_STARTED);

    if (savedAnswers) {
      Object.assign(answers, JSON.parse(savedAnswers));
    }
    if (savedIndex !== null) {
      currentQuestionIndex.value = parseInt(savedIndex, 10);
    }
    if (savedCompleted === "true") {
      quizCompleted.value = true;
    }
    if (savedStarted === "true") {
      hasStarted.value = true;
    }
  } catch (e) {
    console.error("Error loading saved state:", e);
  }
};

// Save state to localStorage
const saveToLocalStorage = (): void => {
  try {
    localStorage.setItem(STORAGE_KEY_ANSWERS, JSON.stringify(answers));
    localStorage.setItem(
      STORAGE_KEY_INDEX,
      currentQuestionIndex.value.toString()
    );
    localStorage.setItem(STORAGE_KEY_COMPLETED, quizCompleted.value.toString());
    localStorage.setItem(STORAGE_KEY_STARTED, hasStarted.value.toString());
  } catch (e) {
    console.error("Error saving state:", e);
  }
};

// Watch for changes and persist
watch(answers, saveToLocalStorage, { deep: true });
watch(currentQuestionIndex, saveToLocalStorage);
watch(quizCompleted, saveToLocalStorage);
watch(hasStarted, saveToLocalStorage);

// Actions
const selectAnswer = (label: string): void => {
  if (currentQuestion.value) {
    answers[currentQuestion.value.id] = label;
  }
};

const goToQuestion = (index: number): void => {
  if (index >= 0 && index < questions.value.length) {
    currentQuestionIndex.value = index;
  }
};

const goNext = (): void => {
  if (!isLastQuestion.value) {
    currentQuestionIndex.value++;
  }
};

const goPrevious = (): void => {
  if (!isFirstQuestion.value) {
    currentQuestionIndex.value--;
  }
};

const submitQuiz = (): void => {
  quizCompleted.value = true;
};

const startQuiz = (): void => {
  hasStarted.value = true;
  quizCompleted.value = false;

  // Ensure we have a valid starting index
  if (questions.value.length > 0) {
    if (
      currentQuestionIndex.value < 0 ||
      currentQuestionIndex.value >= questions.value.length
    ) {
      currentQuestionIndex.value = 0;
    }
  }
};

const restartQuiz = (): void => {
  // Clear all state
  Object.keys(answers).forEach((key) => delete answers[Number(key)]);
  currentQuestionIndex.value = 0;
  quizCompleted.value = false;

  // Clear localStorage
  localStorage.removeItem(STORAGE_KEY_ANSWERS);
  localStorage.removeItem(STORAGE_KEY_INDEX);
  localStorage.removeItem(STORAGE_KEY_COMPLETED);
};

// Initialize
onMounted(async () => {
  await loadQuestions();
  loadSavedState();
});
</script>

<template>
  <div class="app">
    <header class="header">
      <h1 class="logo">
        <span class="logo-icon">✦</span>
        QuizMaster
      </h1>
    </header>

    <main class="main">
      <!-- Loading State -->
      <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>Loading quiz...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="loadQuestions">Try Again</button>
      </div>

      <!-- Intro / Landing Screen -->
      <div
        v-else-if="!quizCompleted && !hasStarted && questions.length"
        class="intro"
      >
        <div class="intro-card">
          <h2 class="intro-title">Document-driven quiz</h2>
          <p class="intro-text">
            This quiz was generated from a Word document via a custom Python parser.
          </p>
          <p class="intro-subtext">
            Behind the scenes, a CLI extracts questions into JSON that this app
            renders as an interactive experience.
          </p>
          <button class="intro-button" @click="startQuiz">
            Start Quiz
          </button>
        </div>
      </div>

      <!-- Results Screen -->
      <QuizResults
        v-else-if="quizCompleted"
        :questions="questions"
        :answers="answers"
        @restart="restartQuiz"
      />

      <!-- Quiz Screen -->
      <template v-else-if="hasStarted && currentQuestion">
        <!-- Progress Bar -->
        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
          </div>
          <span class="progress-text"
            >{{ answeredCount }} of {{ questions.length }} answered</span
          >
        </div>

        <!-- Question Navigator -->
        <div class="question-nav">
          <button
            v-for="(q, index) in questions"
            :key="q.id"
            class="nav-dot"
            :class="{
              active: index === currentQuestionIndex,
              answered: answers[q.id],
            }"
            @click="goToQuestion(index)"
            :title="`Question ${index + 1}`"
          >
            {{ index + 1 }}
          </button>
        </div>

        <!-- Question Component -->
        <QuizQuestion
          :key="currentQuestion.id"
          :question="currentQuestion"
          :selected-answer="currentAnswer"
          :question-number="currentQuestionIndex + 1"
          :total-questions="questions.length"
          @select="selectAnswer"
        />

        <!-- Navigation Buttons -->
        <div class="nav-buttons">
          <button
            class="nav-btn secondary"
            :disabled="isFirstQuestion"
            @click="goPrevious"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12l4.58-4.59z"
              />
            </svg>
            Previous
          </button>

          <button
            v-if="!isLastQuestion"
            class="nav-btn primary"
            @click="goNext"
          >
            Next
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12l-4.58 4.59z"
              />
            </svg>
          </button>

          <button
            v-else
            class="nav-btn submit"
            :disabled="answeredCount < questions.length"
            @click="submitQuiz"
          >
            Submit Quiz
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"
              />
            </svg>
          </button>
        </div>
      </template>
    </main>

    <footer class="footer">
      <p>Your progress is automatically saved</p>
    </footer>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  padding: 0.625rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.logo-icon {
  color: var(--accent-color);
  font-size: 1.25rem;
}

.main {
  flex: 1;
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
  padding: 1rem 2rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 3px solid var(--border-color);
  border-top-color: var(--accent-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.error-state button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: var(--accent-color);
  color: var(--bg-primary);
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.intro {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
}

.intro-card {
  max-width: 520px;
  width: 100%;
  padding: 1.75rem 1.75rem 1.5rem;
  border-radius: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.intro-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.intro-text {
  color: var(--text-primary);
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.intro-subtext {
  color: var(--text-secondary);
  font-size: 0.85rem;
  margin-bottom: 1.25rem;
}

.intro-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  background: var(--accent-gradient);
  color: var(--bg-primary);
  box-shadow: 0 10px 25px rgba(var(--accent-rgb), 0.4);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.intro-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 32px rgba(var(--accent-rgb), 0.45);
}

.progress-container {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.progress-bar {
  height: 4px;
  background: var(--bg-tertiary);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.375rem;
}

.progress-fill {
  height: 100%;
  background: var(--accent-gradient);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.question-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  margin-bottom: 1rem;
}

.nav-dot {
  width: 1.875rem;
  height: 1.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-dot:hover {
  border-color: var(--accent-color);
}

.nav-dot.active {
  background: var(--accent-color);
  border-color: var(--accent-color);
  color: var(--bg-primary);
}

.nav-dot.answered:not(.active) {
  background: var(--accent-bg);
  border-color: var(--accent-color);
  color: var(--accent-color);
}

.nav-buttons {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  margin-top: 1.25rem;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.625rem 1.125rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-btn svg {
  width: 1rem;
  height: 1rem;
}

.nav-btn.secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
}

.nav-btn.secondary:hover:not(:disabled) {
  border-color: var(--accent-color);
}

.nav-btn.secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-btn.primary {
  background: var(--accent-gradient);
  color: var(--bg-primary);
  margin-left: auto;
}

.nav-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(var(--accent-rgb), 0.3);
}

.nav-btn.submit {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  margin-left: auto;
}

.nav-btn.submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
}

.nav-btn.submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
}

.footer {
  padding: 0.5rem 1.5rem;
  text-align: center;
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.footer p {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

@media (max-width: 600px) {
  .main {
    padding: 1.5rem 1rem;
  }

  .nav-buttons {
    flex-wrap: wrap;
  }

  .nav-btn {
    flex: 1;
    justify-content: center;
    min-width: 120px;
  }
}
</style>
