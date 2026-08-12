import { BaseLanguage } from '../types';

export const UI_TRANSLATIONS = {
  ru: {
    appName: 'Gagauzium',
    appSubtitle: 'Изучение гагаузского языка',
    // Bottom Nav
    navHome: 'Главная',
    navLearn: 'Обучение',
    navReview: 'Повторение',

    // Language Selector
    langRu: 'Русский',
    langRo: 'Română',
    selectBaseLang: 'Язык перевода',

    // Home Screen
    yourProgress: 'Ваш прогресс',
    wordsCount: 'слов выучено',
    wordsOfTotal: 'из 750 слов',
    today: 'Сегодня',
    readyForReview: 'слов к повторению',
    needAttention: 'требуют внимания',
    startDailyReview: 'Начать повторение',
    continueLearning: 'Продолжить обучение',
    continueCTA: 'Продолжить',
    streakTitle: 'дней подряд',
    streakSubtitle: 'Отличный ритм! Заходите каждый день.',
    chooseCategory: 'Выбрать другую категорию',

    // Learn Screen
    learnTitle: 'Категории',
    learnSubtitle: 'Выберите тему для изучения слов',
    levelBeginner: 'Начинающий',
    levelConversational: 'Разговорный',
    levelAdvanced: 'Продвинутый',
    levelExpert: 'Эксперт',
    levelLocked: 'Скоро будет доступно',

    // Category Detail
    wordsLearned: 'слов выучено',
    learnNewWords: 'Учить новые слова',
    wordsRemaining: 'слов осталось',
    startLearningCTA: 'Начать изучение',
    difficultWordsTitle: 'Трудные слова',
    difficultWordsDesc: 'слов требуют дополнительного внимания',
    reviewDifficultCTA: 'Повторить трудные',
    learnedWordsTitle: 'Выученные слова',
    learnedWordsDesc: 'просмотреть словарь темы',
    viewWordsCTA: 'Посмотреть слова',
    searchWordsPlaceholder: 'Поиск слова...',
    pronunciation: 'Произношение',
    example: 'Пример',

    // Review Screen
    reviewHubTitle: 'Тренировки',
    reviewHubSubtitle: 'Интерактивное закрепление изученных слов',
    dailyReviewTitle: 'Ежедневное повторение',
    dailyReviewDesc: 'Персональная подборка слов на основе вашей истории',
    difficultWordsReviewTitle: 'Трудные слова',
    difficultWordsReviewDesc: 'Слова, в которых вы чаще всего ошибаетесь',
    quickReviewTitle: 'Экспресс-тренинг',
    quickReviewDesc: 'Быстрая сессия из 5 вопросов для поддержания формы',
    quizTitle: 'Викторина',
    quizDesc: 'Тестовый экзамен с перемешанным форматом упражнений',
    startSessionCTA: 'Начать сессию',
    mixedExerciseNotice: '⚡ Включает варианты: выбор ответа, Правда/Ложь и составление слова.',

    // Exercise Screen
    backCTA: 'Назад',
    chooseCorrectTranslation: 'Выберите правильный перевод',
    whatDoesItMean: 'Что означает это слово?',
    isThisCorrect: 'Это утверждение верно?',
    buildGagauzWord: 'Соберите гагаузское слово:',
    trueBtn: 'Правда',
    falseBtn: 'Ложь',
    checkBtn: 'Проверить',
    clearBtn: 'Стереть',

    // Answer Feedback
    correctHeader: '✓ Правильно!',
    incorrectHeader: '✕ Не совсем',
    correctAnswerIs: 'Правильный ответ:',
    continueExerciseCTA: 'Продолжить',

    // Session Complete
    sessionCompleteTitle: 'Отличная работа!',
    sessionCompleteSubtitle: 'Сессия повторения успешно завершена',
    accuracyLabel: 'Точность',
    xpEarned: 'Очков опыта',
    newWordsMastered: 'Новых слов',
    finishCTA: 'На главную',
    continueAnotherSessionCTA: 'Продолжить еще',

    // Settings
    settingsTitle: 'Настройки',
    appLanguage: 'Язык интерфейса и перевода',
    aboutGagauz: 'О гагаузском языке',
    aboutGagauzText: 'Гагаузский язык — тюркский язык, родной для гагаузов. Официальный язык АО Гагаузия в составе Республики Молдова.',
    resetProgress: 'Сбросить прогресс',
    resetConfirm: 'Вы уверены, что хотите сбросить весь прогресс изучения?',
    close: 'Закрыть'
  },
  ro: {
    appName: 'Gagauzium',
    appSubtitle: 'Învățarea limbii găgăuze',
    // Bottom Nav
    navHome: 'Acasă',
    navLearn: 'Categorii',
    navReview: 'Exerciții',

    // Language Selector
    langRu: 'Русский',
    langRo: 'Română',
    selectBaseLang: 'Limba de traducere',

    // Home Screen
    yourProgress: 'Progresul tău',
    wordsCount: 'cuvinte învățate',
    wordsOfTotal: 'din 750 cuvinte',
    today: 'Astăzi',
    readyForReview: 'cuvinte gata de revizuire',
    needAttention: 'necesită atenție sporită',
    startDailyReview: 'Începe revizuirea',
    continueLearning: 'Continuă învățarea',
    continueCTA: 'Continuă',
    streakTitle: 'zile consecutive',
    streakSubtitle: 'Ritm excelent! Intră în fiecare zi.',
    chooseCategory: 'Alege altă categorie',

    // Learn Screen
    learnTitle: 'Categorii',
    learnSubtitle: 'Alege o temă pentru a învăța cuvinte',
    levelBeginner: 'Începător',
    levelConversational: 'Conversațional',
    levelAdvanced: 'Avansat',
    levelExpert: 'Expert',
    levelLocked: 'În curând',

    // Category Detail
    wordsLearned: 'cuvinte învățate',
    learnNewWords: 'Învață cuvinte noi',
    wordsRemaining: 'cuvinte rămase',
    startLearningCTA: 'Începe învățarea',
    difficultWordsTitle: 'Cuvinte dificile',
    difficultWordsDesc: 'cuvinte necesită atenție suplimentară',
    reviewDifficultCTA: 'Revizuiește cuvintele',
    learnedWordsTitle: 'Cuvinte învățate',
    learnedWordsDesc: 'vezi vocabularul acestei teme',
    viewWordsCTA: 'Vezi cuvintele',
    searchWordsPlaceholder: 'Caută un cuvânt...',
    pronunciation: 'Pronunție',
    example: 'Exemplu',

    // Review Screen
    reviewHubTitle: 'Exerciții',
    reviewHubSubtitle: 'Fixarea interactivă a cuvintelor învățate',
    dailyReviewTitle: 'Revizuire zilnică',
    dailyReviewDesc: 'Selecție personalizată pe baza istoricului tău',
    difficultWordsReviewTitle: 'Cuvinte dificile',
    difficultWordsReviewDesc: 'Cuvintele la care greșești cel mai des',
    quickReviewTitle: 'Revizuire rapidă',
    quickReviewDesc: 'Sesiune scurtă de 5 întrebări pentru exersare',
    quizTitle: 'Test grilă',
    quizDesc: 'Examen de evaluare cu formate mixte de exerciții',
    startSessionCTA: 'Începe sesiunea',
    mixedExerciseNotice: '⚡ Include formate: alegere multiplă, Adevărat/Fals și construirea cuvântului.',

    // Exercise Screen
    backCTA: 'Înapoi',
    chooseCorrectTranslation: 'Alege traducerea corectă',
    whatDoesItMean: 'Ce înseamnă acest cuvânt?',
    isThisCorrect: 'Este această afirmație corectă?',
    buildGagauzWord: 'Construiește cuvântul în găgăuză:',
    trueBtn: 'Adevărat',
    falseBtn: 'Fals',
    checkBtn: 'Verifică',
    clearBtn: 'Șterge',

    // Answer Feedback
    correctHeader: '✓ Corect!',
    incorrectHeader: '✕ Nu chiar',
    correctAnswerIs: 'Răspunsul corect:',
    continueExerciseCTA: 'Continuă',

    // Session Complete
    sessionCompleteTitle: 'Excelentă muncă!',
    sessionCompleteSubtitle: 'Sesiunea de exersare a fost finalizată cu succes',
    accuracyLabel: 'Acuratețe',
    xpEarned: 'Puncte XP',
    newWordsMastered: 'Cuvinte noi',
    finishCTA: 'Spre casă',
    continueAnotherSessionCTA: 'Continuă altă sesiune',

    // Settings
    settingsTitle: 'Setări',
    appLanguage: 'Limba interfeței și traducerii',
    aboutGagauz: 'Despre limba găgăuză',
    aboutGagauzText: 'Limba găgăuză este o limbă turcică vorbită de găgăuzi. Este limbă oficială în Unitatea Teritorială Autonomă Găgăuzia din Republica Moldova.',
    resetProgress: 'Resetează progresul',
    resetConfirm: 'Ești sigur că vrei să resetezi tot progresul de învățare?',
    close: 'Închide'
  }
};

export function getTranslation(lang: BaseLanguage) {
  return UI_TRANSLATIONS[lang] || UI_TRANSLATIONS.ru;
}
