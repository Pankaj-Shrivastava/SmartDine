import React from 'react';
import { IoRestaurant, IoInformationCircle } from 'react-icons/io5';

export function EmptyState() {
    return (
        <section className="flex flex-col items-center justify-center text-center p-xl mt-xl animate-fade-up stagger-2">
            <div className="animate-bounce mb-lg">
                <IoRestaurant className="text-[64px] text-surface-variant" />
            </div>
            <h3 className="font-headline-md text-headline-md text-on-surface mb-sm">
                Ready to discover your next favorite restaurant?
            </h3>
            <p className="font-body-lg text-body-lg text-on-surface-variant max-w-md mb-lg">
                Fill in your preferences above and let our AI find the perfect dining spot for you.
            </p>
            <div className="flex items-center gap-xs text-secondary font-label-md bg-secondary/10 px-md py-sm rounded-full">
                <IoInformationCircle className="text-[18px]" />
                Try 'Koramangala' with 'Mid-Range' budget for popular spots
            </div>
        </section>
    );
}
