import React from 'react';
import { Play, Sparkles, ChevronRight, Flame, Layers, AlertCircle, ArrowRight } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../data/translations';
import { CATEGORIES } from '../data/categories';
import { CategoryIllustration } from './CategoryIcon';

export const HomeScreen: React.FC = () => {
  const {
    baseLanguage,
    lastCategoryId,
    streakDays,
    getTotalProgress,
    getCategoryStats,
    navigateTo
  } = useApp();

  const t = getTranslation(baseLanguage);
  const totalProgress = getTotalProgress();

  const lastCategory = CATEGORIES.find((c) => c.id === lastCategoryId) || CATEGORIES[0];
  const lastCategoryStats = getCategoryStats(lastCategory.id);
  const lastCategoryGagauzName = lastCategory.gagauzName;
  const lastCategoryLocalName = baseLanguage === 'ru' ? lastCategory.nameRu : lastCategory.nameRo;

  return (
    <div className="space-y-4 pb-20 pt-1">
      {/* 1. Progress Card */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950 text-white rounded-3xl p-5 shadow-md relative overflow-hidden">
        {/* Subtle decorative background blur shapes */}
        <div className="absolute -right-8 -top-8 w-32 h-32 bg-blue-500/20 rounded-full blur-xl pointer-events-none" />
        <div className="absolute -left-8 -bottom-8 w-32 h-32 bg-teal-500/15 rounded-full blur-xl pointer-events-none" />

        <div className="relative z-10">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-blue-300/90">
              {t.yourProgress}
            </span>
            <span className="text-xs font-bold bg-white/10 text-white px-2.5 py-0.5 rounded-full backdrop-blur-xs">
              {totalProgress.percentage}%
            </span>
          </div>

          <div className="flex items-baseline gap-2 mb-3">
            <span className="text-3xl sm:text-4xl font-extrabold tracking-tight">
              {totalProgress.learned}
            </span>
            <span className="text-sm font-medium text-slate-300">
              / {totalProgress.total} {t.wordsCount}
            </span>
          </div>

          {/* Progress bar */}
          <div className="w-full bg-slate-700/60 rounded-full h-3 p-0.5 mb-3">
            <div
              className="bg-gradient-to-r from-blue-400 via-indigo-400 to-teal-300 h-2 rounded-full transition-all duration-500 shadow-xs"
              style={{ width: `${Math.max(5, totalProgress.percentage)}%` }}
            />
          </div>

          <div className="flex items-center justify-between text-xs text-slate-300">
            <span>750 {t.wordsOfTotal}</span>
            <span className="text-teal-300 font-medium">
              Level 1: {t.levelBeginner}
            </span>
          </div>
        </div>
      </div>

      {/* 2. Daily Review Card */}
      <div className="bg-white rounded-3xl p-5 border border-slate-100 shadow-xs relative">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-base leading-none">
                {t.today}
              </h3>
              <p className="text-xs text-slate-500 mt-0.5 font-medium">
                {t.dailyReviewTitle}
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 mb-4">
          <div className="bg-amber-50/70 border border-amber-100 rounded-2xl p-3">
            <span className="block text-xl font-extrabold text-amber-900">
              {totalProgress.readyForReview}
            </span>
            <span className="text-xs font-medium text-amber-700/90 leading-tight block">
              {t.readyForReview}
            </span>
          </div>
          <div className="bg-rose-50/70 border border-rose-100 rounded-2xl p-3">
            <span className="block text-xl font-extrabold text-rose-900 flex items-center gap-1">
              {totalProgress.needAttention}
              <AlertCircle className="w-3.5 h-3.5 text-rose-500 inline" />
            </span>
            <span className="text-xs font-medium text-rose-700/90 leading-tight block">
              {t.needAttention}
            </span>
          </div>
        </div>

        <button
          onClick={() =>
            navigateTo({
              type: 'exercise',
              mode: 'daily'
            })
          }
          className="w-full py-3.5 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold rounded-2xl shadow-sm hover:shadow-md transition-all flex items-center justify-center gap-2 text-sm"
        >
          <Play className="w-4 h-4 fill-current" />
          <span>{t.startDailyReview}</span>
        </button>
      </div>

      {/* 3. Continue Learning Card */}
      <div className="bg-white rounded-3xl p-5 border border-slate-100 shadow-xs">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
            {t.continueLearning}
          </span>
          <button
            onClick={() => navigateTo({ type: 'learn' })}
            className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-0.5"
          >
            {t.chooseCategory}
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="flex items-center gap-4 mb-3">
          <CategoryIllustration categoryId={lastCategory.id} size="md" />
          <div className="flex-1 min-w-0">
            <h4 className="font-extrabold text-slate-900 text-lg leading-snug truncate">
              {lastCategoryLocalName}
            </h4>
            <p className="text-xs font-semibold text-blue-600">
              {lastCategoryGagauzName}
            </p>
            <p className="text-xs text-slate-500 mt-1 font-medium">
              {lastCategoryStats.learned} / {lastCategoryStats.total} {t.wordsCount}
            </p>
          </div>
        </div>

        {/* Progress bar */}
        <div className="w-full bg-slate-100 rounded-full h-2.5 mb-4">
          <div
            className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
            style={{
              width: `${Math.round(
                (lastCategoryStats.learned / Math.max(1, lastCategoryStats.total)) * 100
              )}%`
            }}
          />
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() =>
              navigateTo({
                type: 'category_detail',
                categoryId: lastCategory.id
              })
            }
            className="flex-1 py-3 px-4 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-2xl transition-colors flex items-center justify-center gap-2 text-sm"
          >
            <span>{t.continueCTA}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 4. Streak Secondary Card */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200/80 rounded-2xl p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-orange-500 text-white flex items-center justify-center shadow-xs text-xl">
            🔥
          </div>
          <div>
            <div className="font-extrabold text-amber-950 text-sm">
              {streakDays} {t.streakTitle}
            </div>
            <p className="text-xs text-amber-800/80 font-medium">
              {t.streakSubtitle}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
