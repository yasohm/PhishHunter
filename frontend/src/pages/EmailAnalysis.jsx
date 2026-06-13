import React, { useState } from 'react';
import { analyzeEmail } from '../api/client';
import RiskGauge from '../components/RiskGauge';
import FeatureCard from '../components/FeatureCard';

const EmailAnalysis = () => {
    const [sujet, setSujet] = useState('');
    const [corps, setCorps] = useState('');
    const [expediteur, setExpediteur] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleAnalyze = async (e) => {
        e.preventDefault();
        if (!sujet || !corps) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await analyzeEmail(sujet, corps, expediteur);
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.detail || "Une erreur est survenue lors de l'analyse.");
        } finally {
            setLoading(false);
        }
    };

    const getVerdictBadge = () => {
        if (result.risk_level === 'safe')
            return <span className="bg-phish-safe text-white px-4 py-1 rounded-full font-bold uppercase">Légitime</span>;
        if (result.risk_level === 'suspicious')
            return <span className="bg-phish-suspicious text-white px-4 py-1 rounded-full font-bold uppercase">Suspect</span>;
        return <span className="bg-phish-dangerous text-white px-4 py-1 rounded-full font-bold uppercase">Phishing</span>;
    };

    const getBadgeClass = (level) => {
        if (level === 'safe') return 'bg-green-100 text-green-800 border-green-200';
        if (level === 'suspicious') return 'bg-orange-100 text-orange-800 border-orange-200';
        return 'bg-red-100 text-red-800 border-red-200';
    };

    const translateLevel = (level) => {
        if (level === 'safe') return 'Sûre';
        if (level === 'suspicious') return 'Suspecte';
        return 'Dangereuse';
    };

    const isFeatureSuspicious = (name, value) => {
        if (name === 'ratio_urls_suspectes' && value > 0.1) return true;
        if (name === 'has_link_text_mismatch' && value === 1) return true;
        if (name === 'has_urgent_keywords' && value === 1) return true;
        if (name === 'nb_mots_urgence' && value >= 2) return true;
        if (name === 'subject_entropy' && value > 4.2) return true;
        if (name === 'has_html_form' && value === 1) return true;
        if (name === 'has_password_field' && value === 1) return true;
        if (name === 'has_brand_spoofing' && value === 1) return true;
        if (name === 'special_chars_subject' && value > 2) return true;
        if (name === 'has_free_email_sender' && value === 1) return true;
        return false;
    };

    return (
        <div className="container mx-auto px-4 py-12 max-w-4xl animate-fade-in">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-extrabold text-navy-900 mb-4">
                    Analyse d'Email
                </h1>
                <p className="text-lg text-slate-600">
                    Analysez les emails suspects pour détecter des tentatives de hameçonnage.
                </p>
            </div>

            <form onSubmit={handleAnalyze} className="mb-12 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        placeholder="Expéditeur (ex: support@paypa1.com)"
                        className="p-4 rounded-xl border-2 border-slate-200 focus:border-blue-500 outline-none transition-all text-lg shadow-sm"
                        value={expediteur}
                        onChange={(e) => setExpediteur(e.target.value)}
                    />
                    <input
                        type="text"
                        placeholder="Objet de l'email *"
                        required
                        className="p-4 rounded-xl border-2 border-slate-200 focus:border-blue-500 outline-none transition-all text-lg shadow-sm"
                        value={sujet}
                        onChange={(e) => setSujet(e.target.value)}
                    />
                </div>
                <textarea
                    placeholder="Corps de l'email (texte ou HTML) *"
                    required
                    rows="8"
                    className="w-full p-4 rounded-xl border-2 border-slate-200 focus:border-blue-500 outline-none transition-all text-lg shadow-sm font-mono"
                    value={corps}
                    onChange={(e) => setCorps(e.target.value)}
                ></textarea>
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full gradient-bg text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform active:scale-95 transition-all disabled:opacity-50"
                >
                    {loading ? 'Analyse...' : 'Analyser l\'email'}
                </button>
            </form>

            {loading && (
                <div className="flex flex-col items-center justify-center p-12">
                    <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                    <p className="text-slate-600 font-medium animate-pulse">Analyse en cours...</p>
                </div>
            )}

            {error && (
                <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-8 rounded" role="alert">
                    <p>{error}</p>
                </div>
            )}

            {result && (
                <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100 animate-fade-in">
                    <div className="p-8 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
                        <div>
                            <p className="text-sm text-slate-500 uppercase tracking-widest font-semibold mb-1">Verdict de l'email</p>
                            <h2 className="text-xl font-bold truncate max-w-md">{result.sujet}</h2>
                            <p className="text-sm text-slate-400">De: {result.expediteur || "Inconnu"}</p>
                        </div>
                        {getVerdictBadge()}
                    </div>

                    <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                        <RiskGauge confidence={result.confidence} riskLevel={result.risk_level} />

                        <div className="grid grid-cols-2 gap-3">
                            {Object.entries(result.features).map(([key, value]) => (
                                <FeatureCard
                                    key={key}
                                    name={key}
                                    value={value}
                                    isSuspicious={isFeatureSuspicious(key, value)}
                                />
                            ))}
                        </div>
                    </div>

                    {result.url_analyses && result.url_analyses.length > 0 && (
                        <div className="p-8 border-t border-slate-100 bg-slate-50">
                            <h3 className="text-lg font-bold mb-4 flex items-center">
                                <span className="bg-blue-100 text-blue-600 px-2 py-0.5 rounded text-sm mr-2">
                                    {result.url_analyses.length}
                                </span>
                                Analyse détaillée des URLs
                            </h3>
                            <div className="space-y-3">
                                {result.url_analyses.map((analysis, index) => (
                                    <div key={index} className="flex items-center justify-between p-3 bg-white border border-slate-200 rounded-xl shadow-sm">
                                        <div className="font-mono text-sm break-all flex-1 mr-4">
                                            {analysis.url}
                                        </div>
                                        <div className="flex items-center gap-3 shrink-0">
                                            <span className="text-sm font-bold text-slate-500">{analysis.confidence}%</span>
                                            <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getBadgeClass(analysis.risk_level)}`}>
                                                {translateLevel(analysis.risk_level)}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                                <p className="text-xs text-slate-400 mt-4 italic">
                                    * Le score de danger global de l'email est déterminé par le niveau de risque le plus élevé détecté (contenu vs lien).
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default EmailAnalysis;
