import React from 'react';
import { IoSparkles } from 'react-icons/io5';
import { useTranslation } from 'react-i18next';

export function ResultsHeader({ count }) {
    const { t } = useTranslation();
    return (
        <div className="flex flex-col items-start gap-xs mb-lg animate-fade-up stagger-2">
            <h2 className="flex items-center gap-sm font-headline-lg text-headline-lg text-on-surface">
                <IoSparkles className="text-primary" />
                {t('results.header', { count })}
            </h2>
            <div className="h-1 w-48 bg-gradient-to-r from-primary-container to-secondary-container rounded-full opacity-60"></div>
        </div>
    );
}
