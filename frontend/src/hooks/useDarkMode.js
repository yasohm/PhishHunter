import { useState, useEffect } from 'react';

export function useDarkMode() {
    const [dark, setDark] = useState(() => {
        const stored = localStorage.getItem('phishguard-dark');
        if (stored !== null) return stored === 'true';
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    });

    useEffect(() => {
        const root = document.documentElement;
        root.classList.toggle('dark', dark);
        localStorage.setItem('phishguard-dark', String(dark));
    }, [dark]);

    return [dark, setDark];
}
