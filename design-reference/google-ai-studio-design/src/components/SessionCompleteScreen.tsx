import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Award, CheckCircle2, Flame, ArrowRight, Home, RotateCcw } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../data/translations';

interface SessionCompleteScreenProps {
  stats: {
    total: number;
    correct: number;
    xp: number;
    newWordsLearned: number;
  };
}

export const SessionCompleteScreen: React.FC<SessionCompleteScreenProps> = ({ stats }) => {
  const { baseLanguage, navigateTo, streakDays } = useApp();
  const t = getTranslation(baseLanguage);

  const accuracy = Math.round((stats.correct / Math.max(1, stats.total)) * 100);

  useEffect(() => {
    // Fire celebratory confetti!
    try {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    } catch (e) {
      console.warn('Confetti error', e);
    }
  }, []);

  return (
    <div className="min-h-[85vh] flex flex-col justify-between py-6 px-4 max-w-md mx-auto">
      {/* Top Banner Celebration */}
      <div className="text-center pt-4 space-y-3">
        <div className="w-20 h-20 mx-auto rounded-3xl bg-gradient-to-tr from-amber-400 via-orange-500 to-yellow-300 p-0.5 shadow-lg flex items-center justify-center animate-bounce duration-1000">
          <div className="w-full h-full bg-white rounded-[22px] flex items-center justify-center">
            <Award className="w-10 h-10 text-amber-500" />
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            {t.sessionCompleteTitle}
          </h2>
          <p className="text-xs text-slate-500 font-medium mt-1">
            {t.sessionCompleteSubtitle}
          </p>
        </div>
      </div>

      {/* Stats Cards Grid */}
      <div className="grid grid-cols-2 gap-3 my-6">
        {/* Accuracy */}
        <div className="bg-white border border-slate-100 rounded-3xl p-4 text-center shadow-2xs">
          <span className="text-2xl font-extrabold text-blue-600 block">
            {accuracy}%
          </span>
          <span className="text-xs font-semibold text-slate-500 block mt-0.5">
            {t.accuracyLabel}
          </span>
        </div>

        {/* XP Earned */}
        <div className="bg-white border border-slate-100 rounded-3xl p-4 text-center shadow-2xs">
          <span className="text-2xl font-extrabold text-amber-500 block">
            +{stats.xp}
          </span>
          <span className="text-xs font-semibold text-slate-500 block mt-0.5">
            {t.xpEarned}
          </span>
        </div>

        {/* Mastered Words */}
        <div className="bg-white border border-slate-100 rounded-3xl p-4 text-center shadow-2xs">
          <span className="text-2xl font-extrabold text-emerald-600 block">
            {stats.correct} / {stats.total}
          </span>
          <span className="text-xs font-semibold text-slate-500 block mt-0.5">
            {t.wordsLearned}
          </span>
        </div>

        {/* Streak */}
        <div className="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200/80 rounded-3xl p-4 text-center shadow-2xs">
          <span className="text-2xl font-extrabold text-orange-600 block flex items-center justify-center gap-1">
            🔥 {streakDays}
          </span>
          <span className="text-xs font-semibold text-amber-800/80 block mt-0.5">
            {t.streakTitle}
          </span>
        </div>
      </div>

      {/* Actions */}
      <div className="space-y-2.5">
        <button
          onClick={() => navigateTo({ type: 'home' })}
          className="w-full py-4 px-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-2xl shadow-md transition-all flex items-center justify-center gap-2 text-sm"
        >
          <Home className="w-4 h-4" />
          <span>{t.finishCTA}</span>
        </button>

        <button
          onClick={() => navigateTo({ type: 'review' })}
          className="w-full py-3.5 px-4 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold rounded-2xl transition-all flex items-center justify-center gap-2 text-xs"
        >
          <RotateCcw className="w-4 h-4" />
          <span>{t.continueAnotherSessionCTA}</span>
        </button>
      </div>
    </div>
  );
};
