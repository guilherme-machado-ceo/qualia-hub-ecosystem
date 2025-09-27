"use client";

import React from 'react';

const Footer = () => {
  return (
    <footer className="border-t border-q-neon-cyan/10 mt-20 py-8">
      <div className="container mx-auto px-4 text-center">
        <p className="text-sm text-q-light/70 font-rajdhani mb-2">
          © {new Date().getFullYear()} QIQU - Hubstry DeepTech. All rights reserved.
        </p>
        <div className="flex justify-center items-center space-x-4">
          <a href="https://github.com/guilherme-machado-ceo/hubstry-hale-ecosystem" target="_blank" rel="noopener noreferrer" className="text-q-neon-cyan hover:underline font-sans text-sm">
            Hubstry HALE Ecosystem
          </a>
          <span className="text-q-light/50">|</span>
          <a href="https://github.com/guilherme-machado-ceo/iot-protocol-hubstry" target="_blank" rel="noopener noreferrer" className="text-q-neon-cyan hover:underline font-sans text-sm">
            IoT Protocol Hubstry
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;