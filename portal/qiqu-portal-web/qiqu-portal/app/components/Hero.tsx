"use client";

import React from 'react';
import Lottie from 'lottie-react';
import animationData from '../../public/assets/lotties/quantum-circuit.json';
import { Button } from './ui/button';

const Hero = () => {
  return (
    <section className="relative text-center py-20 md:py-32 overflow-hidden">
      <div className="absolute inset-0 bg-grid-pattern z-0"></div>
      <div className="absolute inset-0 bg-gradient-to-b from-q-dark via-q-dark to-transparent z-10"></div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeInOut" }}
        className="relative z-20"
      >
        <div className="w-48 h-48 md:w-64 md:h-64 mx-auto">
          <Lottie animationData={animationData} loop={true} />
        </div>

        <h1 className="font-orbitron text-5xl md:text-7xl font-extrabold text-white tracking-wider mt-4">
          QIQU
        </h1>
        <p className="mt-2 text-lg md:text-xl text-q-light font-rajdhani">
          HARMONIC QUANTUM INTELLIGENCE
        </p>
        <p className="mt-4 text-q-light/70 max-w-2xl mx-auto font-rajdhani">
          Explorando a fronteira da computação quântica e protocolos harmônicos para construir o futuro da inteligência de sistemas.
        </p>

        <div className="mt-8 flex justify-center gap-4">
            <Button className="font-orbitron hover:shadow-neon-glow">
                Explorar Simulação
            </Button>
            <Button variant="outline" className="font-orbitron border-q-neon-magenta text-q-neon-magenta hover:bg-q-neon-magenta hover:text-q-dark">
                Ver Documentação
            </Button>
        </div>
      </motion.div>
    </section>
  );
};

export default Hero;
