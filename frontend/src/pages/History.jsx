import React, { useState, useEffect } from 'react';
import { getHistory } from '../api/client';

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

    useEffect(() => {
        fetchHistory(1, filter);
    }, [filter]);

    const handlePageChange = (newPage) => {
        if (newPage >= 1 && newPage <= pagination.pages) {
            fetchHistory(newPage, filter);
        }
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

    return (
        <div className="container mx-auto px-4 py-12 max-w-5xl animate-fade-in">
            <div className="flex justify-between items-end mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-navy-900 mb-2">Historique des Analyses</h1>
                    <p className="text-slate-600">Retrouvez tous les sites précédemment analysés par PhishGuard.</p>
                </div>

                <div className="flex gap-2">
                    <button
                        onClick={() => setFilter(null)}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${!filter ? 'gradient-bg text-white' : 'bg-white text-slate-600 hover:bg-slate-100 border'}`}
                    >
                        Tous
                    </button>
                    <button
                        onClick={() => setFilter('safe')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filter === 'safe' ? 'bg-phish-safe text-white' : 'bg-white text-slate-600 hover:bg-slate-100 border'}`}
                    >
                        Sûre
                    </button>
                    <button
                        onClick={() => setFilter('suspicious')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filter === 'suspicious' ? 'bg-phish-suspicious text-white' : 'bg-white text-slate-600 hover:bg-slate-100 border'}`}
                    >
                        Suspecte
                    </button>
                    <button
                        onClick={() => setFilter('dangerous')}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filter === 'dangerous' ? 'bg-phish-dangerous text-white' : 'bg-white text-slate-600 hover:bg-slate-100 border'}`}
                    >
                        Dangereuse
                    </button>
                </div>
            </div>

            {error && (
                <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-8 rounded">
                    <p>{error}</p>
                </div>
            )}

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-slate-50 border-b border-slate-200">
                        <tr>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">URL</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Verdict</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Confiance</th>
                            <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Date</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {loading ? (
                            [...Array(5)].map((_, i) => (
                                <tr key={i} className="animate-pulse">
                                    <td className="px-6 py-6"><div className="h-4 bg-slate-100 rounded w-3/4"></div></td>
                                    <td className="px-6 py-6"><div className="h-6 bg-slate-100 rounded-full w-20 mx-auto"></div></td>
                                    <td className="px-6 py-6"><div className="h-4 bg-slate-100 rounded w-12 mx-auto"></div></td>
                                    <td className="px-6 py-6"><div className="h-4 bg-slate-100 rounded w-24 ml-auto"></div></td>
                                </tr>
                            ))
                        ) : history.length === 0 ? (
                            <tr>
                                <td colSpan="4" className="px-6 py-12 text-center text-slate-500">
                                    Aucune analyse trouvée pour ce filtre.
                                </td>
                            </tr>
                        ) : (
                            history.map((scan) => (
                                <tr key={scan.id} className="hover:bg-slate-50 transition-colors">
                                    <td className="px-6 py-4 font-medium text-slate-900 truncate max-w-sm">
                                        {scan.url}
                                    </td>
                                    <td className="px-6 py-4 text-center">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getBadgeClass(scan.risk_level)}`}>
                                            {translateLevel(scan.risk_level)}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-center font-bold text-slate-700">
                                        {scan.confidence}%
                                    </td>
                                    <td className="px-6 py-4 text-right text-slate-500 text-sm">
                                        {new Date(scan.created_at).toLocaleDateString('fr-FR')}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>

                {pagination.pages > 1 && (
                    <div className="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-between items-center">
                        <span className="text-sm text-slate-500">
                            Page {pagination.page} sur {pagination.pages}
                        </span>
                        <div className="flex gap-2">
                            <button
                                disabled={pagination.page <= 1}
                                onClick={() => handlePageChange(pagination.page - 1)}
                                className="px-3 py-1 bg-white border border-slate-300 rounded text-sm hover:bg-slate-50 disabled:opacity-50"
                            >
                                Précédent
                            </button>
                            <button
                                disabled={pagination.page >= pagination.pages}
                                onClick={() => handlePageChange(pagination.page + 1)}
                                className="px-3 py-1 bg-white border border-slate-300 rounded text-sm hover:bg-slate-50 disabled:opacity-50"
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
