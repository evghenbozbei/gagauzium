export type BaseLanguage = 'ru' | 'ro';

export type CategoryLevel = 'beginner' | 'conversational' | 'advanced' | 'expert';

export interface Category {
  id: string;
  gagauzName: string;
  nameRu: string;
  nameRo: string;
  descriptionRu: string;
  descriptionRo: string;
  iconName: string;
  color: string; // TailWind primary accent color hex/class
  bgGradient: string;
  level: CategoryLevel;
}

export type WordStatus = 'unlearned' | 'learning' | 'learned' | 'difficult';

export interface Word {
  id: string;
  categoryId: string;
  gagauz: string;
  ru: string;
  ro: string;
  pronunciation: string;
  exampleGagauz?: string;
  exampleRu?: string;
  exampleRo?: string;
}

export interface UserWordState {
  status: WordStatus;
  errorCount: number;
  lastReviewedAt?: number;
  timesCorrect: number;
}

export type ExerciseType = 'multiple_choice' | 'true_false' | 'word_building';

export interface ExerciseQuestion {
  id: string;
  type: ExerciseType;
  word: Word;
  promptText: string;
  targetTranslation: string;
  options?: string[]; // For multiple choice
  statementTranslation?: string; // For true/false (may be correct or distractor)
  isStatementTrue?: boolean; // For true/false
  letterBank?: string[]; // For word building
}

export type NavTab = 'home' | 'learn' | 'review';

export type ScreenState =
  | { type: 'home' }
  | { type: 'learn' }
  | { type: 'review' }
  | { type: 'category_detail'; categoryId: string }
  | { type: 'learned_words'; categoryId: string }
  | {
      type: 'exercise';
      mode: 'category_new' | 'category_difficult' | 'daily' | 'difficult' | 'quick' | 'quiz';
      categoryId?: string;
    }
  | {
      type: 'session_complete';
      stats: {
        total: number;
        correct: number;
        xp: number;
        newWordsLearned: number;
      };
    };

export interface AppState {
  baseLanguage: BaseLanguage;
  userWords: Record<string, UserWordState>;
  streakDays: number;
  lastCategoryId: string;
  selectedLevel: CategoryLevel;
  activeScreen: ScreenState;
}
