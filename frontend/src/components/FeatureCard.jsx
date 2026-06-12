import React from 'react';

const FeatureCard = ({ name, value, isSuspicious }) => {
    const formatName = (str) => {
        return str
            .replace(/_/g, ' ')
            .replace(/\b\w/g, (l) => l.toUpperCase());
    };

    const displayValue = () => {
        if (typeof value === 'boolean') return value ? 'Oui' : 'Non';
        if (typeof value === 'number' && value === 0 && name.includes('has')) return 'Non';
        if (typeof value === 'number' && value === 1 && name.includes('has')) return 'Oui';
        return value;
    };

    return (
        <div className={`p-3 rounded-lg border flex flex-col justify-between transition-all hover:shadow-md ${isSuspicious
                ? 'bg-red-50 border-red-200 text-red-900'
                : 'bg-green-50 border-green-200 text-green-900'
            }`}>
            <span className="text-xs font-semibold uppercase opacity-70 mb-1">
                {formatName(name)}
            </span>
            <div className="flex justify-between items-end">
                <span className="text-lg font-bold truncate pr-1">
                    {displayValue()}
                </span>
                <div className={`w-3 h-3 rounded-full ${isSuspicious ? 'bg-red-500' : 'bg-green-500'}`}></div>
            </div>
        </div>
    );
};

export default FeatureCard;
