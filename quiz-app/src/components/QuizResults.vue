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

// Scoring computed properties
const correctAnswers = computed(() => {
  return props.questions.filter(
    (q) => props.answers[q.id] === q.correctLabel
  ).length;
});

const totalQuestions = computed(() => props.questions.length);

const scorePercentage = computed(() => {
  if (totalQuestions.value === 0) return 0;
  return Math.round((correctAnswers.value / totalQuestions.value) * 100);
});

const totalAnswered = computed(() => {
  return Object.keys(props.answers).length;
});

const getSelectedChoice = (question: Question): Choice | null => {
  const selectedLabel = props.answers[question.id];
  if (!selectedLabel) return null;
  return question.choices.find((c) => c.label === selectedLabel) ?? null;
};

const getCorrectChoice = (question: Question): Choice | null => {
  return question.choices.find((c) => c.label === question.correctLabel) ?? null;
};

const isCorrect = (question: Question): boolean => {
  return props.answers[question.id] === question.correctLabel;
};

const isAnswered = (question: Question): boolean => {
  return props.answers[question.id] !== undefined;
};

const getScoreMessage = computed(() => {
  const percent = scorePercentage.value;
  if (percent === 100) return "Perfect score! 🎉";
  if (percent >= 80) return "Excellent work! 🌟";
  if (percent >= 60) return "Good job! 👍";
  if (percent >= 40) return "Keep practicing! 📚";
  return "Don't give up! 💪";
});

const handleRestart = (): void => {
  emit("restart");
};
</script>

<template>
  <div class="results-container">
    <div class="results-header">
      <div class="results-icon" :class="{ perfect: scorePercentage === 100 }">
        <svg
          v-if="scorePercentage >= 60"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
        >
          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
        >
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
        </svg>
      </div>
      <h1 class="results-title">Quiz Complete!</h1>
      <p class="results-subtitle">{{ getScoreMessage }}</p>
    </div>

    <!-- Score Summary Card -->
    <div class="score-card">
      <div class="score-circle">
        <svg viewBox="0 0 36 36" class="circular-chart">
          <path
            class="circle-bg"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <path
            class="circle"
            :stroke-dasharray="`${scorePercentage}, 100`"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
        </svg>
        <div class="score-text">
          <span class="score-percent">{{ scorePercentage }}%</span>
        </div>
      </div>
      <div class="score-details">
        <p class="score-summary">
          You scored <strong>{{ correctAnswers }}</strong> out of <strong>{{ totalQuestions }}</strong>
        </p>
        <div class="score-breakdown">
          <span class="breakdown-item correct">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
            </svg>
            {{ correctAnswers }} Correct
          </span>
          <span class="breakdown-item incorrect">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" />
            </svg>
            {{ totalQuestions - correctAnswers }} Incorrect
          </span>
        </div>
      </div>
    </div>

    <div class="answers-review">
      <h2 class="review-title">Your Answers</h2>

      <div
        v-for="(question, index) in questions"
        :key="question.id"
        class="answer-item"
        :class="{ 
          correct: isAnswered(question) && isCorrect(question), 
          incorrect: isAnswered(question) && !isCorrect(question),
          unanswered: !isAnswered(question)
        }"
        :style="{ animationDelay: `${index * 0.1}s` }"
      >
        <div class="answer-header">
          <span class="answer-number">Q{{ index + 1 }}</span>
          <span class="answer-question">{{ question.text }}</span>
          <span class="answer-status">
            <svg
              v-if="isAnswered(question) && isCorrect(question)"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="status-icon correct"
            >
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
            </svg>
            <svg
              v-else-if="isAnswered(question)"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="status-icon incorrect"
            >
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" />
            </svg>
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="status-icon skipped"
            >
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" />
            </svg>
          </span>
        </div>
        
        <div class="answer-content">
          <!-- User's Answer -->
          <div
            class="answer-response"
            :class="{ 
              'user-correct': isAnswered(question) && isCorrect(question),
              'user-incorrect': isAnswered(question) && !isCorrect(question),
              'unanswered': !isAnswered(question)
            }"
          >
            <span class="response-prefix">Your answer:</span>
            <template v-if="getSelectedChoice(question)">
              <span class="response-label">{{
                getSelectedChoice(question)?.label
              }}</span>
              <span class="response-text">{{
                getSelectedChoice(question)?.text
              }}</span>
            </template>
            <template v-else>
              <span class="response-text not-answered">Not answered</span>
            </template>
          </div>

          <!-- Correct Answer (shown if user was wrong or didn't answer) -->
          <div
            v-if="!isCorrect(question) || !isAnswered(question)"
            class="answer-response correct-answer"
          >
            <span class="response-prefix">Correct answer:</span>
            <span class="response-label">{{
              getCorrectChoice(question)?.label
            }}</span>
            <span class="response-text">{{
              getCorrectChoice(question)?.text
            }}</span>
          </div>
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

.results-icon.perfect {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
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

/* Score Card Styles */
.score-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.25rem 1.5rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  margin-bottom: 1.25rem;
}

.score-circle {
  position: relative;
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.circular-chart {
  display: block;
  width: 100%;
  height: 100%;
}

.circle-bg {
  fill: none;
  stroke: var(--bg-tertiary);
  stroke-width: 3;
}

.circle {
  fill: none;
  stroke: var(--accent-color);
  stroke-width: 3;
  stroke-linecap: round;
  animation: progress 1s ease-out forwards;
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}

@keyframes progress {
  0% {
    stroke-dasharray: 0, 100;
  }
}

.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.score-percent {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent-color);
}

.score-details {
  flex: 1;
}

.score-summary {
  font-size: 1rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.score-summary strong {
  color: var(--accent-color);
}

.score-breakdown {
  display: flex;
  gap: 1rem;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8125rem;
  font-weight: 500;
}

.breakdown-item svg {
  width: 0.875rem;
  height: 0.875rem;
}

.breakdown-item.correct {
  color: #10b981;
}

.breakdown-item.incorrect {
  color: #ef4444;
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
  transition: border-color 0.2s ease;
}

.answer-item.correct {
  border-color: rgba(16, 185, 129, 0.4);
  background: linear-gradient(to right, rgba(16, 185, 129, 0.05), transparent);
}

.answer-item.incorrect {
  border-color: rgba(239, 68, 68, 0.4);
  background: linear-gradient(to right, rgba(239, 68, 68, 0.05), transparent);
}

.answer-item.unanswered {
  border-color: rgba(234, 179, 8, 0.4);
  background: linear-gradient(to right, rgba(234, 179, 8, 0.05), transparent);
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
  flex: 1;
}

.answer-status {
  flex-shrink: 0;
}

.status-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.status-icon.correct {
  color: #10b981;
}

.status-icon.incorrect {
  color: #ef4444;
}

.status-icon.skipped {
  color: #eab308;
}

.answer-content {
  margin-left: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.answer-response {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.625rem;
  border-radius: 6px;
}

.answer-response.user-correct {
  background: rgba(16, 185, 129, 0.15);
}

.answer-response.user-incorrect {
  background: rgba(239, 68, 68, 0.15);
}

.answer-response.unanswered {
  background: var(--bg-tertiary);
}

.answer-response.correct-answer {
  background: rgba(16, 185, 129, 0.1);
  border: 1px dashed rgba(16, 185, 129, 0.3);
}

.response-prefix {
  font-size: 0.6875rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  flex-shrink: 0;
}

.response-label {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.375rem;
  height: 1.375rem;
  font-weight: 600;
  font-size: 0.6875rem;
  border-radius: 4px;
  flex-shrink: 0;
}

.user-correct .response-label {
  background: #10b981;
  color: white;
}

.user-incorrect .response-label {
  background: #ef4444;
  color: white;
}

.correct-answer .response-label {
  background: #10b981;
  color: white;
}

.response-text {
  color: var(--text-primary);
  font-size: 0.8125rem;
}

.response-text.not-answered {
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
  .score-card {
    flex-direction: column;
    text-align: center;
  }

  .score-breakdown {
    justify-content: center;
  }

  .answer-content {
    margin-left: 0;
  }
}
</style>
