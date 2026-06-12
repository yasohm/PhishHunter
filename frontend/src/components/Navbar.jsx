import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();

    return (
        <nav className="gradient-bg text-white shadow-xl">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                <Link to="/" className="flex items-center space-x-2">
                    <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                        PhishGuard
                    </span>
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
