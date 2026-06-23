import React from 'react';
import { IoTrophy, IoStar, IoStarOutline, IoPizza, IoWallet, IoSparkles } from 'react-icons/io5';
import { useTranslation } from 'react-i18next';

export function RecommendationCard({ recommendation, index }) {
    const { t } = useTranslation();
    const { rank, name, cuisine, rating, cost_for_two, explanation } = recommendation;
    
    // Determine rank styling
    let badgeStyle = "bg-surface-variant text-on-surface-variant";
    let borderStyle = "border-outline-variant/20";
    if (rank === 1) {
        badgeStyle = "bg-gradient-to-r from-[#f0c040] to-[#e6a817] text-black";
        borderStyle = "gold-border";
    } else if (rank === 2) {
        badgeStyle = "bg-gradient-to-r from-[#C0C0C0] to-[#a8a8a8] text-black";
    } else if (rank === 3) {
        badgeStyle = "bg-gradient-to-r from-[#CD7F32] to-[#b8712e] text-white";
    }

    // Generate stars
    const numericRating = parseFloat(rating) || 0;
    const fullStars = Math.floor(numericRating);
    const hasHalfStar = numericRating - fullStars >= 0.5;
    
    const renderStars = () => {
        const stars = [];
        for (let i = 0; i < 5; i++) {
            if (i < fullStars || (i === fullStars && hasHalfStar)) {
                stars.push(<IoStar key={i} className="text-yellow-500 text-[14px]" />);
            } else {
                stars.push(<IoStarOutline key={i} className="text-yellow-500/50 text-[14px]" />);
            }
        }
        return stars;
    };

    return (
        <article className={`glass-card overflow-hidden ${borderStyle} hover:shadow-[0_0_20px_rgba(252,83,109,0.15)] hover:translate-y-[-4px] transition-all animate-fade-up`} style={{ animationDelay: `${index * 0.1}s` }}>
            <div className="p-xl flex flex-col md:flex-row gap-lg relative">
                {/* Rank Badge */}
                <div className={`absolute top-0 left-0 font-bold px-2 py-1 text-[10px] rounded-br-lg uppercase tracking-wider flex items-center gap-1 ${badgeStyle}`}>
                    {(rank <= 3) && <IoTrophy className="text-[12px]" />}
                    {t('results.rank', { rank })}
                </div>
                
                {/* Content */}
                <div className="flex-1 space-y-sm mt-4 md:mt-0">
                    <div className="flex justify-between items-start">
                        <h3 className="font-headline-md text-headline-md text-on-surface">{name}</h3>
                        <div className="flex items-center gap-xs bg-tertiary/10 text-tertiary px-sm py-[2px] rounded-full">
                            <IoStar className="text-[16px]" />
                            <span className="font-label-md text-label-md">{rating}</span>
                        </div>
                    </div>
                    
                    {/* Chips Row */}
                    <div className="flex flex-wrap gap-xs pb-sm border-b border-outline-variant/20">
                        <span className="flex items-center gap-1 text-caption font-caption text-on-surface-variant border border-secondary/30 bg-surface-container-high px-2 py-1 rounded-full">
                            <IoPizza className="text-secondary" /> {cuisine}
                        </span>
                        <span className="flex items-center gap-1 text-caption font-caption text-on-surface-variant border border-yellow-500/30 bg-surface-container-high px-2 py-1 rounded-full">
                            <div className="flex">{renderStars()}</div> {rating}/5
                        </span>
                        <span className="flex items-center gap-1 text-caption font-caption text-on-surface-variant border border-tertiary/30 bg-surface-container-high px-2 py-1 rounded-full">
                            <IoWallet className="text-tertiary" /> ₹{cost_for_two} {t('results.forTwo')}
                        </span>
                    </div>
                    
                    {/* AI Insight Section */}
                    <div className="bg-primary/5 border-l-4 border-primary p-md rounded-r-lg mt-md">
                        <div className="flex items-center gap-1 mb-1">
                            <IoSparkles className="text-primary text-[14px]" />
                            <span className="font-label-md text-label-md text-primary uppercase">{t('results.aiInsight')}</span>
                        </div>
                        <p className="font-body-md text-body-md text-on-surface-variant italic">
                            "{explanation}"
                        </p>
                    </div>
                </div>
            </div>
        </article>
    );
}
