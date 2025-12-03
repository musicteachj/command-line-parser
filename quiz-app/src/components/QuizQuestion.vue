<script setup lang="ts">
import type { Question } from "../types/quiz";

defineProps<{
  question: Question;
  selectedAnswer: string | null;
  questionNumber: number;
  totalQuestions: number;
}>();

const emit = defineEmits<{
  select: [label: string];
}>();

const handleSelect = (label: string): void => {
  emit("select", label);
};
</script>

<template>
  <div class="question-container">
    <div class="question-header">
      <span class="question-badge"
        >Question {{ questionNumber }} of {{ totalQuestions }}</span
      >
    </div>

    <h2 class="question-text">{{ question.text }}</h2>

    <div class="choices-container">
      <label
        v-for="choice in question.choices"
        :key="choice.label"
        class="choice-item"
        :class="{ selected: selectedAnswer === choice.label }"
      >
        <input
          type="radio"
          :name="`question-${question.id}`"
          :value="choice.label"
          :checked="selectedAnswer === choice.label"
          @change="handleSelect(choice.label)"
        />
        <span class="choice-label">{{ choice.label }}</span>
        <span class="choice-text">{{ choice.text }}</span>
        <span class="choice-check" v-if="selectedAnswer === choice.label">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path
              d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"
            />
          </svg>
        </span>
      </label>
    </div>
  </div>
</template>

<style scoped>
.question-container {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.question-header {
  margin-bottom: 0.625rem;
}

.question-badge {
  display: inline-block;
  padding: 0.3rem 0.625rem;
  background: var(--accent-gradient);
  color: var(--bg-primary);
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 1.5rem;
  letter-spacing: 0.02em;
}

.question-text {
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 1rem;
  line-height: 1.4;
}

.choices-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.choice-item {
  display: flex;
  align-items: center;
  padding: 0.625rem 0.875rem;
  background: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.choice-item:hover {
  border-color: var(--accent-color);
  background: var(--bg-hover);
}

.choice-item.selected {
  border-color: var(--accent-color);
  background: var(--accent-bg);
}

.choice-item input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.choice-label {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.625rem;
  height: 1.625rem;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.75rem;
  border-radius: 6px;
  margin-right: 0.75rem;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.choice-item.selected .choice-label {
  background: var(--accent-color);
  color: var(--bg-primary);
}

.choice-text {
  flex: 1;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.choice-check {
  width: 1.125rem;
  height: 1.125rem;
  color: var(--accent-color);
  margin-left: 0.375rem;
  animation: scaleIn 0.2s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

.choice-check svg {
  width: 100%;
  height: 100%;
}
</style>
