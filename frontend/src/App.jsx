import React from 'react';
import { Hero } from './components/Hero';
import { SearchForm } from './components/SearchForm';
import { ResultsHeader } from './components/ResultsHeader';
import { StatsBar } from './components/StatsBar';
import { RecommendationCard } from './components/RecommendationCard';
import { SkeletonCard } from './components/SkeletonCard';
import { EmptyState } from './components/EmptyState';
import { ErrorBanner } from './components/ErrorBanner';
import { useRecommendations } from './hooks/useRecommendations';
import { useTranslation } from 'react-i18next';

function App() {
    const { results, metadata, isLoading, error, search, clearResults } = useRecommendations();
    const { t, i18n } = useTranslation();
    const hasSearched = results !== null || error !== null;

    const toggleLanguage = () => {
        const newLang = i18n.language === 'en' ? 'hi' : 'en';
        i18n.changeLanguage(newLang);
    };

    return (
        <div className="dark bg-background text-on-background min-h-screen">
            <header className="fixed top-0 w-full z-50 bg-surface/40 backdrop-blur-md border-b border-white/10 shadow-sm">
                <div className="flex justify-between items-center px-xl py-md max-w-7xl mx-auto">
                    <div className="flex items-center gap-xs">
                        <span className="font-display-lg text-display-lg font-bold bg-gradient-to-r from-primary to-primary-container bg-clip-text text-transparent">
                            {t('app.title')}
                        </span>
                    </div>
                    <button
                        onClick={toggleLanguage}
                        className="px-md py-sm bg-surface-container-high hover:bg-surface-variant text-on-surface rounded-full font-label-md text-label-md transition-colors border border-outline-variant/30"
                    >
                        {i18n.language === 'en' ? 'हिन्दी' : 'English'}
                    </button>
                </div>
            </header>

            <main className="pt-32 pb-2xl px-md max-w-[720px] mx-auto space-y-3xl">
                <Hero />

                <div className="space-y-3xl">
                    <SearchForm onSearch={search} isLoading={isLoading} />

                    {error && (
                        <ErrorBanner
                            type={error.type === "not_found" ? "warning" : "error"}
                            message={error.message}
                            onDismiss={clearResults}
                        />
                    )}

                    {isLoading && <SkeletonCard count={3} />}

                    {results && results.length > 0 && (
                        <section className="space-y-xl">
                            <ResultsHeader count={results.length} />
                            {metadata && <StatsBar metadata={metadata} />}
                            <div className="space-y-xl">
                                {results.map((rec, i) => (
                                    <RecommendationCard
                                        key={rec.rank}
                                        recommendation={rec}
                                        index={i}
                                    />
                                ))}
                            </div>
                        </section>
                    )}

                    {!hasSearched && !isLoading && <EmptyState />}
                </div>
            </main>
        </div>
    );
}

export default App;
