import React from 'react';
import { Home, BookOpen, Repeat } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { NavTab } from '../types';
import { getTranslation } from '../data/translations';

export const BottomNav: React.FC = () => {
  const { activeScreen, navigateTab, baseLanguage } = useApp();
  const t = getTranslation(baseLanguage);

  // Hide bottom nav in exercise or session complete screen so user stays 100% focused!
  if (activeScreen.type === 'exercise' || activeScreen.type === 'session_complete') {
    return null;
  }

  const getCurrentTab = (): NavTab => {
    if (activeScreen.type === 'learn' || activeScreen.type === 'category_detail' || activeScreen.type === 'learned_words') {
      return 'learn';
    }
    if (activeScreen.type === 'review') {
      return 'review';
    }
    return 'home';
  };

  const currentTab = getCurrentTab();

  const navItems: { tab: NavTab; label: string; icon: React.FC<{ className?: string }> }[] = [
    { tab: 'home', label: t.navHome, icon: Home },
    { tab: 'learn', label: t.navLearn, icon: BookOpen },
    { tab: 'review', label: t.navReview, icon: Repeat }
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-30 bg-white/95 backdrop-blur-md border-t border-slate-200/80 pb-safe shadow-lg">
      <div className="max-w-md mx-auto grid grid-cols-3 px-3 py-1.5">
        {navItems.map(({ tab, label, icon: Icon }) => {
          const isActive = currentTab === tab;
          return (
            <button
              key={tab}
              onClick={() => navigateTab(tab)}
              className={`flex flex-col items-center justify-center py-1 px-2 rounded-2xl transition-all duration-200 ${
                isActive
                  ? 'text-blue-600 font-bold scale-102'
                  : 'text-slate-500 hover:text-slate-700 font-medium'
              }`}
            >
              <div
                className={`p-1.5 rounded-xl transition-colors ${
                  isActive ? 'bg-blue-50 text-blue-600' : 'bg-transparent'
                }`}
              >
                <Icon className="w-5 h-5" />
              </div>
              <span className="text-[11px] mt-0.5 tracking-tight">{label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
