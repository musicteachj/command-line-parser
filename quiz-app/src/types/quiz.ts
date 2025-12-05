export interface Choice {
  label: string;
  text: string;
}

export interface Question {
  id: number;
  text: string;
  correctLabel: string;
  choices: Choice[];
}

export interface QuizData {
  questions: Question[];
}

export type Answers = Record<number, string>;
