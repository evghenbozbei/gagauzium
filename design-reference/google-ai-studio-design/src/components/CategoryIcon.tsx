import React from 'react';
import {
  Users,
  UtensilsCrossed,
  Hash,
  Clock,
  Dog,
  Sun,
  Home,
  Shirt,
  Briefcase,
  Bus,
  Palette,
  Zap,
  MapPin,
  HeartPulse
} from 'lucide-react';

interface CategoryIconProps {
  iconName: string;
  className?: string;
  color?: string;
}

export const CategoryLucideIcon: React.FC<CategoryIconProps> = ({ iconName, className = 'w-6 h-6', color }) => {
  const props = { className, style: color ? { color } : undefined };

  switch (iconName) {
    case 'Users':
      return <Users {...props} />;
    case 'UtensilsCrossed':
      return <UtensilsCrossed {...props} />;
    case 'Hash':
      return <Hash {...props} />;
    case 'Clock':
      return <Clock {...props} />;
    case 'Dog':
      return <Dog {...props} />;
    case 'Sun':
      return <Sun {...props} />;
    case 'Home':
      return <Home {...props} />;
    case 'Shirt':
      return <Shirt {...props} />;
    case 'Briefcase':
      return <Briefcase {...props} />;
    case 'Bus':
      return <Bus {...props} />;
    case 'Palette':
      return <Palette {...props} />;
    case 'Zap':
      return <Zap {...props} />;
    case 'MapPin':
      return <MapPin {...props} />;
    case 'HeartPulse':
      return <HeartPulse {...props} />;
    default:
      return <Users {...props} />;
  }
};

/**
 * Modern, consistent, friendly vector illustrations for Gagauzium categories.
 * Crafted with soft pastel shapes, dual-tone layers, and playful geometry.
 */
export const CategoryIllustration: React.FC<{ categoryId: string; size?: 'sm' | 'md' | 'lg' }> = ({
  categoryId,
  size = 'md'
}) => {
  const dimensions =
    size === 'sm' ? 'w-12 h-12' : size === 'lg' ? 'w-24 h-24 sm:w-28 sm:h-28' : 'w-16 h-16 sm:w-20 sm:h-20';

  return (
    <div className={`relative flex items-center justify-center shrink-0 ${dimensions}`}>
      <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-sm select-none" fill="none">
        {/* Category specific artwork */}
        {categoryId === 'family' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#EFF6FF" />
            <path d="M50 20C40 20 32 28 32 38C32 50 45 62 50 67C55 62 68 50 68 38C68 28 60 20 50 20Z" fill="#3B82F6" opacity="0.15" />
            {/* Person 1 */}
            <circle cx="38" cy="42" r="12" fill="#3B82F6" />
            <path d="M22 74C22 61 30 55 38 55C46 55 54 61 54 74" fill="#3B82F6" opacity="0.8" />
            {/* Person 2 */}
            <circle cx="62" cy="42" r="11" fill="#60A5FA" />
            <path d="M48 74C48 62 55 57 62 57C69 57 76 62 76 74" fill="#60A5FA" />
            {/* Child heart */}
            <path d="M50 38C48 35 44 35 43 38C42 41 47 45 50 48C53 45 58 41 57 38C56 35 52 35 50 38Z" fill="#EF4444" />
          </g>
        )}

        {categoryId === 'food' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#FFFBEB" />
            <circle cx="50" cy="50" r="32" fill="#F59E0B" opacity="0.2" />
            {/* Plate & Placinta pastry */}
            <ellipse cx="50" cy="56" rx="28" ry="16" fill="#FBBF24" />
            <ellipse cx="50" cy="52" rx="24" ry="13" fill="#F59E0B" />
            <path d="M30 50C38 42 62 42 70 50" stroke="#FFF" strokeWidth="3" strokeLinecap="round" />
            <circle cx="42" cy="48" r="3" fill="#D97706" />
            <circle cx="54" cy="54" r="3" fill="#D97706" />
            <circle cx="60" cy="46" r="2.5" fill="#D97706" />
          </g>
        )}

        {categoryId === 'numbers' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#ECFDF5" />
            <rect x="25" y="25" width="22" height="22" rx="6" fill="#10B981" />
            <text x="36" y="41" fill="#FFF" fontSize="16" fontWeight="bold" textAnchor="middle">1</text>
            <rect x="53" y="25" width="22" height="22" rx="6" fill="#34D399" />
            <text x="64" y="41" fill="#FFF" fontSize="16" fontWeight="bold" textAnchor="middle">2</text>
            <rect x="39" y="53" width="22" height="22" rx="6" fill="#059669" />
            <text x="50" y="69" fill="#FFF" fontSize="16" fontWeight="bold" textAnchor="middle">3</text>
          </g>
        )}

        {categoryId === 'time' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#F3E8FF" />
            <circle cx="50" cy="50" r="28" fill="#8B5CF6" />
            <circle cx="50" cy="50" r="22" fill="#FFF" />
            <path d="M50 34V50H62" stroke="#8B5CF6" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
            <circle cx="50" cy="50" r="3" fill="#6D28D9" />
          </g>
        )}

        {categoryId === 'animals' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#FCE7F3" />
            {/* Friendly Cat/Dog face */}
            <circle cx="50" cy="54" r="24" fill="#EC4899" />
            {/* Ears */}
            <path d="M30 36L22 18L40 28Z" fill="#DB2777" />
            <path d="M70 36L78 18L60 28Z" fill="#DB2777" />
            {/* Eyes */}
            <circle cx="40" cy="50" r="3.5" fill="#FFF" />
            <circle cx="60" cy="50" r="3.5" fill="#FFF" />
            <circle cx="40" cy="50" r="2" fill="#831843" />
            <circle cx="60" cy="50" r="2" fill="#831843" />
            {/* Nose */}
            <polygon points="50,56 46,53 54,53" fill="#FFF" />
          </g>
        )}

        {categoryId === 'nature' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#E0F2FE" />
            {/* Sun */}
            <circle cx="66" cy="34" r="14" fill="#FACE15" />
            {/* Mountain */}
            <polygon points="18,72 42,32 66,72" fill="#0284C7" />
            <polygon points="42,32 50,45 34,45" fill="#E0F2FE" />
            <polygon points="38,72 58,42 78,72" fill="#0369A1" opacity="0.9" />
          </g>
        )}

        {categoryId === 'home' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#EEF2FF" />
            {/* House */}
            <path d="M26 48L50 28L74 48V72H26V48Z" fill="#6366F1" />
            {/* Roof accent */}
            <path d="M22 48L50 25L78 48" stroke="#4F46E5" strokeWidth="5" strokeLinecap="round" />
            {/* Door & Window */}
            <rect x="43" y="54" width="14" height="18" rx="2" fill="#C7D2FE" />
            <circle cx="55" cy="63" r="1.5" fill="#4338CA" />
          </g>
        )}

        {categoryId === 'clothing' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#CCFBF1" />
            {/* Shirt / Dress */}
            <path d="M32 30L22 40L32 46V72H68V46L78 40L68 30L50 36Z" fill="#14B8A6" />
            <path d="M38 30C42 38 58 38 62 30" stroke="#0D9488" strokeWidth="3" fill="none" />
            <circle cx="50" cy="46" r="2" fill="#FFF" />
            <circle cx="50" cy="54" r="2" fill="#FFF" />
          </g>
        )}

        {categoryId === 'professions' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#FFEDD5" />
            {/* Briefcase & Hat */}
            <rect x="26" y="42" width="48" height="30" rx="6" fill="#F97316" />
            <path d="M40 42V35C40 33 42 31 44 31H56C58 31 60 33 60 35V42" stroke="#EA580C" strokeWidth="4" fill="none" />
            <line x1="26" y1="54" x2="74" y2="54" stroke="#FB923C" strokeWidth="3" />
            <rect x="46" y="51" width="8" height="6" rx="1" fill="#FFF" />
          </g>
        )}

        {categoryId === 'transport' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#DBEAFE" />
            {/* Car / Bus */}
            <rect x="22" y="44" width="56" height="22" rx="6" fill="#3B82F6" />
            <path d="M30 44L38 30H62L70 44Z" fill="#60A5FA" />
            <circle cx="36" cy="66" r="6" fill="#1E3A8A" />
            <circle cx="36" cy="66" r="3" fill="#FFF" />
            <circle cx="64" cy="66" r="6" fill="#1E3A8A" />
            <circle cx="64" cy="66" r="3" fill="#FFF" />
          </g>
        )}

        {categoryId === 'colors' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#F3E8FF" />
            {/* Palette */}
            <path d="M50 20C30 20 20 32 20 50C20 68 32 78 50 78C56 78 60 74 60 68C60 66 59 64 61 62C63 60 66 60 68 60C74 60 80 54 80 46C80 32 68 20 50 20Z" fill="#A855F7" />
            <circle cx="35" cy="38" r="4" fill="#EF4444" />
            <circle cx="50" cy="32" r="4" fill="#EAB308" />
            <circle cx="65" cy="38" r="4" fill="#3B82F6" />
            <circle cx="35" cy="55" r="4" fill="#10B981" />
          </g>
        )}

        {categoryId === 'actions' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#FEF9C3" />
            {/* Zap Energy */}
            <polygon points="56,18 28,52 48,52 42,82 72,48 52,48" fill="#EAB308" stroke="#CA8A04" strokeWidth="2" strokeLinejoin="round" />
          </g>
        )}

        {categoryId === 'places' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#FEE2E2" />
            {/* Map Pin */}
            <path d="M50 18C36 18 25 29 25 43C25 61 50 82 50 82C50 82 75 61 75 43C75 29 64 18 50 18Z" fill="#EF4444" />
            <circle cx="50" cy="40" r="10" fill="#FFF" />
          </g>
        )}

        {categoryId === 'anatomy' && (
          <g>
            <circle cx="50" cy="50" r="42" fill="#ECFCCB" />
            {/* Heart */}
            <path d="M50 74C50 74 24 55 24 38C24 28 32 22 40 22C46 22 50 26 50 26C50 26 54 22 60 22C68 22 76 28 76 38C76 55 50 74 50 74Z" fill="#84CC16" />
            <path d="M38 30C34 30 30 34 30 40" stroke="#FFF" strokeWidth="3" strokeLinecap="round" />
          </g>
        )}
      </svg>
    </div>
  );
};
