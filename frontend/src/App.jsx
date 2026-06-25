import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import History from './pages/History'
import EmailAnalysis from './pages/EmailAnalysis'
import { useDarkMode } from './hooks/useDarkMode'

function App() {
  const [dark, setDark] = useDarkMode();

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-900 transition-colors duration-200">
        <Navbar dark={dark} onToggleDark={() => setDark(d => !d)} />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/history" element={<History />} />
            <Route path="/email" element={<EmailAnalysis />} />
          </Routes>
        </main>
        <footer className="py-8 text-center text-slate-400 dark:text-slate-600 text-sm border-t border-slate-100 dark:border-slate-800">
          PhishHunter — Analyseur de Phishing IA © 2026
        </footer>
      </div>
    </Router>
  )
}

export default App
