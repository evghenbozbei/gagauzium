import React, { useState } from 'react';
import { Settings, Globe, Languages, Info } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../data/translations';
import { SettingsModal } from './SettingsModal';

export const Header: React.FC = () => {
  const { baseLanguage, setBaseLanguage, activeScreen, navigateTab } = useApp();
  const t = getTranslation(baseLanguage);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // Hide top header if in Exercise screen (Exercise screen handles its own focused top header with back button)
  if (activeScreen.type === 'exercise') {
    return null;
  }

  return (
    <>
      <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-slate-100 shadow-xs px-4 py-3">
        <div className="max-w-md mx-auto flex items-center justify-between">
          {/* Logo Branding */}
          <button
            onClick={() => navigateTab('home')}
            className="flex items-center gap-2.5 text-left focus:outline-hidden group"
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-teal-500 p-0.5 shadow-sm group-hover:scale-105 transition-transform">
              <div className="w-full h-full bg-white rounded-[10px] flex items-center justify-center font-bold text-blue-600 text-lg">
                G
              </div>
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold text-lg text-slate-900 tracking-tight leading-none">
                  Gagauzium
                </span>
                <span className="bg-blue-50 text-blue-700 text-[10px] font-semibold px-1.5 py-0.5 rounded-full border border-blue-200/80">
                  Gagauz
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium leading-none mt-0.5">
                {baseLanguage === 'ru' ? 'Гагаузский язык' : 'Limba găgăuză'}
              </p>
            </div>
          </button>

          {/* Quick Base Language Switcher & Settings */}
          <div className="flex items-center gap-1.5">
            {/* Language Selector Pill */}
            <button
              onClick={() => setBaseLanguage(baseLanguage === 'ru' ? 'ro' : 'ru')}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-slate-100/80 hover:bg-slate-200/70 text-slate-700 text-xs font-semibold transition-colors border border-slate-200/50"
              title={t.selectBaseLang}
            >
              <Globe className="w-3.5 h-3.5 text-slate-500" />
              <span>{baseLanguage === 'ru' ? '🇷🇺 RU' : '🇷🇴 RO'}</span>
            </button>

            {/* Settings Trigger */}
            <button
              onClick={() => setIsSettingsOpen(true)}
              className="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-colors"
              aria-label="Settings"
            >
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Settings Modal */}
      {isSettingsOpen && <SettingsModal onClose={() => setIsSettingsOpen(false)} />}
    </>
  );
};
