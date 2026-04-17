"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Atom, GitBranch, Sun, Moon } from 'lucide-react';
import { useTheme } from 'next-themes';
import { Button } from './ui/button';

const Header = () => {
  const { theme, setTheme } = useTheme();

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="fixed top-0 left-0 right-0 bg-q-dark/80 backdrop-blur-sm border-b border-q-neon-cyan/10 z-50"
    >
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-full bg-gradient-to-br from-q-neon-cyan to-q-neon-magenta flex items-center justify-center shadow-neon-glow">
            <Atom className="h-6 w-6 text-white" />
          </div>
          <h1 className="text-2xl font-orbitron font-bold text-white">QIQU</h1>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="icon" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0 text-q-light" />
            <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100 text-q-light" />
            <span className="sr-only">Toggle theme</span>
          </Button>
          <a href="https://github.com/guilherme-machado-ceo/qiqu-project" target="_blank" rel="noopener noreferrer">
            <Button variant="outline" className="border-q-neon-cyan text-q-neon-cyan hover:bg-q-neon-cyan hover:text-q-dark font-sans">
              <GitBranch className="h-4 w-4 mr-2" />
              GitHub
            </Button>
          </a>
        </div>
      </div>
    </motion.header>
  );
};

export default Header;