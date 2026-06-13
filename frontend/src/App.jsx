import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import History from './pages/History'
import EmailAnalysis from './pages/EmailAnalysis'

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/history" element={<History />} />
            <Route path="/email" element={<EmailAnalysis />} />
          </Routes>
        </main>
        <footer className="py-8 text-center text-slate-400 text-sm border-t border-slate-100">
          PhishGuard — Analyseur de Phishing IA © 2026
        </footer>
      </div>
    </Router>
  )
}

export default App
