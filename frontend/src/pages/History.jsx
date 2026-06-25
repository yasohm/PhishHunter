import React, { useState, useEffect } from 'react';
import { getHistory } from '../api/client';
import { exportJSON, exportPDF } from '../utils/export';

const History = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState(null);
    const [pagination, setPagination] = useState({ page: 1, pages: 1 });

    const fetchHistory = async (page = 1, riskLevel = null) => {
        setLoading(true);
        try {
            const data = await getHistory(page, 15, riskLevel);
            setHistory(data.items);
            setPagination({ page: data.page, pages: data.pages });
        } catch (err) {
            setError("Impossible de récupérer l'historique.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchHistory(1, filter); }, [filter]);

    const handlePageChange = (newPage) => {
        if (newPage >= 1 && newPage <= pagination.pages) fetchHistory(newPage, filter);
    };

    const getBadgeClass = (level) => {
        if (level === 'safe') return 'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-400 dark:border-green-800';
        if (level === 'suspicious') return 'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/30 dark:text-orange-400 dark:border-orange-800';
        return 'bg-red-100 text-red-800 border-red-200 dark:bg-red-900/30 dark:text-red-400 dark:border-red-800';
    };

    const translateLevel = (level) => {
        if (level === 'safe') return 'Sûre';
        if (level === 'suspicious') return 'Suspecte';
        return 'Dangereuse';
    };

    const filterBtnClass = (active) =>
        active
            ? 'gradient-bg text-white'
            : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 border dark:border-slate-700';

    return (
        <div className="container mx-auto px-4 py-12 max-w-5xl animate-fade-in">
            <div className="flex justify-between items-end mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-navy-900 dark:text-slate-100 mb-2">Historique des Analyses</h1>
                    <p className="text-slate-600 dark:text-slate-400">Retrouvez tous les sites précédemment analysés par PhishHunter.</p>
                </div>
                <div className="flex gap-2">
                    {[
                        { label: 'Tous', value: null },
                        { label: 'Sûre', value: 'safe' },
                        { label: 'Suspecte', value: 'suspicious' },
                        { label: 'Dangereuse', value: 'dangerous' },
                    ].map(({ label, value }) => (
                        <button
                            key={label}
                            onClick={() => setFilter(value)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${value === null
                                ? filterBtnClass(!filter)
                                : filter === value
                                    ? (value === 'safe' ? 'bg-phish-safe text-white' : value === 'suspicious' ? 'bg-phish-suspicious text-white' : 'bg-phish-dangerous text-white')
                                    : filterBtnClass(false)
                            }`}
                        >
                            {label}
                        </button>
                    ))}
                </div>
            </div>

            {error && (
                <div className="bg-red-100 dark:bg-red-900/30 border-l-4 border-red-500 text-red-700 dark:text-red-400 p-4 mb-8 rounded">
                    <p>{error}</p>
                </div>
            )}

            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-slate-50 dark:bg-slate-700/50 border-b border-slate-200 dark:border-slate-700">
                        <tr>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">URL</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider text-center">Verdict</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider text-center">Confiance</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider text-right">Date</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider text-center">Export</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                        {loading ? (
                            [...Array(5)].map((_, i) => (
                                <tr key={i} className="animate-pulse">
                                    <td className="px-6 py-6"><div className="h-4 bg-slate-100 dark:bg-slate-700 rounded w-3/4"></div></td>
                                    <td className="px-6 py-6"><div className="h-6 bg-slate-100 dark:bg-slate-700 rounded-full w-20 mx-auto"></div></td>
                                    <td className="px-6 py-6"><div className="h-4 bg-slate-100 dark:bg-slate-700 rounded w-12 mx-auto"></div></td>
                                    <td className="px-6 py-6"><div className="h-4 bg-slate-100 dark:bg-slate-700 rounded w-24 ml-auto"></div></td>
                                    <td className="px-6 py-6"><div className="h-4 bg-slate-100 dark:bg-slate-700 rounded w-16 mx-auto"></div></td>
                                </tr>
                            ))
                        ) : history.length === 0 ? (
                            <tr>
                                <td colSpan="5" className="px-6 py-12 text-center text-slate-500 dark:text-slate-400">
                                    Aucune analyse trouvée pour ce filtre.
                                </td>
                            </tr>
                        ) : (
                            history.map((scan) => {
                                const isEmail = scan.url.startsWith('EMAIL:');
                                return (
                                    <tr key={scan.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
                                        <td className="px-6 py-4 font-medium text-slate-900 dark:text-slate-200 truncate max-w-sm">
                                            {scan.url}
                                        </td>
                                        <td className="px-6 py-4 text-center">
                                            <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getBadgeClass(scan.risk_level)}`}>
                                                {translateLevel(scan.risk_level)}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-center font-bold text-slate-700 dark:text-slate-300">
                                            {scan.confidence}%
                                        </td>
                                        <td className="px-6 py-4 text-right text-slate-500 dark:text-slate-400 text-sm">
                                            {new Date(scan.created_at).toLocaleDateString('fr-FR')}
                                        </td>
                                        <td className="px-6 py-4 text-center">
                                            <div className="flex items-center justify-center gap-1">
                                                <button
                                                    title="Exporter JSON"
                                                    onClick={() => exportJSON(scan, isEmail ? 'email' : 'url')}
                                                    className="p-1.5 rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600 hover:text-slate-800 dark:hover:text-slate-100 transition-all"
                                                >
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                                                </button>
                                                <button
                                                    title="Exporter PDF"
                                                    onClick={() => exportPDF(scan, isEmail ? 'email' : 'url')}
                                                    className="p-1.5 rounded-lg text-blue-500 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/30 hover:text-blue-700 dark:hover:text-blue-300 transition-all"
                                                >
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                );
                            })
                        )}
                    </tbody>
                </table>

                {pagination.pages > 1 && (
                    <div className="px-6 py-4 bg-slate-50 dark:bg-slate-700/50 border-t border-slate-200 dark:border-slate-700 flex justify-between items-center">
                        <span className="text-sm text-slate-500 dark:text-slate-400">
                            Page {pagination.page} sur {pagination.pages}
                        </span>
                        <div className="flex gap-2">
                            <button
                                disabled={pagination.page <= 1}
                                onClick={() => handlePageChange(pagination.page - 1)}
                                className="px-3 py-1 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 rounded text-sm hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50"
                            >
                                Précédent
                            </button>
                            <button
                                disabled={pagination.page >= pagination.pages}
                                onClick={() => handlePageChange(pagination.page + 1)}
                                className="px-3 py-1 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 rounded text-sm hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50"
                            >
                                Suivant
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default History;
