import React from 'react';
import { AppProvider, useApp } from './context/AppContext';
import { Header } from './components/Header';
import { BottomNav } from './components/BottomNav';
import { HomeScreen } from './components/HomeScreen';
import { LearnScreen } from './components/LearnScreen';
import { CategoryDetailScreen } from './components/CategoryDetailScreen';
import { ReviewScreen } from './components/ReviewScreen';
import { ExerciseScreen } from './components/ExerciseScreen';
import { SessionCompleteScreen } from './components/SessionCompleteScreen';

const MainContainer: React.FC = () => {
  const { activeScreen } = useApp();

  const renderScreen = () => {
    switch (activeScreen.type) {
      case 'home':
        return <HomeScreen />;
      case 'learn':
        return <LearnScreen />;
      case 'category_detail':
        return <CategoryDetailScreen categoryId={activeScreen.categoryId} />;
      case 'review':
        return <ReviewScreen />;
      case 'exercise':
        return (
          <ExerciseScreen
            mode={activeScreen.mode}
            categoryId={activeScreen.categoryId}
          />
        );
      case 'session_complete':
        return <SessionCompleteScreen stats={activeScreen.stats} />;
      default:
        return <HomeScreen />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900 font-sans antialiased selection:bg-blue-500 selection:text-white">
      {/* Mobile Device Frame Wrapper */}
      <div className="max-w-md mx-auto min-h-screen bg-slate-50 flex flex-col shadow-xl border-x border-slate-200/60 relative">
        <Header />
        <main className="flex-1 px-4 py-3">
          {renderScreen()}
        </main>
        <BottomNav />
      </div>
    </div>
  );
};

export default function App() {
  return (
    <AppProvider>
      <MainContainer />
    </AppProvider>
  );
}
