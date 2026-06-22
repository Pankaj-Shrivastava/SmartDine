import React from 'react';
import { IoSparkles } from 'react-icons/io5';

export function ResultsHeader({ count }) {
    return (
        <div className="flex flex-col items-start gap-xs mb-lg animate-fade-up stagger-2">
            <h2 className="flex items-center gap-sm font-headline-lg text-headline-lg text-on-surface">
                <IoSparkles className="text-primary" />
                Top {count} Picks For You
            </h2>
            <div className="h-1 w-48 bg-gradient-to-r from-primary-container to-secondary-container rounded-full opacity-60"></div>
        </div>
    );
}
