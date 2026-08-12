import { Category } from '../types';

export const CATEGORIES: Category[] = [
  {
    id: 'family',
    gagauzName: 'Ailä',
    nameRu: 'Семья',
    nameRo: 'Familie',
    descriptionRu: 'Члены семьи, родственники и отношения',
    descriptionRo: 'Membrii familiei, rudele și relațiile',
    iconName: 'Users',
    color: '#3B82F6', // Blue
    bgGradient: 'from-blue-500/10 to-indigo-500/10 border-blue-200/60',
    level: 'beginner'
  },
  {
    id: 'food',
    gagauzName: 'Yemeklär',
    nameRu: 'Еда и напитки',
    nameRo: 'Mâncare și băuturi',
    descriptionRu: 'Продукты питания, национальная кухня и напитки',
    descriptionRo: 'Produse alimentare, bucătăria tradițională și băuturi',
    iconName: 'UtensilsCrossed',
    color: '#F59E0B', // Amber
    bgGradient: 'from-amber-500/10 to-orange-500/10 border-amber-200/60',
    level: 'beginner'
  },
  {
    id: 'numbers',
    gagauzName: 'Sayılar',
    nameRu: 'Числа',
    nameRo: 'Numere',
    descriptionRu: 'Числа, цифры и базовый счёт',
    descriptionRo: 'Numere, cifre și numărarea de bază',
    iconName: 'Hash',
    color: '#10B981', // Emerald
    bgGradient: 'from-emerald-500/10 to-teal-500/10 border-emerald-200/60',
    level: 'beginner'
  },
  {
    id: 'time',
    gagauzName: 'Vakit',
    nameRu: 'Время и дни',
    nameRo: 'Timp și zile',
    descriptionRu: 'Дни недели, месяцы, время суток и часы',
    descriptionRo: 'Zilele săptămânii, lunile, momentele zilei și orele',
    iconName: 'Clock',
    color: '#8B5CF6', // Purple
    bgGradient: 'from-purple-500/10 to-violet-500/10 border-purple-200/60',
    level: 'beginner'
  },
  {
    id: 'animals',
    gagauzName: 'Hayvanlar',
    nameRu: 'Животные',
    nameRo: 'Animale',
    descriptionRu: 'Домашние и дикие животные, птицы',
    descriptionRo: 'Animale domestice și sălbatice, păsări',
    iconName: 'Dog',
    color: '#EC4899', // Pink
    bgGradient: 'from-pink-500/10 to-rose-500/10 border-pink-200/60',
    level: 'beginner'
  },
  {
    id: 'nature',
    gagauzName: 'Tebiât',
    nameRu: 'Природа',
    nameRo: 'Natură',
    descriptionRu: 'Погода, элементы природы, растения',
    descriptionRo: 'Vremea, elementele naturii, plantele',
    iconName: 'Sun',
    color: '#06B6D4', // Cyan
    bgGradient: 'from-cyan-500/10 to-sky-500/10 border-cyan-200/60',
    level: 'beginner'
  },
  {
    id: 'home',
    gagauzName: 'Ev',
    nameRu: 'Дом',
    nameRo: 'Casă',
    descriptionRu: 'Мебель, комнаты, бытовые предметы',
    descriptionRo: 'Mobilă, camere, obiecte de uz casnic',
    iconName: 'Home',
    color: '#6366F1', // Indigo
    bgGradient: 'from-indigo-500/10 to-blue-500/10 border-indigo-200/60',
    level: 'beginner'
  },
  {
    id: 'clothing',
    gagauzName: 'Giyim',
    nameRu: 'Одежда',
    nameRo: 'Îmbrăcăminte',
    descriptionRu: 'Элементы гардероба и аксессуары',
    descriptionRo: 'Articole de îmbrăcăminte și accesorii',
    iconName: 'Shirt',
    color: '#14B8A6', // Teal
    bgGradient: 'from-teal-500/10 to-emerald-500/10 border-teal-200/60',
    level: 'beginner'
  },
  {
    id: 'professions',
    gagauzName: 'Zanaatlar',
    nameRu: 'Профессии',
    nameRo: 'Profesii',
    descriptionRu: 'Специальности, работа и труд',
    descriptionRo: 'Specialități, muncă și profesii',
    iconName: 'Briefcase',
    color: '#F97316', // Orange
    bgGradient: 'from-orange-500/10 to-amber-500/10 border-orange-200/60',
    level: 'beginner'
  },
  {
    id: 'transport',
    gagauzName: 'Taşımak',
    nameRu: 'Транспорт',
    nameRo: 'Transport',
    descriptionRu: 'Средства передвижения и город',
    descriptionRo: 'Mijloace de transport și orașul',
    iconName: 'Bus',
    color: '#3B82F6', // Blue
    bgGradient: 'from-blue-500/10 to-cyan-500/10 border-blue-200/60',
    level: 'beginner'
  },
  {
    id: 'colors',
    gagauzName: 'Renkler',
    nameRu: 'Цвета',
    nameRo: 'Culori',
    descriptionRu: 'Основные и дополнительные цвета',
    descriptionRo: 'Culorile principale și secundare',
    iconName: 'Palette',
    color: '#A855F7', // Purple
    bgGradient: 'from-purple-500/10 to-pink-500/10 border-purple-200/60',
    level: 'beginner'
  },
  {
    id: 'actions',
    gagauzName: 'İşlär',
    nameRu: 'Действия',
    nameRo: 'Acțiuni',
    descriptionRu: 'Основные глаголы и ежедневные действия',
    descriptionRo: 'Verbe de bază și acțiuni zilnice',
    iconName: 'Zap',
    color: '#EAB308', // Yellow
    bgGradient: 'from-yellow-500/10 to-amber-500/10 border-yellow-200/60',
    level: 'beginner'
  },
  {
    id: 'places',
    gagauzName: 'Yerlär',
    nameRu: 'Места',
    nameRo: 'Locuri',
    descriptionRu: 'Локации, город, здания и заведения',
    descriptionRo: 'Locații, oraș, clădiri și instituții',
    iconName: 'MapPin',
    color: '#EF4444', // Red
    bgGradient: 'from-red-500/10 to-rose-500/10 border-red-200/60',
    level: 'beginner'
  },
  {
    id: 'anatomy',
    gagauzName: 'Gövde',
    nameRu: 'Анатомия',
    nameRo: 'Anatomie',
    descriptionRu: 'Части тела и здоровье',
    descriptionRo: 'Părțile corpului și sănătate',
    iconName: 'HeartPulse',
    color: '#84CC16', // Lime
    bgGradient: 'from-lime-500/10 to-emerald-500/10 border-lime-200/60',
    level: 'beginner'
  }
];
