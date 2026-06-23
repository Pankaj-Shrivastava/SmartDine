import React from 'react';
import { IoRestaurant } from 'react-icons/io5';
import { useTranslation } from 'react-i18next';

export function Hero() {
    const { t } = useTranslation();
    return (
        <section className="text-center space-y-md animate-fade-up">
            <div className="flex justify-center items-center gap-sm mb-xs">
                <IoRestaurant className="text-primary text-[48px]" />
                <h1 className="font-display-lg text-display-lg bg-gradient-to-r from-primary-container to-secondary-container bg-clip-text text-transparent">
                    {t('app.title')}
                </h1>
            </div>
            <div className="flex flex-col items-center gap-xs">
                <p className="font-headline-md text-headline-md text-on-surface">{t('hero.subtitle')}</p>
                <div className="gradient-underline"></div>
            </div>
            <p className="font-body-lg text-body-lg text-on-surface-variant max-w-lg mx-auto">
                {t('hero.description')}
            </p>
        </section>
    );
}
