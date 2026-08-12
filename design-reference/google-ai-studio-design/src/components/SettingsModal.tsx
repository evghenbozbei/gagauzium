import React from 'react';
import { X, Globe, Info, RotateCcw, Heart } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../data/translations';

interface SettingsModalProps {
  onClose: () => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({ onClose }) => {
  const { baseLanguage, setBaseLanguage, resetAllProgress } = useApp();
  const t = getTranslation(baseLanguage);

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-sm rounded-3xl p-5 shadow-2xl space-y-5">
        {/* Modal Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <h3 className="font-extrabold text-slate-900 text-lg">
            {t.settingsTitle}
          </h3>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Language Selection */}
        <div className="space-y-2">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-500 block">
            {t.appLanguage}
          </label>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => setBaseLanguage('ru')}
              className={`p-3 rounded-2xl border-2 font-bold text-xs transition-all flex items-center justify-center gap-2 ${
                baseLanguage === 'ru'
                  ? 'bg-blue-50 text-blue-700 border-blue-500'
                  : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
              }`}
            >
              <span className="text-base">🇷🇺</span>
              <span>{t.langRu}</span>
            </button>

            <button
              onClick={() => setBaseLanguage('ro')}
              className={`p-3 rounded-2xl border-2 font-bold text-xs transition-all flex items-center justify-center gap-2 ${
                baseLanguage === 'ro'
                  ? 'bg-blue-50 text-blue-700 border-blue-500'
                  : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
              }`}
            >
              <span className="text-base">🇷🇴</span>
              <span>{t.langRo}</span>
            </button>
          </div>
        </div>

        {/* About Gagauz Language */}
        <div className="bg-slate-50 rounded-2xl p-3.5 border border-slate-100 space-y-1.5">
          <div className="flex items-center gap-1.5 text-xs font-bold text-slate-900">
            <Info className="w-4 h-4 text-blue-600" />
            <span>{t.aboutGagauz}</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed font-medium">
            {t.aboutGagauzText}
          </p>
        </div>

        {/* Reset Progress */}
        <div className="pt-2 border-t border-slate-100">
          <button
            onClick={() => {
              if (window.confirm(t.resetConfirm)) {
                resetAllProgress();
                onClose();
              }
            }}
            className="w-full py-2.5 px-3 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 font-bold text-xs transition-colors flex items-center justify-center gap-2"
          >
            <RotateCcw className="w-4 h-4" />
            <span>{t.resetProgress}</span>
          </button>
        </div>

        {/* Close Button */}
        <button
          onClick={onClose}
          className="w-full py-3 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-2xl text-xs transition-colors"
        >
          {t.close}
        </button>
      </div>
    </div>
  );
};
