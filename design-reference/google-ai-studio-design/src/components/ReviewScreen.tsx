import React from 'react';
import { Sparkles, AlertCircle, Zap, Award, Play, Layers } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../data/translations';

export const ReviewScreen: React.FC = () => {
  const { baseLanguage, getTotalProgress, navigateTo } = useApp();
  const t = getTranslation(baseLanguage);
  const totalStats = getTotalProgress();

  const reviewActivities = [
    {
      id: 'daily',
      title: t.dailyReviewTitle,
      description: t.dailyReviewDesc,
      icon: Sparkles,
      iconBg: 'bg-amber-50 text-amber-600 border-amber-200/60',
      badge: `${totalStats.readyForReview} ${t.readyForReview}`,
      badgeBg: 'bg-amber-100 text-amber-800',
      cta: t.startSessionCTA,
      btnClass: 'bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white'
    },
    {
      id: 'difficult',
      title: t.difficultWordsReviewTitle,
      description: t.difficultWordsReviewDesc,
      icon: AlertCircle,
      iconBg: 'bg-rose-50 text-rose-600 border-rose-200/60',
      badge: `${totalStats.needAttention} ${t.needAttention}`,
      badgeBg: 'bg-rose-100 text-rose-800',
      cta: t.startSessionCTA,
      btnClass: 'bg-rose-600 hover:bg-rose-700 text-white'
    },
    {
      id: 'quick',
      title: t.quickReviewTitle,
      description: t.quickReviewDesc,
      icon: Zap,
      iconBg: 'bg-indigo-50 text-indigo-600 border-indigo-200/60',
      badge: baseLanguage === 'ru' ? '5 вопросов' : '5 întrebări',
      badgeBg: 'bg-indigo-100 text-indigo-800',
      cta: t.startSessionCTA,
      btnClass: 'bg-indigo-600 hover:bg-indigo-700 text-white'
    },
    {
      id: 'quiz',
      title: t.quizTitle,
      description: t.quizDesc,
      icon: Award,
      iconBg: 'bg-teal-50 text-teal-600 border-teal-200/60',
      badge: baseLanguage === 'ru' ? 'Экзамен' : 'Examen',
      badgeBg: 'bg-teal-100 text-teal-800',
      cta: t.startSessionCTA,
      btnClass: 'bg-teal-600 hover:bg-teal-700 text-white'
    }
  ];

  return (
    <div className="space-y-4 pb-20 pt-1">
      {/* Header */}
      <div>
        <h2 className="text-xl font-extrabold text-slate-900 tracking-tight">
          {t.reviewHubTitle}
        </h2>
        <p className="text-xs text-slate-500 font-medium">
          {t.reviewHubSubtitle}
        </p>
      </div>

      {/* Format Notice */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/60 rounded-2xl p-3.5 flex items-center gap-2.5 text-xs text-blue-900 font-medium">
        <Layers className="w-4 h-4 text-blue-600 shrink-0" />
        <span>{t.mixedExerciseNotice}</span>
      </div>

      {/* Review Activities List */}
      <div className="space-y-3">
        {reviewActivities.map((act) => {
          const Icon = act.icon;
          return (
            <div
              key={act.id}
              className="bg-white rounded-3xl p-5 border border-slate-100 shadow-2xs hover:shadow-sm transition-all"
            >
              <div className="flex items-start justify-between gap-3 mb-2">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-10 h-10 rounded-2xl flex items-center justify-center font-bold border ${act.iconBg}`}
                  >
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-extrabold text-slate-900 text-base leading-snug">
                      {act.title}
                    </h3>
                    <span
                      className={`inline-block text-[10px] font-bold px-2 py-0.5 rounded-full mt-0.5 ${act.badgeBg}`}
                    >
                      {act.badge}
                    </span>
                  </div>
                </div>
              </div>

              <p className="text-xs text-slate-500 font-medium mb-4 leading-relaxed">
                {act.description}
              </p>

              <button
                onClick={() =>
                  navigateTo({
                    type: 'exercise',
                    mode: act.id as any
                  })
                }
                className={`w-full py-3.5 px-4 rounded-2xl font-bold text-sm transition-all flex items-center justify-center gap-2 shadow-xs hover:shadow-md ${act.btnClass}`}
              >
                <Play className="w-4 h-4 fill-current" />
                <span>{act.cta}</span>
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};
