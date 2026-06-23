import React from 'react';
import { IoLocationSharp, IoWallet, IoPizza, IoStar, IoSearch } from 'react-icons/io5';
import { useTranslation } from 'react-i18next';

export function StatsBar({ metadata }) {
    const { t } = useTranslation();
    if (!metadata) return null;

    const items = [
        { icon: IoLocationSharp, text: metadata.location, color: 'text-secondary', border: 'border-secondary/30' },
        { icon: IoWallet, text: metadata.budget, color: 'text-tertiary', border: 'border-tertiary/30' },
        { icon: IoPizza, text: metadata.cuisine || t('results.anyCuisine'), color: 'text-primary', border: 'border-primary/30' },
        { icon: IoStar, text: t('results.rating', { rating: metadata.min_rating }), color: 'text-yellow-500', border: 'border-yellow-500/30' },
        { icon: IoSearch, text: t('results.candidates', { count: metadata.candidates_found }), color: 'text-on-surface-variant', border: 'border-outline-variant/30' }
    ];

    return (
        <div className="flex flex-wrap gap-sm mb-lg animate-fade-up stagger-2">
            {items.map((item, index) => {
                const Icon = item.icon;
                return (
                    <span key={index} className={`flex items-center gap-1 bg-surface-container-high px-md py-xs rounded-full border ${item.border} text-caption font-caption ${item.color}`}>
                        <Icon className="text-[14px]" />
                        {item.text}
                    </span>
                );
            })}
        </div>
    );
}
