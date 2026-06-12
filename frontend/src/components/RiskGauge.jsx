import React from 'react';

const RiskGauge = ({ confidence, riskLevel }) => {
    // Calculer l'angle pour la jauge semi-circulaire (0 à 180 degrés)
    const angle = (confidence / 100) * 180;

    // Déterminer la couleur basée sur le niveau de risque
    const getColor = () => {
        if (riskLevel === 'safe') return '#22C55E'; // Green
        if (riskLevel === 'suspicious') return '#F97316'; // Orange
        return '#EF4444'; // Red
    };

    const color = getColor();

    return (
        <div className="flex flex-col items-center justify-center p-4">
            <div className="relative w-48 h-24 overflow-hidden">
                {/* Background arc */}
                <svg viewBox="0 0 100 50" className="w-full h-full">
                    <path
                        d="M 10 50 A 40 40 0 0 1 90 50"
                        fill="none"
                        stroke="#E2E8F0"
                        strokeWidth="8"
                    />
                    {/* Active risk arc */}
                    <path
                        d="M 10 50 A 40 40 0 0 1 90 50"
                        fill="none"
                        stroke={color}
                        strokeWidth="8"
                        strokeDasharray="125.6"
                        strokeDashoffset={125.6 - (confidence / 100) * 125.6}
                        className="transition-all duration-1000 ease-out"
                    />
                </svg>
                <div className="absolute bottom-0 left-0 right-0 text-center font-bold text-3xl">
                    {confidence}%
                </div>
            </div>
            <div className="mt-2 text-sm font-medium uppercase tracking-wider text-slate-500">
                Score de Danger
            </div>
        </div>
    );
};

export default RiskGauge;
