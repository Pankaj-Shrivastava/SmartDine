import React from 'react';

export function SkeletonCard({ count = 3 }) {
    return (
        <div className="space-y-xl w-full">
            {Array.from({ length: count }).map((_, i) => (
                <article key={i} className={`glass-card p-xl flex flex-col md:flex-row gap-lg animate-fade-up`} style={{ animationDelay: `${i * 0.1}s` }}>
                    {/* Image Skeleton */}
                    <div className="relative w-full md:w-32 h-32 flex-shrink-0 rounded-lg overflow-hidden border border-outline-variant/20 bg-surface-variant/50 animate-pulse">
                    </div>
                    {/* Content Skeleton */}
                    <div className="flex-1 space-y-sm">
                        <div className="flex justify-between items-start">
                            <div className="h-8 w-48 bg-surface-variant/50 rounded animate-pulse"></div>
                            <div className="h-6 w-16 bg-surface-variant/50 rounded-full animate-pulse"></div>
                        </div>
                        <div className="flex gap-xs">
                            <div className="h-4 w-32 bg-surface-variant/50 rounded animate-pulse"></div>
                            <div className="h-4 w-24 bg-surface-variant/50 rounded animate-pulse"></div>
                        </div>
                        <div className="bg-primary/5 p-md rounded-lg mt-md h-20 animate-pulse border border-primary/10"></div>
                    </div>
                </article>
            ))}
        </div>
    );
}
