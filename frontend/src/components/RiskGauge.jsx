import React from 'react';

const RiskGauge = ({ confidence, riskLevel }) => {
    const getColor = () => {
        if (riskLevel === 'safe') return '#22C55E';
        if (riskLevel === 'suspicious') return '#F97316';
        return '#EF4444';
    };

    const color = getColor();
    const trackColor = 'var(--gauge-track, #E2E8F0)';

    return (
        <div className="flex flex-col items-center justify-center p-4 [--gauge-track:#E2E8F0] dark:[--gauge-track:#334155]">
            <div className="relative w-48 h-24 overflow-hidden">
                <svg viewBox="0 0 100 50" className="w-full h-full">
                    <path
                        d="M 10 50 A 40 40 0 0 1 90 50"
                        fill="none"
                        stroke={trackColor}
                        strokeWidth="8"
                    />
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
                <div className="absolute bottom-0 left-0 right-0 text-center font-bold text-3xl text-slate-900 dark:text-slate-100">
                    {confidence}%
                </div>
            </div>
            <div className="mt-2 text-sm font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400">
                Score de Danger
            </div>
        </div>
    );
};

export default RiskGauge;
