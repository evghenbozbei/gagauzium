import React, { useState } from 'react';
import { ArrowLeft, Play, AlertCircle, BookOpen, Sparkles, CheckCircle2 } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { CATEGORIES } from '../data/categories';
import { getTranslation } from '../data/translations';
import { CategoryIllustration } from './CategoryIcon';
import { LearnedWordsModal } from './LearnedWordsModal';

interface CategoryDetailScreenProps {
  categoryId: string;
}

export const CategoryDetailScreen: React.FC<CategoryDetailScreenProps> = ({ categoryId }) => {
  const { baseLanguage, getCategoryStats, navigateTo } = useApp();
  const t = getTranslation(baseLanguage);
  const [isDictionaryOpen, setIsDictionaryOpen] = useState(false);

  const category = CATEGORIES.find((c) => c.id === categoryId) || CATEGORIES[0];
  const stats = getCategoryStats(category.id);
  const catName = baseLanguage === 'ru' ? category.nameRu : category.nameRo;
  const catDesc = baseLanguage === 'ru' ? category.descriptionRu : category.descriptionRo;
  const percent = Math.round((stats.learned / Math.max(1, stats.total)) * 100);

  return (
    <div className="space-y-4 pb-20 pt-1">
      {/* Top Back Navigation Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigateTo({ type: 'learn' })}
          className="flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-slate-900 bg-white px-3 py-2 rounded-xl border border-slate-200/80 shadow-2xs hover:bg-slate-50 transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{t.backCTA}</span>
        </button>

        <span className="text-xs font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-100">
          {category.gagauzName}
        </span>
      </div>

      {/* Category Hero Banner */}
      <div className="bg-gradient-to-br from-white via-slate-50/50 to-blue-50/30 rounded-3xl p-5 border border-slate-100 shadow-xs relative overflow-hidden">
        <div className="flex items-center gap-4">
          <CategoryIllustration categoryId={category.id} size="lg" />
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight leading-tight">
              {catName}
            </h2>
            <p className="text-xs font-bold text-blue-600 mt-0.5">
              {category.gagauzName}
            </p>
            <p className="text-xs text-slate-500 mt-1 font-medium leading-relaxed">
              {catDesc}
            </p>
          </div>
        </div>

        {/* Progress Overview Bar */}
        <div className="mt-4 pt-4 border-t border-slate-100">
          <div className="flex items-center justify-between text-xs font-bold mb-1.5">
            <span className="text-slate-700">
              {stats.learned} / {stats.total} {t.wordsLearned}
            </span>
            <span className="text-blue-600">{percent}%</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-2.5 p-0.5">
            <div
              className="bg-gradient-to-r from-blue-600 to-indigo-600 h-1.5 rounded-full transition-all duration-300"
              style={{ width: `${percent}%` }}
            />
          </div>
        </div>
      </div>

      {/* 3 Main Action Cards */}
      <div className="space-y-3">
        {/* Action 1: Learn New Words */}
        <div className="bg-white rounded-3xl p-5 border border-slate-100 shadow-2xs hover:shadow-sm transition-all relative overflow-hidden group">
          <div className="flex items-start justify-between gap-3 mb-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-extrabold text-slate-900 text-base leading-snug">
                  {t.learnNewWords}
                </h3>
                <p className="text-xs text-slate-500 font-medium">
                  {stats.unlearned} {t.wordsRemaining}
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={() =>
              navigateTo({
                type: 'exercise',
                mode: 'category_new',
                categoryId: category.id
              })
            }
            disabled={stats.unlearned === 0}
            className={`w-full py-3.5 px-4 rounded-2xl font-bold text-sm transition-all flex items-center justify-center gap-2 ${
              stats.unlearned > 0
                ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-xs'
                : 'bg-slate-100 text-slate-400 cursor-not-allowed'
            }`}
          >
            <Play className="w-4 h-4 fill-current" />
            <span>{stats.unlearned > 0 ? t.startLearningCTA : t.wordsLearned}</span>
          </button>
        </div>

        {/* Action 2: Difficult Words */}
        <div className="bg-white rounded-3xl p-5 border border-slate-100 shadow-2xs hover:shadow-sm transition-all relative overflow-hidden group">
          <div className="flex items-start justify-between gap-3 mb-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center font-bold">
                <AlertCircle className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-extrabold text-slate-900 text-base leading-snug">
                  {t.difficultWordsTitle}
                </h3>
                <p className="text-xs text-slate-500 font-medium">
                  {stats.difficult > 0
                    ? `${stats.difficult} ${t.difficultWordsDesc}`
                    : baseLanguage === 'ru'
                    ? 'Нет слов, требующих внимания!'
                    : 'Nu există cuvinte dificile!'}
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={() =>
              navigateTo({
                type: 'exercise',
                mode: 'category_difficult',
                categoryId: category.id
              })
            }
            disabled={stats.difficult === 0}
            className={`w-full py-3.5 px-4 rounded-2xl font-bold text-sm transition-all flex items-center justify-center gap-2 ${
              stats.difficult > 0
                ? 'bg-rose-600 hover:bg-rose-700 text-white shadow-xs'
                : 'bg-slate-100 text-slate-400 cursor-not-allowed'
            }`}
          >
            <AlertCircle className="w-4 h-4" />
            <span>
              {stats.difficult > 0
                ? t.reviewDifficultCTA
                : baseLanguage === 'ru'
                ? 'Всё изучено без ошибок'
                : 'Toate învățate cu succes'}
            </span>
          </button>
        </div>

        {/* Action 3: Learned Words */}
        <div className="bg-white rounded-3xl p-5 border border-slate-100 shadow-2xs hover:shadow-sm transition-all relative overflow-hidden group">
          <div className="flex items-start justify-between gap-3 mb-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
                <BookOpen className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-extrabold text-slate-900 text-base leading-snug">
                  {t.learnedWordsTitle}
                </h3>
                <p className="text-xs text-slate-500 font-medium">
                  {stats.learned} {t.wordsLearned}
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={() => setIsDictionaryOpen(true)}
            className="w-full py-3.5 px-4 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-2xl text-sm transition-all flex items-center justify-center gap-2"
          >
            <BookOpen className="w-4 h-4" />
            <span>{t.viewWordsCTA}</span>
          </button>
        </div>
      </div>

      {/* Dictionary Modal */}
      {isDictionaryOpen && (
        <LearnedWordsModal
          categoryId={category.id}
          onClose={() => setIsDictionaryOpen(false)}
        />
      )}
    </div>
  );
};
