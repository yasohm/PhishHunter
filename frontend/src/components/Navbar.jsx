import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const SunIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
    </svg>
);

const MoonIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
    </svg>
);

const Navbar = ({ dark, onToggleDark }) => {
    const location = useLocation();

    return (
        <nav className="gradient-bg text-white shadow-xl">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                <Link to="/" className="flex items-center space-x-2">
                    <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                        PhishGuard
                    </span>
                </Link>

                <div className="flex items-center gap-6">
                    <Link
                        to="/history"
                        className={`transition-colors hover:text-blue-200 ${location.pathname === '/history' ? 'font-semibold border-b-2 border-blue-400' : 'text-slate-300'}`}
                    >
                        Historique
                    </Link>
                    <Link
                        to="/"
                        className={`transition-colors hover:text-blue-200 ${location.pathname === '/' ? 'font-semibold border-b-2 border-blue-400' : 'text-slate-300'}`}
                    >
                        Accueil
                    </Link>
                    <Link
                        to="/email"
                        className={`transition-colors hover:text-blue-200 ${location.pathname === '/email' ? 'font-semibold border-b-2 border-blue-400' : 'text-slate-300'}`}
                    >
                        Analyse Email
                    </Link>

                    <button
                        onClick={onToggleDark}
                        title={dark ? 'Passer en mode clair' : 'Passer en mode sombre'}
                        className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors text-white"
                    >
                        {dark ? <SunIcon /> : <MoonIcon />}
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
