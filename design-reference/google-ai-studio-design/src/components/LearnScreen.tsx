import React from 'react';
import { Lock, Sparkles, CheckCircle2 } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { CATEGORIES } from '../data/categories';
import { getTranslation } from '../data/translations';
import { CategoryIllustration } from './CategoryIcon';
import { CategoryLevel } from '../types';

export const LearnScreen: React.FC = () => {
  const { baseLanguage, getCategoryStats, navigateTo, selectedLevel, setSelectedLevel } = useApp();
  const t = getTranslation(baseLanguage);

  const levels: { id: CategoryLevel; label: string; active: boolean }[] = [
    { id: 'beginner', label: t.levelBeginner, active: true },
    { id: 'conversational', label: t.levelConversational, active: false },
    { id: 'advanced', label: t.levelAdvanced, active: false },
    { id: 'expert', label: t.levelExpert, active: false }
  ];

  return (
    <div className="space-y-4 pb-20 pt-1">
      {/* Header Title */}
      <div>
        <h2 className="text-xl font-extrabold text-slate-900 tracking-tight">
          {t.learnTitle}
        </h2>
        <p className="text-xs text-slate-500 font-medium">
          {t.learnSubtitle}
        </p>
      </div>

      {/* Progression Levels Tabs (Beginner active, others visually indicated as locked) */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
        {levels.map((lvl) => {
          const isSelected = selectedLevel === lvl.id && lvl.active;
          return (
            <button
              key={lvl.id}
              onClick={() => {
                if (lvl.active) setSelectedLevel(lvl.id);
              }}
              disabled={!lvl.active}
              className={`shrink-0 px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                isSelected
                  ? 'bg-blue-600 text-white shadow-xs'
                  : lvl.active
                  ? 'bg-white text-slate-700 border border-slate-200/80 hover:bg-slate-50'
                  : 'bg-slate-100 text-slate-400 opacity-75 cursor-not-allowed'
              }`}
            >
              <span>{lvl.label}</span>
              {!lvl.active && <Lock className="w-3 h-3 text-slate-400" />}
            </button>
          );
        })}
      </div>

      {/* Category Cards Grid — 2 cards per row */}
      <div className="grid grid-cols-2 gap-3">
        {CATEGORIES.map((cat) => {
          const stats = getCategoryStats(cat.id);
          const percent = Math.round((stats.learned / Math.max(1, stats.total)) * 100);
          const catName = baseLanguage === 'ru' ? cat.nameRu : cat.nameRo;

          return (
            <button
              key={cat.id}
              onClick={() =>
                navigateTo({
                  type: 'category_detail',
                  categoryId: cat.id
                })
              }
              className="bg-white hover:bg-slate-50/80 border border-slate-100 rounded-2xl p-3.5 text-left transition-all duration-200 shadow-2xs hover:shadow-sm hover:-translate-y-0.5 flex flex-col justify-between group relative overflow-hidden"
            >
              {/* Top Row: Illustration & Percent badge */}
              <div className="flex items-start justify-between gap-1 mb-2">
                <CategoryIllustration categoryId={cat.id} size="sm" />
                {percent > 0 && (
                  <span className="text-[10px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded-full border border-blue-100">
                    {percent}%
                  </span>
                )}
              </div>

              {/* Title & Gagauz Subtitle */}
              <div className="mb-2">
                <h3 className="font-extrabold text-slate-900 text-sm leading-tight group-hover:text-blue-600 transition-colors line-clamp-1">
                  {catName}
                </h3>
                <p className="text-[11px] font-semibold text-blue-600/90 leading-none mt-0.5">
                  {cat.gagauzName}
                </p>
              </div>

              {/* Stats & Progress bar */}
              <div className="mt-auto pt-1">
                <div className="flex items-center justify-between text-[11px] text-slate-500 font-medium mb-1">
                  <span>
                    {stats.learned} / {stats.total}
                  </span>
                  {stats.learned === stats.total && (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 inline" />
                  )}
                </div>
                <div className="w-full bg-slate-100 rounded-full h-1.5">
                  <div
                    className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
                    style={{ width: `${percent}%` }}
                  />
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
