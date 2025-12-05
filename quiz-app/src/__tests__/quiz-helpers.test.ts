/**
 * Automated tests for quiz helper functions.
 *
 * Run with: npm test
 */

import { describe, it, expect } from "vitest";
import {
  calculateProgress,
  countAnswered,
  isQuizComplete,
  getUnansweredQuestions,
  isValidQuestion,
} from "../utils/quiz-helpers";
import type { Question, Answers } from "../types/quiz";

describe("Quiz Helper Functions", () => {
  // Sample questions for testing
  const mockQuestions: Question[] = [
    {
      id: 1,
      text: "Question 1?",
      correctLabel: "A",
      choices: [
        { label: "A", text: "Answer A" },
        { label: "B", text: "Answer B" },
        { label: "C", text: "Answer C" },
        { label: "D", text: "Answer D" },
      ],
    },
    {
      id: 2,
      text: "Question 2?",
      correctLabel: "B",
      choices: [
        { label: "A", text: "Answer A" },
        { label: "B", text: "Answer B" },
        { label: "C", text: "Answer C" },
        { label: "D", text: "Answer D" },
      ],
    },
    {
      id: 3,
      text: "Question 3?",
      correctLabel: "C",
      choices: [
        { label: "A", text: "Answer A" },
        { label: "B", text: "Answer B" },
        { label: "C", text: "Answer C" },
        { label: "D", text: "Answer D" },
      ],
    },
  ];

  describe("calculateProgress", () => {
    it("returns 0 for empty question list", () => {
      expect(calculateProgress(0, 0)).toBe(0);
    });

    it("returns correct percentage for first question", () => {
      // First question (index 0) of 3 = 33%
      expect(calculateProgress(0, 3)).toBe(33);
    });

    it("returns correct percentage for middle question", () => {
      // Second question (index 1) of 3 = 67%
      expect(calculateProgress(1, 3)).toBe(67);
    });

    it("returns 100 for last question", () => {
      // Third question (index 2) of 3 = 100%
      expect(calculateProgress(2, 3)).toBe(100);
    });

    it("handles single question quiz", () => {
      expect(calculateProgress(0, 1)).toBe(100);
    });
  });

  describe("countAnswered", () => {
    it("returns 0 for empty answers", () => {
      const answers: Answers = {};
      expect(countAnswered(answers)).toBe(0);
    });

    it("returns correct count for partial answers", () => {
      const answers: Answers = { 1: "A", 2: "B" };
      expect(countAnswered(answers)).toBe(2);
    });

    it("returns correct count for all answers", () => {
      const answers: Answers = { 1: "A", 2: "B", 3: "C" };
      expect(countAnswered(answers)).toBe(3);
    });
  });

  describe("isQuizComplete", () => {
    it("returns false when no answers", () => {
      expect(isQuizComplete({}, 3)).toBe(false);
    });

    it("returns false when partially answered", () => {
      expect(isQuizComplete({ 1: "A", 2: "B" }, 3)).toBe(false);
    });

    it("returns true when all questions answered", () => {
      expect(isQuizComplete({ 1: "A", 2: "B", 3: "C" }, 3)).toBe(true);
    });

    it("returns true for empty quiz", () => {
      expect(isQuizComplete({}, 0)).toBe(true);
    });
  });

  describe("getUnansweredQuestions", () => {
    it("returns all indices when no answers", () => {
      const result = getUnansweredQuestions(mockQuestions, {});
      expect(result).toEqual([0, 1, 2]);
    });

    it("returns empty array when all answered", () => {
      const answers: Answers = { 1: "A", 2: "B", 3: "C" };
      const result = getUnansweredQuestions(mockQuestions, answers);
      expect(result).toEqual([]);
    });

    it("returns correct indices for partial answers", () => {
      const answers: Answers = { 1: "A", 3: "C" };
      const result = getUnansweredQuestions(mockQuestions, answers);
      expect(result).toEqual([1]); // Question 2 (index 1) is unanswered
    });
  });

  describe("isValidQuestion", () => {
    it("returns true for valid question", () => {
      expect(isValidQuestion(mockQuestions[0])).toBe(true);
    });

    it("returns false for null", () => {
      expect(isValidQuestion(null)).toBe(false);
    });

    it("returns false for undefined", () => {
      expect(isValidQuestion(undefined)).toBe(false);
    });

    it("returns false for missing id", () => {
      expect(
        isValidQuestion({
          text: "Question?",
          correctLabel: "A",
          choices: [],
        })
      ).toBe(false);
    });

    it("returns false for missing text", () => {
      expect(
        isValidQuestion({
          id: 1,
          correctLabel: "A",
          choices: [],
        })
      ).toBe(false);
    });

    it("returns false for wrong number of choices", () => {
      expect(
        isValidQuestion({
          id: 1,
          text: "Question?",
          correctLabel: "A",
          choices: [{ label: "A", text: "Only one" }],
        })
      ).toBe(false);
    });

    it("returns false for invalid choice structure", () => {
      expect(
        isValidQuestion({
          id: 1,
          text: "Question?",
          correctLabel: "A",
          choices: [
            { label: "A" }, // missing text
            { label: "B", text: "B" },
            { label: "C", text: "C" },
            { label: "D", text: "D" },
          ],
        })
      ).toBe(false);
    });
  });
});

