/**
 * Quiz helper functions for computing progress and state.
 * Extracted for testability.
 */

import type { Answers, Question } from "../types/quiz";

/**
 * Calculate quiz progress percentage based on current question index.
 */
export function calculateProgress(
  currentIndex: number,
  totalQuestions: number
): number {
  if (totalQuestions === 0) return 0;
  return Math.round(((currentIndex + 1) / totalQuestions) * 100);
}

/**
 * Count how many questions have been answered.
 */
export function countAnswered(answers: Answers): number {
  return Object.keys(answers).length;
}

/**
 * Check if all questions have been answered.
 */
export function isQuizComplete(
  answers: Answers,
  totalQuestions: number
): boolean {
  return countAnswered(answers) >= totalQuestions;
}

/**
 * Get unanswered question indices.
 */
export function getUnansweredQuestions(
  questions: Question[],
  answers: Answers
): number[] {
  return questions
    .map((q, index) => (answers[q.id] === undefined ? index : -1))
    .filter((index) => index !== -1);
}

/**
 * Validate that a question has the required structure.
 */
export function isValidQuestion(question: unknown): question is Question {
  if (!question || typeof question !== "object") return false;

  const q = question as Record<string, unknown>;

  return (
    typeof q.id === "number" &&
    typeof q.text === "string" &&
    Array.isArray(q.choices) &&
    q.choices.length === 4 &&
    q.choices.every(
      (c: unknown) =>
        c &&
        typeof c === "object" &&
        typeof (c as Record<string, unknown>).label === "string" &&
        typeof (c as Record<string, unknown>).text === "string"
    )
  );
}

