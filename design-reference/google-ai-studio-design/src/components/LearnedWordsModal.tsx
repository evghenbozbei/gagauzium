import React, { useState } from 'react';
import { Search, X, Volume2, CheckCircle2, AlertCircle } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { getTranslation } from '../data/translations';
import { CATEGORIES } from '../data/categories';

interface LearnedWordsModalProps {
  categoryId: string;
  onClose: () => void;
}

export const LearnedWordsModal: React.FC<LearnedWordsModalProps> = ({ categoryId, onClose }) => {
  const { baseLanguage, getWordsByCategoryId, userWords } = useApp();
  const t = getTranslation(baseLanguage);
  const [searchQuery, setSearchQuery] = useState('');
  const [playingId, setPlayingId] = useState<string | null>(null);

  const category = CATEGORIES.find((c) => c.id === categoryId) || CATEGORIES[0];
  const catName = baseLanguage === 'ru' ? category.nameRu : category.nameRo;
  const words = getWordsByCategoryId(categoryId);

  const filteredWords = words.filter((w) => {
    const query = searchQuery.toLowerCase().trim();
    if (!query) return true;
    const trans = baseLanguage === 'ru' ? w.ru : w.ro;
    return (
      w.gagauz.toLowerCase().includes(query) ||
      trans.toLowerCase().includes(query) ||
      w.pronunciation.toLowerCase().includes(query)
    );
  });

  const speakWord = (word: typeof words[0]) => {
    setPlayingId(word.id);
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(word.gagauz);
      utterance.lang = 'tr-TR'; // Turkish accent is phonetically closest to Gagauz for browser TTS
      utterance.rate = 0.85;
      utterance.onend = () => setPlayingId(null);
      utterance.onerror = () => setPlayingId(null);
      window.speechSynthesis.speak(utterance);
    } else {
      setTimeout(() => setPlayingId(null), 1000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-end sm:items-center justify-center p-0 sm:p-4 animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-md h-[85vh] sm:h-[80vh] rounded-t-3xl sm:rounded-3xl flex flex-col overflow-hidden shadow-2xl">
        {/* Modal Header */}
        <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <div>
            <h3 className="font-extrabold text-slate-900 text-lg leading-tight">
              {catName} — {t.learnedWordsTitle}
            </h3>
            <p className="text-xs text-slate-500 font-medium">
              {words.length} {t.wordsOfTotal}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-200/50 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search Bar */}
        <div className="p-3 border-b border-slate-100 bg-white">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={t.searchWordsPlaceholder}
              className="w-full bg-slate-100/80 rounded-2xl pl-10 pr-4 py-2 text-xs font-medium text-slate-900 placeholder-slate-400 focus:outline-hidden focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Words List */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
          {filteredWords.map((w) => {
            const status = userWords[w.id]?.status || 'unlearned';
            const translation = baseLanguage === 'ru' ? w.ru : w.ro;
            const exampleGagauz = w.exampleGagauz;
            const exampleTrans = baseLanguage === 'ru' ? w.exampleRu : w.exampleRo;

            return (
              <div
                key={w.id}
                className="bg-slate-50/80 border border-slate-100 rounded-2xl p-3.5 flex items-start justify-between gap-3"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-extrabold text-slate-900 text-base">
                      {w.gagauz}
                    </span>
                    <span className="text-[11px] font-semibold text-slate-400">
                      {w.pronunciation}
                    </span>
                    {status === 'learned' && (
                      <span className="inline-flex items-center gap-0.5 text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200/60 ml-auto">
                        <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                      </span>
                    )}
                    {status === 'difficult' && (
                      <span className="inline-flex items-center gap-0.5 text-[10px] font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded-full border border-rose-200/60 ml-auto">
                        <AlertCircle className="w-3 h-3 text-rose-500" />
                      </span>
                    )}
                  </div>

                  <p className="text-xs font-semibold text-slate-700">
                    {translation}
                  </p>

                  {exampleGagauz && (
                    <div className="mt-2 text-[11px] bg-white p-2 rounded-xl border border-slate-200/60">
                      <p className="font-semibold text-blue-900">{exampleGagauz}</p>
                      <p className="text-slate-500 mt-0.5">{exampleTrans}</p>
                    </div>
                  )}
                </div>

                <button
                  onClick={() => speakWord(w)}
                  className={`p-2.5 rounded-xl border transition-all ${
                    playingId === w.id
                      ? 'bg-blue-600 text-white border-blue-600 scale-95'
                      : 'bg-white text-blue-600 border-slate-200 hover:bg-blue-50'
                  }`}
                  title={t.pronunciation}
                >
                  <Volume2 className="w-4 h-4" />
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
