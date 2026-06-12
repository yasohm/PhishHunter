import React, { useState } from 'react';
import { analyzeUrl } from '../api/client';
import RiskGauge from '../components/RiskGauge';
import FeatureCard from '../components/FeatureCard';
import { Link } from 'react-router-dom';

const Home = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleAnalyze = async (e) => {
        e.preventDefault();
        if (!url) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await analyzeUrl(url);
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.detail || "Une erreur est survenue lors de l'analyse.");
        } finally {
            setLoading(false);
        }
    };

    const getVerdictBadge = () => {
        if (result.risk_level === 'safe')
            return <span className="bg-phish-safe text-white px-4 py-1 rounded-full font-bold">SÛRE</span>;
        if (result.risk_level === 'suspicious')
            return <span className="bg-phish-suspicious text-white px-4 py-1 rounded-full font-bold">SUSPECTE</span>;
        return <span className="bg-phish-dangerous text-white px-4 py-1 rounded-full font-bold">DANGEREUSE</span>;
    };

    const isFeatureSuspicious = (name, value) => {
        // Liste simple des caractéristiques considérées comme suspectes si vraies/positives
        if (name === 'has_https' && value === 0) return true;
        if (name === 'has_ip_address' && value === 1) return true;
        if (name === 'has_suspicious_keywords' && value === 1) return true;
        if (name === 'has_favicon_mismatch' && value === 1) return true;
        if (name === 'has_password_input' && value === 1) return true;
        if (name === 'page_title_mismatch' && value === 1) return true;
        if (name === 'subdomain_count' && value > 2) return true;
        if (name === 'special_char_count' && value > 2) return true;
        if (name === 'domain_age_days' && value < 180) return true;
        if (name === 'redirect_count' && value > 1) return true;
        if (name === 'html_form_count' && value > 2) return true;
        if (name === 'external_links_ratio' && value > 0.5) return true;
        return false;
    };

    return (
        <div className="container mx-auto px-4 py-12 max-w-4xl animate-fade-in">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-extrabold text-navy-900 mb-4">
                    Protégez-vous contre le Phishing
                </h1>
                <p className="text-lg text-slate-600">
                    Entrez une URL pour analyser sa légitimité en temps réel grâce à notre IA.
                </p>
            </div>

            <form onSubmit={handleAnalyze} className="mb-12">
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="https://exemple-site.com"
                        className="flex-1 p-4 rounded-xl border-2 border-slate-200 focus:border-blue-500 outline-none transition-all text-lg shadow-sm"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="gradient-bg text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform active:scale-95 transition-all disabled:opacity-50"
                    >
                        {loading ? 'Analyse...' : 'Analyser'}
                    </button>
                </div>
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
                            <p className="text-sm text-slate-500 uppercase tracking-widest font-semibold mb-1">Résultat de l'analyse</p>
                            <h2 className="text-xl font-bold truncate max-w-md">{result.url}</h2>
                        </div>
                        {getVerdictBadge()}
                    </div>

                    <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                        <RiskGauge confidence={result.confidence} riskLevel={result.risk_level} />

                        <div className="grid grid-cols-2 gap-3">
                            {Object.entries(result.features).slice(0, 8).map(([key, value]) => (
                                <FeatureCard
                                    key={key}
                                    name={key}
                                    value={value}
                                    isSuspicious={isFeatureSuspicious(key, value)}
                                />
                            ))}
                        </div>
                    </div>

                    <div className="p-8 bg-slate-50 flex justify-center border-t border-slate-100">
                        <Link to="/history" className="text-blue-600 font-semibold hover:underline">
                            Voir l'historique complet des analyses →
                        </Link>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Home;
