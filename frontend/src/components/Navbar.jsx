import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();

    return (
        <nav className="gradient-bg text-white shadow-xl">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                <Link to="/" className="text-2xl font-bold flex items-center gap-2 hover:opacity-90 transition-opacity">
                    <span>PhishGuard</span>
                    <span role="img" aria-label="shield">🛡️</span>
                </Link>
                <div className="flex gap-6">
                    <Link
                        to="/"
                        className={`transition-colors hover:text-blue-200 ${location.pathname === '/' ? 'font-semibold border-b-2 border-blue-400' : 'text-slate-300'}`}
                    >
                        Accueil
                    </Link>
                    <Link
                        to="/history"
                        className={`transition-colors hover:text-blue-200 ${location.pathname === '/history' ? 'font-semibold border-b-2 border-blue-400' : 'text-slate-300'}`}
                    >
                        Historique
                    </Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
