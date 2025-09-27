"use client";

import React from 'react';
import { motion } from 'framer-motion';

const roadmapPhases = [
  {
    tag: "A",
    title: "Simulação Harmônica",
    description: "Desenvolvimento de simuladores para modelar o comportamento quântico sobre a estrutura harmônica do Hubstry.",
  },
  {
    tag: "B",
    title: "Emulação Quântica Híbrida",
    description: "Criação de emuladores para validar os modelos quânticos em hardware clássico controlado.",
  },
  {
    tag: "C",
    title: "Integração com Protocolos",
    description: "Integração e testes de compatibilidade com os protocolos Hubstry IoT e HALE.",
  },
  {
    tag: "D",
    title: "Validação e Benchmarking",
    description: "Execução de cenários de validação para medir fidelidade, segurança e performance.",
  },
  {
    tag: "E",
    title: "Migração para QPU Real",
    description: "Mapeamento dos canais harmônicos para execução em QPUs (Quantum Processing Units) reais.",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.3,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, x: -40 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      type: 'spring',
      stiffness: 120,
    },
  },
};

const Roadmap = () => {
  return (
    <section className="container mx-auto px-4 py-16">
      <h2 className="text-4xl font-orbitron font-bold text-center text-white mb-16">
        Roadmap Evolutivo
      </h2>
      <div className="relative max-w-2xl mx-auto">
        <div
          className="absolute left-6 top-0 h-full w-1 bg-gradient-to-b from-q-neon-cyan/50 via-q-neon-magenta/50 to-q-neon-green/50 rounded-full"
          aria-hidden="true"
        ></div>

        <motion.ul
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
        >
          {roadmapPhases.map((phase) => (
            <motion.li
              key={phase.tag}
              variants={itemVariants}
              className="relative pl-16 pb-12"
            >
              <div className="absolute left-0 top-0">
                <div className="h-12 w-12 rounded-full bg-q-dark-2 border-2 border-q-neon-cyan flex items-center justify-center shadow-neon-glow">
                  <span className="font-orbitron text-q-neon-cyan font-bold text-lg">{phase.tag}</span>
                </div>
              </div>
              <div className="bg-q-dark-2/60 p-6 rounded-lg border border-q-dark-2 hover:border-q-neon-magenta/50 transition-colors duration-300 backdrop-blur-sm">
                <h3 className="text-xl font-orbitron font-bold text-q-neon-magenta mb-2">{phase.title}</h3>
                <p className="font-rajdhani text-q-light/80">{phase.description}</p>
              </div>
            </motion.li>
          ))}
        </motion.ul>
      </div>
    </section>
  );
};

export default Roadmap;