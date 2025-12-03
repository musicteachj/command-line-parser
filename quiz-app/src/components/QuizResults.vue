<script setup lang="ts">
import { computed } from "vue";
import type { Question, Choice, Answers } from "../types/quiz";

const props = defineProps<{
  questions: Question[];
  answers: Answers;
}>();

const emit = defineEmits<{
  restart: [];
}>();

// Since there are no correct answers defined, we just show what the user selected
const totalAnswered = computed(() => {
  return Object.keys(props.answers).length;
});

const completionPercentage = computed(() => {
  return Math.round((totalAnswered.value / props.questions.length) * 100);
});

const getSelectedChoice = (question: Question): Choice | null => {
  const selectedLabel = props.answers[question.id];
  if (!selectedLabel) return null;
  return question.choices.find((c) => c.label === selectedLabel) ?? null;
};

const handleRestart = (): void => {
  emit("restart");
};
</script>

<template>
  <div class="results-container">
    <div class="results-header">
      <div class="results-icon">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
        >
          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
        </svg>
      </div>
      <h1 class="results-title">Quiz Complete!</h1>
      <p class="results-subtitle">Here's a summary of your responses</p>
    </div>

    <div class="stats-card">
      <div class="stat">
        <span class="stat-value">{{ totalAnswered }}</span>
        <span class="stat-label">Questions Answered</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat">
        <span class="stat-value">{{ questions.length }}</span>
        <span class="stat-label">Total Questions</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat">
        <span class="stat-value">{{ completionPercentage }}%</span>
        <span class="stat-label">Completion</span>
      </div>
    </div>

    <div class="answers-review">
      <h2 class="review-title">Your Answers</h2>

      <div
        v-for="(question, index) in questions"
        :key="question.id"
        class="answer-item"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="answer-header">
          <span class="answer-number">Q{{ index + 1 }}</span>
          <span class="answer-question">{{ question.text }}</span>
        </div>
        <div
          class="answer-response"
          :class="{ unanswered: !getSelectedChoice(question) }"
        >
          <template v-if="getSelectedChoice(question)">
            <span class="response-label">{{
              getSelectedChoice(question)?.label
            }}</span>
            <span class="response-text">{{
              getSelectedChoice(question)?.text
            }}</span>
          </template>
          <template v-else>
            <span class="response-text">Not answered</span>
          </template>
        </div>
      </div>
    </div>

    <button class="restart-btn" @click="handleRestart">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
      >
        <path
          d="M17.65 6.35A7.958 7.958 0 0012 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0112 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"
        />
      </svg>
      Take Quiz Again
    </button>
  </div>
</template>

<style scoped>
.results-container {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.results-header {
  text-align: center;
  margin-bottom: 1.25rem;
}

.results-icon {
  width: 2.5rem;
  height: 2.5rem;
  margin: 0 auto 0.5rem;
  background: var(--accent-gradient);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(var(--accent-rgb), 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(var(--accent-rgb), 0);
  }
}

.results-icon svg {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--bg-primary);
}

.results-title {
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.results-subtitle {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.stats-card {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  padding: 0.875rem 1.5rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  margin-bottom: 1.25rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.125rem;
}

.stat-value {
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--accent-color);
}

.stat-label {
  font-size: 0.625rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-divider {
  width: 1px;
  height: 2rem;
  background: var(--border-color);
}

.answers-review {
  margin-bottom: 1rem;
}

.review-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.625rem;
}

.answer-item {
  padding: 0.625rem 0.875rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  margin-bottom: 0.5rem;
  animation: slideIn 0.4s ease-out both;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.answer-header {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.375rem;
}

.answer-number {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 1.5rem;
  height: 1.5rem;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.625rem;
  border-radius: 4px;
  flex-shrink: 0;
}

.answer-question {
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.8125rem;
  line-height: 1.4;
}

.answer-response {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.625rem;
  background: var(--accent-bg);
  border-radius: 6px;
  margin-left: 2rem;
}

.answer-response.unanswered {
  background: var(--bg-tertiary);
}

.response-label {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.375rem;
  height: 1.375rem;
  background: var(--accent-color);
  color: var(--bg-primary);
  font-weight: 600;
  font-size: 0.6875rem;
  border-radius: 4px;
  flex-shrink: 0;
}

.response-text {
  color: var(--text-primary);
  font-size: 0.8125rem;
}

.answer-response.unanswered .response-text {
  color: var(--text-secondary);
  font-style: italic;
}

.restart-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  width: 100%;
  padding: 0.625rem 1.5rem;
  background: var(--accent-gradient);
  color: var(--bg-primary);
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.restart-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(var(--accent-rgb), 0.3);
}

.restart-btn svg {
  width: 1rem;
  height: 1rem;
}

@media (max-width: 600px) {
  .stats-card {
    flex-direction: column;
    gap: 1rem;
  }

  .stat-divider {
    width: 3rem;
    height: 1px;
  }

  .answer-response {
    margin-left: 0;
  }
}
</style>
