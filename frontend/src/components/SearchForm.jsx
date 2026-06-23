import React, { useState } from 'react';
import { IoLocationSharp, IoWallet, IoPizza, IoStar, IoSparkles, IoList, IoSearch, IoAlertCircle, IoRefresh } from 'react-icons/io5';
import { useTranslation } from 'react-i18next';

const LOCATIONS = [
    "Koramangala",
    "Indiranagar",
    "Jayanagar",
    "Whitefield",
    "HSR Layout",
    "BTM Layout",
    "JP Nagar",
    "Marathahalli",
    "Malleshwaram",
    "Frazer Town"
];

const CUISINES = [
    "North Indian",
    "South Indian",
    "Chinese",
    "Fast Food",
    "Biryani",
    "Street Food",
    "Italian",
    "Continental",
    "Desserts",
    "Beverages"
];

export function SearchForm({ onSearch, isLoading }) {
    const { t } = useTranslation();
    const [formData, setFormData] = useState({
        location: '',
        budget: 'medium',
        cuisine: '',
        min_rating: 3.5,
        additional_preferences: '',
        num_recommendations: 5
    });
    const [error, setError] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'min_rating' || name === 'num_recommendations' ? Number(value) : value
        }));
        if (name === 'location') setError('');
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!formData.location) {
            setError(t('searchForm.locationRequired'));
            return;
        }
        onSearch(formData);
    };

    return (
        <section className="glass-card p-xl animate-fade-up stagger-1">
            <form onSubmit={handleSubmit} className="space-y-lg">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-lg">
                    {/* Location Dropdown */}
                    <div className="space-y-xs">
                        <label className="flex items-center gap-xs font-label-md text-label-md text-on-surface-variant">
                            <IoLocationSharp className="text-[18px]" />
                            {t('searchForm.location')} <span className="text-error">*</span>
                        </label>
                        <div className="relative">
                            <select 
                                name="location" 
                                value={formData.location} 
                                onChange={handleChange}
                                disabled={isLoading}
                                className={`w-full bg-black/20 border ${error ? 'border-error' : 'border-outline-variant'} rounded-xl px-md py-sm ${!formData.location ? 'text-on-surface-variant' : 'text-on-surface'} focus:border-secondary focus:ring-1 focus:ring-secondary transition-all outline-none`}
                            >
                                <option value="" disabled className="bg-background text-on-surface-variant">{t('searchForm.locationPlaceholder')}</option>
                                {LOCATIONS.map(loc => (
                                    <option key={loc} value={loc} className="bg-background text-on-surface">{loc}</option>
                                ))}
                            </select>
                            {error && (
                                <div className="absolute -bottom-6 left-0 flex items-center gap-1 text-error text-xs">
                                    <IoAlertCircle /> {error}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Budget */}
                    <div className="space-y-xs">
                        <label className="flex items-center gap-xs font-label-md text-label-md text-on-surface-variant">
                            <IoWallet className="text-[18px]" />
                            {t('searchForm.budget')}
                        </label>
                        <select 
                            name="budget" 
                            value={formData.budget} 
                            onChange={handleChange}
                            disabled={isLoading}
                            className="w-full bg-black/20 border border-outline-variant rounded-xl px-md py-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary transition-all outline-none"
                        >
                            <option value="low" className="bg-background text-on-surface">{t('searchForm.budgetLow')}</option>
                            <option value="medium" className="bg-background text-on-surface">{t('searchForm.budgetMedium')}</option>
                            <option value="high" className="bg-background text-on-surface">{t('searchForm.budgetHigh')}</option>
                        </select>
                    </div>

                    {/* Cuisine */}
                    <div className="space-y-xs">
                        <label className="flex items-center gap-xs font-label-md text-label-md text-on-surface-variant">
                            <IoPizza className="text-[18px]" />
                            {t('searchForm.cuisine')}
                        </label>
                        <select 
                            name="cuisine" 
                            value={formData.cuisine} 
                            onChange={handleChange}
                            disabled={isLoading}
                            className={`w-full bg-black/20 border border-outline-variant rounded-xl px-md py-sm ${!formData.cuisine ? 'text-on-surface-variant' : 'text-on-surface'} focus:border-secondary focus:ring-1 focus:ring-secondary transition-all outline-none`}
                        >
                            <option value="" className="bg-background text-on-surface-variant">{t('searchForm.cuisineAny')}</option>
                            {CUISINES.map(cuisine => (
                                <option key={cuisine} value={cuisine} className="bg-background text-on-surface">{cuisine}</option>
                            ))}
                        </select>
                    </div>

                    {/* Results Count */}
                    <div className="space-y-xs">
                        <label className="flex items-center gap-xs font-label-md text-label-md text-on-surface-variant">
                            <IoList className="text-[18px]" />
                            {t('searchForm.results')}
                        </label>
                        <input 
                            name="num_recommendations" 
                            type="number" 
                            min="1" 
                            max="10" 
                            value={formData.num_recommendations} 
                            onChange={handleChange}
                            disabled={isLoading}
                            className="w-full bg-black/20 border border-outline-variant rounded-xl px-md py-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary transition-all outline-none" 
                        />
                    </div>
                </div>

                {/* Rating Slider */}
                <div className="space-y-xs">
                    <div className="flex justify-between items-center">
                        <label className="flex items-center gap-xs font-label-md text-label-md text-on-surface-variant">
                            <IoStar className="text-[18px]" />
                            {t('searchForm.minRating')}
                        </label>
                        <span className="text-primary font-bold">{formData.min_rating.toFixed(1)} / 5.0</span>
                    </div>
                    <input 
                        name="min_rating" 
                        type="range" 
                        min="0" 
                        max="5" 
                        step="0.5" 
                        value={formData.min_rating} 
                        onChange={handleChange}
                        disabled={isLoading}
                        className="w-full h-1 bg-surface-variant rounded-full appearance-none rating-slider" 
                    />
                </div>

                {/* Additional Preferences */}
                <div className="space-y-xs">
                    <label className="flex items-center gap-xs font-label-md text-label-md text-on-surface-variant">
                        <IoSparkles className="text-[18px]" />
                        {t('searchForm.additionalPrefs')}
                    </label>
                    <textarea 
                        name="additional_preferences" 
                        rows="3" 
                        value={formData.additional_preferences} 
                        onChange={handleChange}
                        disabled={isLoading}
                        placeholder={t('searchForm.additionalPrefsPlaceholder')}
                        className="w-full bg-black/20 border border-outline-variant rounded-xl px-md py-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary transition-all outline-none resize-none"
                    ></textarea>
                </div>

                <button 
                    type="submit" 
                    disabled={isLoading}
                    className="w-full py-md bg-gradient-to-r from-primary-container to-secondary-container text-on-primary-fixed font-title-lg text-title-lg rounded-xl flex items-center justify-center gap-sm shadow-lg hover:brightness-110 active:scale-[0.98] transition-all disabled:opacity-70 disabled:cursor-not-allowed"
                >
                    {isLoading ? (
                        <>
                            <IoRefresh className="animate-spin text-[24px]" />
                            <span>{t('searchForm.searching')}</span>
                        </>
                    ) : (
                        <>
                            <IoSearch className="text-[24px]" />
                            <span>{t('searchForm.submit')}</span>
                        </>
                    )}
                </button>
            </form>
        </section>
    );
}
