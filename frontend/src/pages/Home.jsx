import React, { useState } from 'react';
import { analyzeUrl } from '../api/client';
import RiskGauge from '../components/RiskGauge';
import FeatureCard from '../components/FeatureCard';
import { Link } from 'react-router-dom';
import { exportJSON, exportPDF } from '../utils/export';

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

    return (
        <div className="container mx-auto px-4 py-12 max-w-4xl animate-fade-in">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-extrabold text-navy-900 dark:text-slate-100 mb-4">
                    Protégez-vous contre le Phishing
                </h1>
                <p className="text-lg text-slate-600 dark:text-slate-400">
                    Entrez une URL pour analyser sa légitimité en temps réel grâce à notre IA.
                </p>
            </div>

            <form onSubmit={handleAnalyze} className="mb-12">
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="https://exemple-site.com"
                        className="flex-1 p-4 rounded-xl border-2 border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:border-blue-500 outline-none transition-all text-lg shadow-sm"
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
                    <p className="text-slate-600 dark:text-slate-400 font-medium animate-pulse">Analyse en cours...</p>
                </div>
            )}

            {error && (
                <div className="bg-red-100 dark:bg-red-900/30 border-l-4 border-red-500 text-red-700 dark:text-red-400 p-4 mb-8 rounded" role="alert">
                    <p>{error}</p>
                </div>
            )}

            {result && (
                <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl overflow-hidden border border-slate-100 dark:border-slate-700 animate-fade-in">
                    <div className="p-8 border-b border-slate-100 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 flex justify-between items-center">
                        <div>
                            <p className="text-sm text-slate-500 dark:text-slate-400 uppercase tracking-widest font-semibold mb-1">Résultat de l'analyse</p>
                            <h2 className="text-xl font-bold truncate max-w-md dark:text-slate-100">{result.url}</h2>
                        </div>
                        {getVerdictBadge()}
                    </div>

                    <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                        <RiskGauge confidence={result.confidence} riskLevel={result.risk_level} />
                        <div className="grid grid-cols-2 gap-3">
                            {Object.entries(result.features)
                                .filter(([key]) => !key.endsWith('_UCI'))
                                .map(([key, value]) => (
                                    <FeatureCard key={key} name={key} value={value} />
                                ))}
                        </div>
                    </div>

                    <div className="p-8 bg-slate-50 dark:bg-slate-800/50 flex flex-wrap justify-between items-center gap-4 border-t border-slate-100 dark:border-slate-700">
                        <Link to="/history" className="text-blue-600 dark:text-blue-400 font-semibold hover:underline">
                            Voir l'historique complet des analyses →
                        </Link>
                        <div className="flex gap-2">
                            <button
                                onClick={() => exportJSON(result, 'url')}
                                className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-600 transition-all"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                                JSON
                            </button>
                            <button
                                onClick={() => exportPDF(result, 'url')}
                                className="flex items-center gap-2 px-4 py-2 gradient-bg text-white rounded-lg text-sm font-semibold hover:shadow-md transition-all"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                                Exporter PDF
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Home;
