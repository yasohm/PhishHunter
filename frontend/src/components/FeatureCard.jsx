import React from 'react';

const FeatureCard = ({ name, value }) => {
    // 1. Format common discrete values (UCI encoding)
    const isUciFeature = !(['url_length', 'URL_Length', 'nb_urls', 'body_length', 'nb_mots_urgence',
        'special_chars_subject', 'subject_entropy', 'ratio_urls_suspectes',
        'digit_count', 'url_entropy', 'subdomain_count', 'special_char_count',
        'html_form_count', 'external_links_ratio', 'redirect_count',
        'domain_age_days'].includes(name));

    const getUciDisplay = (val) => {
        if (val === 1) return { text: 'Légitime', styles: 'bg-green-50 border-green-200 text-green-900', dot: 'bg-green-500' };
        if (val === 0) return { text: 'Neutre', styles: 'bg-amber-50 border-amber-200 text-amber-900', dot: 'bg-amber-500' };
        if (val === -1) return { text: 'Phishing', styles: 'bg-red-50 border-red-200 text-red-900', dot: 'bg-red-500' };
        return null;
    };

    const uciData = isUciFeature ? getUciDisplay(value) : null;

    // 2. Format name
    const formatName = (str) => {
        return str
            .replace(/_/g, ' ')
            .replace(/\b\w/g, (l) => l.toUpperCase());
    };

    // 3. Determine if suspicious (for red cards)
    const isSuspiciousValue = value === -1;

    // 4. Final styling
    const cardStyles = uciData ? uciData.styles : 'bg-slate-50 border-slate-200 text-slate-900';
    const dotStyles = uciData ? uciData.dot : 'bg-slate-400';
    const displayText = uciData ? uciData.text : value;

    return (
        <div className={`p-3 rounded-lg border flex flex-col justify-between transition-all hover:shadow-md ${cardStyles}`}>
            <span className="text-xs font-semibold uppercase opacity-70 mb-1">
                {formatName(name)}
            </span>
            <div className="flex justify-between items-end">
                <span className="text-lg font-bold truncate pr-1">
                    {displayText}
                </span>
                <div className={`w-3 h-3 rounded-full ${dotStyles}`}></div>
            </div>
        </div>
    );
};

export default FeatureCard;
