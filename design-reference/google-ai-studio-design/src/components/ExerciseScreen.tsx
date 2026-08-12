import React, { useState, useEffect } from 'react';
import { ArrowLeft, Check, X, Volume2, Sparkles, RefreshCw } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { ExerciseQuestion, Word } from '../types';
import { getTranslation } from '../data/translations';
import { CATEGORIES } from '../data/categories';

interface ExerciseScreenProps {
  mode: 'category_new' | 'category_difficult' | 'daily' | 'difficult' | 'quick' | 'quiz';
  categoryId?: string;
}

export const ExerciseScreen: React.FC<ExerciseScreenProps> = ({ mode, categoryId }) => {
  const {
    baseLanguage,
    allWords,
    userWords,
    recordWordResult,
    navigateTo,
    getWordsByCategoryId
  } = useApp();

  const t = getTranslation(baseLanguage);

  const [questions, setQuestions] = useState<ExerciseQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [selectedOption, setSelectedOption] = useState<string | boolean | null>(null);
  const [builtLetters, setBuiltLetters] = useState<string[]>([]);
  const [selectedLetterIndices, setSelectedLetterIndices] = useState<number[]>([]);
  const [isAnswered, setIsAnswered] = useState<boolean>(false);
  const [isCorrect, setIsCorrect] = useState<boolean>(false);
  const [sessionScore, setSessionScore] = useState<{ total: number; correct: number; xp: number }>({
    total: 0,
    correct: 0,
    xp: 0
  });

  // Helper to shuffle array
  const shuffle = <T,>(arr: T[]): T[] => {
    return [...arr].sort(() => Math.random() - 0.5);
  };

  // Generate Questions for Session
  useEffect(() => {
    let sourceWords: Word[] = [];

    if (categoryId) {
      const catWords = getWordsByCategoryId(categoryId);
      if (mode === 'category_new') {
        sourceWords = catWords.filter((w) => (userWords[w.id]?.status || 'unlearned') !== 'learned');
      } else if (mode === 'category_difficult') {
        sourceWords = catWords.filter((w) => userWords[w.id]?.status === 'difficult');
      }
      if (sourceWords.length === 0) sourceWords = catWords;
    } else {
      if (mode === 'difficult') {
        sourceWords = allWords.filter((w) => userWords[w.id]?.status === 'difficult');
      } else if (mode === 'daily') {
        sourceWords = allWords.filter((w) => (userWords[w.id]?.status || 'unlearned') !== 'unlearned');
      }
      if (sourceWords.length === 0) sourceWords = allWords;
    }

    const limit = mode === 'quick' ? 5 : mode === 'quiz' ? 10 : Math.min(20, Math.max(5, sourceWords.length));
    const selectedWords = shuffle(sourceWords).slice(0, limit);

    const generatedQuestions: ExerciseQuestion[] = selectedWords.map((word, idx) => {
      // Rotate exercise formats across session automatically as requested!
      // 1. Multiple choice, 2. True/False, 3. Word building, etc.
      const types: ('multiple_choice' | 'true_false' | 'word_building')[] = [
        'multiple_choice',
        'true_false',
        'word_building'
      ];
      const type = types[idx % types.length];

      const targetTrans = baseLanguage === 'ru' ? word.ru : word.ro;

      // Distractor translations from other words
      const otherWords = allWords.filter((w: Word) => w.id !== word.id);
      const distractors = shuffle(otherWords)
        .slice(0, 3)
        .map((w: Word) => (baseLanguage === 'ru' ? w.ru : w.ro));

      if (type === 'multiple_choice') {
        const options = shuffle([targetTrans, ...distractors]);
        return {
          id: `q_${word.id}_${idx}`,
          type,
          word,
          promptText: word.gagauz,
          targetTranslation: targetTrans,
          options,
          correctAnswer: targetTrans
        };
      } else if (type === 'true_false') {
        const isTrue = Math.random() > 0.5;
        const statementTrans = isTrue ? targetTrans : distractors[0];
        return {
          id: `q_${word.id}_${idx}`,
          type,
          word,
          promptText: word.gagauz,
          targetTranslation: targetTrans,
          statementTranslation: statementTrans,
          isStatementTrue: isTrue,
          correctAnswer: isTrue
        };
      } else {
        // Word Building
        const gagauzClean = word.gagauz.toUpperCase().replace(/[^A-ZÇĞIİÖŞÜÄÖ]/g, '');
        const targetLetters = gagauzClean.split('');

        // Distractor letters
        const extraLettersPool = ['A', 'E', 'I', 'O', 'U', 'N', 'R', 'S', 'T', 'K', 'B', 'D'];
        const extraLetters = shuffle(extraLettersPool.filter((l) => !targetLetters.includes(l))).slice(0, 3);

        const letterBank = shuffle([...targetLetters, ...extraLetters]);

        return {
          id: `q_${word.id}_${idx}`,
          type,
          word,
          promptText: targetTrans,
          targetTranslation: word.gagauz,
          letterBank,
          correctAnswer: word.gagauz.toUpperCase()
        };
      }
    });

    setQuestions(generatedQuestions);
    setCurrentIndex(0);
    setBuiltLetters([]);
    setSelectedLetterIndices([]);
    setIsAnswered(false);
    setSelectedOption(null);
  }, [mode, categoryId, baseLanguage]);

  const currentQ = questions[currentIndex];

  if (!currentQ) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] p-4 text-center">
        <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mb-3" />
        <p className="text-sm font-semibold text-slate-600">
          {baseLanguage === 'ru' ? 'Загрузка упражнения...' : 'Se încarcă exercițiul...'}
        </p>
      </div>
    );
  }

  const category = CATEGORIES.find((c) => c.id === currentQ.word.categoryId) || CATEGORIES[0];
  const sessionTitle = categoryId
    ? baseLanguage === 'ru'
      ? category.nameRu
      : category.nameRo
    : mode === 'daily'
    ? t.dailyReviewTitle
    : mode === 'difficult'
    ? t.difficultWordsTitle
    : mode === 'quick'
    ? t.quickReviewTitle
    : t.quizTitle;

  // Speak word TTS
  const speakCurrentWord = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(currentQ.word.gagauz);
      utterance.lang = 'tr-TR';
      utterance.rate = 0.85;
      window.speechSynthesis.speak(utterance);
    }
  };

  // Evaluate Answer
  const handleEvaluateAnswer = (userAnswer: string | boolean) => {
    if (isAnswered) return;

    let correct = false;
    if (currentQ.type === 'multiple_choice') {
      correct = userAnswer === currentQ.correctAnswer;
    } else if (currentQ.type === 'true_false') {
      correct = userAnswer === currentQ.correctAnswer;
    } else if (currentQ.type === 'word_building') {
      const builtStr = (userAnswer as string).toUpperCase().replace(/\s+/g, '');
      const targetStr = (currentQ.correctAnswer as string).toUpperCase().replace(/\s+/g, '');
      correct = builtStr === targetStr;
    }

    setIsCorrect(correct);
    setIsAnswered(true);

    // Save result to context
    recordWordResult(currentQ.word.id, correct);

    // Update Session Score
    setSessionScore((prev) => ({
      total: prev.total + 1,
      correct: prev.correct + (correct ? 1 : 0),
      xp: prev.xp + (correct ? 10 : 2)
    }));

    if (correct) {
      speakCurrentWord();
    }
  };

  // Word building letter selection
  const handleSelectLetter = (letter: string, index: number) => {
    if (selectedLetterIndices.includes(index) || isAnswered) return;
    setBuiltLetters((prev) => [...prev, letter]);
    setSelectedLetterIndices((prev) => [...prev, index]);
  };

  const handleRemoveLetter = (builtIndex: number) => {
    if (isAnswered) return;
    const removedLetter = builtLetters[builtIndex];
    setBuiltLetters((prev) => prev.filter((_, idx) => idx !== builtIndex));

    // Remove from selected bank indices
    const originalBankIdx = selectedLetterIndices.find(
      (bankIdx) => currentQ.letterBank && currentQ.letterBank[bankIdx] === removedLetter
    );
    if (originalBankIdx !== undefined) {
      setSelectedLetterIndices((prev) => prev.filter((i) => i !== originalBankIdx));
    }
  };

  const handleClearLetters = () => {
    if (isAnswered) return;
    setBuiltLetters([]);
    setSelectedLetterIndices([]);
  };

  const handleContinueNext = () => {
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption(null);
      setBuiltLetters([]);
      setSelectedLetterIndices([]);
      setIsAnswered(false);
      setIsCorrect(false);
    } else {
      // Session Completed! Navigate to complete screen
      navigateTo({
        type: 'session_complete',
        stats: {
          total: sessionScore.total,
          correct: sessionScore.correct,
          xp: sessionScore.xp,
          newWordsLearned: sessionScore.correct
        }
      });
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-between max-w-md mx-auto pb-safe">
      {/* Top Header Bar */}
      <div className="bg-white border-b border-slate-100 p-4 sticky top-0 z-20 shadow-2xs">
        <div className="flex items-center justify-between gap-3 mb-2">
          {/* ← Back button */}
          <button
            onClick={() => {
              if (categoryId) {
                navigateTo({ type: 'category_detail', categoryId });
              } else {
                navigateTo({ type: 'home' });
              }
            }}
            className="flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 bg-slate-100 px-3 py-1.5 rounded-xl transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>{t.backCTA}</span>
          </button>

          {/* Session Title */}
          <span className="text-xs font-extrabold text-slate-900 truncate">
            {sessionTitle}
          </span>

          {/* Progress Counter e.g. 7 / 20 */}
          <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-100">
            {currentIndex + 1} / {questions.length}
          </span>
        </div>

        {/* Thin Progress Bar */}
        <div className="w-full bg-slate-100 rounded-full h-1.5">
          <div
            className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
            style={{
              width: `${Math.round(((currentIndex + 1) / questions.length) * 100)}%`
            }}
          />
        </div>
      </div>

      {/* Central Area Question Content */}
      <div className="flex-1 p-4 flex flex-col justify-center space-y-6 my-auto">
        {/* Prominent Word Card */}
        <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-xs text-center relative">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-2">
            {currentQ.type === 'multiple_choice' && t.chooseCorrectTranslation}
            {currentQ.type === 'true_false' && t.isThisCorrect}
            {currentQ.type === 'word_building' && t.buildGagauzWord}
          </span>

          <div className="flex items-center justify-center gap-2 mb-2">
            <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              {currentQ.promptText}
            </h1>
            {currentQ.type !== 'word_building' && (
              <button
                onClick={speakCurrentWord}
                className="p-2 rounded-full text-blue-600 hover:bg-blue-50 transition-colors"
                title={t.pronunciation}
              >
                <Volume2 className="w-5 h-5" />
              </button>
            )}
          </div>

          <p className="text-xs text-slate-500 font-medium">
            {currentQ.word.pronunciation}
          </p>

          {/* True/False Statement prompt */}
          {currentQ.type === 'true_false' && (
            <div className="mt-4 p-3 bg-indigo-50/60 rounded-2xl border border-indigo-100">
              <p className="text-xs font-bold text-indigo-950">
                "{currentQ.statementTranslation}"
              </p>
            </div>
          )}
        </div>

        {/* Interactive Answer Area based on Exercise Type */}

        {/* Type A — Multiple Choice */}
        {currentQ.type === 'multiple_choice' && currentQ.options && (
          <div className="grid grid-cols-1 gap-2.5">
            {currentQ.options.map((opt, idx) => {
              const isSelected = selectedOption === opt;
              let optionClass =
                'bg-white text-slate-800 border-slate-200 hover:border-blue-300 hover:bg-blue-50/40';

              if (isAnswered) {
                if (opt === currentQ.correctAnswer) {
                  optionClass = 'bg-emerald-500 text-white border-emerald-500 font-bold';
                } else if (isSelected && !isCorrect) {
                  optionClass = 'bg-rose-500 text-white border-rose-500 font-bold';
                } else {
                  optionClass = 'bg-slate-100 text-slate-400 border-transparent opacity-60';
                }
              }

              return (
                <button
                  key={idx}
                  onClick={() => {
                    setSelectedOption(opt);
                    handleEvaluateAnswer(opt);
                  }}
                  disabled={isAnswered}
                  className={`w-full py-4 px-5 rounded-2xl border-2 text-left text-sm font-bold transition-all flex items-center justify-between ${optionClass}`}
                >
                  <span>{opt}</span>
                  <span className="w-6 h-6 rounded-full border border-current flex items-center justify-center text-xs opacity-75">
                    {idx + 1}
                  </span>
                </button>
              );
            })}
          </div>
        )}

        {/* Type B — True / False */}
        {currentQ.type === 'true_false' && (
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => {
                setSelectedOption(true);
                handleEvaluateAnswer(true);
              }}
              disabled={isAnswered}
              className={`py-5 px-4 rounded-2xl border-2 font-black text-base transition-all flex flex-col items-center justify-center gap-1 ${
                isAnswered
                  ? currentQ.correctAnswer === true
                    ? 'bg-emerald-500 text-white border-emerald-500'
                    : selectedOption === true
                    ? 'bg-rose-500 text-white border-rose-500'
                    : 'bg-slate-100 text-slate-400'
                  : 'bg-white text-emerald-700 border-emerald-200 hover:bg-emerald-50'
              }`}
            >
              <Check className="w-6 h-6" />
              <span>{t.trueBtn}</span>
            </button>

            <button
              onClick={() => {
                setSelectedOption(false);
                handleEvaluateAnswer(false);
              }}
              disabled={isAnswered}
              className={`py-5 px-4 rounded-2xl border-2 font-black text-base transition-all flex flex-col items-center justify-center gap-1 ${
                isAnswered
                  ? currentQ.correctAnswer === false
                    ? 'bg-emerald-500 text-white border-emerald-500'
                    : selectedOption === false
                    ? 'bg-rose-500 text-white border-rose-500'
                    : 'bg-slate-100 text-slate-400'
                  : 'bg-white text-rose-700 border-rose-200 hover:bg-rose-50'
              }`}
            >
              <X className="w-6 h-6" />
              <span>{t.falseBtn}</span>
            </button>
          </div>
        )}

        {/* Type C — Word Building */}
        {currentQ.type === 'word_building' && (
          <div className="space-y-4">
            {/* Selected Letters Slots */}
            <div className="flex items-center justify-center gap-1.5 flex-wrap min-h-[52px] p-2 bg-slate-200/60 rounded-2xl border border-slate-300/60">
              {builtLetters.length === 0 ? (
                <span className="text-xs font-semibold text-slate-400">
                  {baseLanguage === 'ru' ? 'Нажимайте буквы ниже' : 'Apasă literele de mai jos'}
                </span>
              ) : (
                builtLetters.map((letter, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleRemoveLetter(idx)}
                    disabled={isAnswered}
                    className="w-10 h-10 rounded-xl bg-white text-blue-700 font-black text-lg shadow-xs border border-blue-200 hover:bg-rose-50 hover:text-rose-600 transition-all flex items-center justify-center animate-in scale-95 duration-100"
                  >
                    {letter}
                  </button>
                ))
              )}
            </div>

            {/* Letter Bank Buttons */}
            {currentQ.letterBank && (
              <div className="flex items-center justify-center gap-2 flex-wrap">
                {currentQ.letterBank.map((letter, idx) => {
                  const isUsed = selectedLetterIndices.includes(idx);
                  return (
                    <button
                      key={idx}
                      onClick={() => handleSelectLetter(letter, idx)}
                      disabled={isUsed || isAnswered}
                      className={`w-11 h-11 rounded-2xl font-black text-base transition-all shadow-2xs ${
                        isUsed
                          ? 'bg-slate-200 text-slate-400 border-transparent opacity-40 cursor-not-allowed'
                          : 'bg-white text-slate-900 border border-slate-200 hover:border-blue-400 hover:bg-blue-50 active:scale-95'
                      }`}
                    >
                      {letter}
                    </button>
                  );
                })}
              </div>
            )}

            {/* Action Bar for Word Building: Clear & Check */}
            {!isAnswered && (
              <div className="flex items-center gap-2 pt-2">
                <button
                  onClick={handleClearLetters}
                  disabled={builtLetters.length === 0}
                  className="px-4 py-3 rounded-2xl bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold text-xs transition-colors"
                >
                  {t.clearBtn}
                </button>

                <button
                  onClick={() => handleEvaluateAnswer(builtLetters.join(''))}
                  disabled={builtLetters.length === 0}
                  className={`flex-1 py-3.5 px-4 rounded-2xl font-bold text-sm transition-all shadow-sm ${
                    builtLetters.length > 0
                      ? 'bg-blue-600 hover:bg-blue-700 text-white'
                      : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                  }`}
                >
                  {t.checkBtn}
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Answer Feedback Bottom Sheet / Overlay */}
      {isAnswered && (
        <div
          className={`p-5 rounded-t-3xl border-t-2 animate-in slide-in-from-bottom duration-300 ${
            isCorrect
              ? 'bg-emerald-50 border-emerald-500 text-emerald-950'
              : 'bg-rose-50 border-rose-500 text-rose-950'
          }`}
        >
          <div className="flex items-start justify-between gap-3 mb-3">
            <div className="flex items-center gap-2">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white ${
                  isCorrect ? 'bg-emerald-500' : 'bg-rose-500'
                }`}
              >
                {isCorrect ? <Check className="w-5 h-5" /> : <X className="w-5 h-5" />}
              </div>
              <div>
                <h3 className="font-extrabold text-base leading-none">
                  {isCorrect ? t.correctHeader : t.incorrectHeader}
                </h3>
                <p className="text-xs font-semibold mt-1 opacity-90">
                  {currentQ.word.gagauz} —{' '}
                  {baseLanguage === 'ru' ? currentQ.word.ru : currentQ.word.ro}
                </p>
              </div>
            </div>

            <button
              onClick={speakCurrentWord}
              className="p-2 rounded-xl bg-white/80 hover:bg-white text-slate-800 transition-colors"
            >
              <Volume2 className="w-4 h-4" />
            </button>
          </div>

          {!isCorrect && (
            <div className="mb-4 p-2.5 bg-white/80 rounded-xl border border-rose-200 text-xs">
              <span className="font-bold text-rose-900 block">
                {t.correctAnswerIs}
              </span>
              <span className="font-bold text-slate-900">
                {currentQ.type === 'word_building'
                  ? currentQ.word.gagauz
                  : baseLanguage === 'ru'
                  ? currentQ.word.ru
                  : currentQ.word.ro}
              </span>
            </div>
          )}

          <button
            onClick={handleContinueNext}
            className={`w-full py-3.5 px-4 rounded-2xl font-bold text-sm text-white shadow-md transition-all ${
              isCorrect
                ? 'bg-emerald-600 hover:bg-emerald-700'
                : 'bg-rose-600 hover:bg-rose-700'
            }`}
          >
            {t.continueExerciseCTA}
          </button>
        </div>
      )}
    </div>
  );
};
