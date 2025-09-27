"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Atom, Brain, Shield, Code } from 'lucide-react';

const modules = [
  {
    icon: <Brain className="h-8 w-8 text-q-neon-cyan" />,
    title: "Simulação Quântica",
    description: "Simulador quântico de alta performance baseado em princípios harmônicos.",
  },
  {
    icon: <Shield className="h-8 w-8 text-q-neon-cyan" />,
    title: "Emulação de Segurança",
    description: "Emulação de protocolos de segurança quântica como QKD para testes de robustez.",
  },
  {
    icon: <Code className="h-8 w-8 text-q-neon-cyan" />,
    title: "Mapeamento Harmônico",
    description: "Compilador para traduzir séries harmônicas em estados quânticos executáveis.",
  },
  {
    icon: <Atom className="h-8 w-8 text-q-neon-cyan" />,
    title: "Integração com Hubstry",
    description: "Testes de compatibilidade com os protocolos Hubstry IoT e HALE.",
  },
];

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
    },
  },
};

const Cards = () => {
  return (
    <section className="container mx-auto px-4 py-16">
      <h2 className="text-4xl font-orbitron font-bold text-center text-white mb-12">
        Módulos Principais
      </h2>
      <motion.div
        className="grid md:grid-cols-2 lg:grid-cols-4 gap-8"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
        transition={{ staggerChildren: 0.2 }}
      >
        {modules.map((mod, i) => (
          <motion.div
            key={i}
            variants={cardVariants}
            whileHover={{ scale: 1.05, boxShadow: "0 0 20px rgba(0, 255, 255, 0.4)" }}
            transition={{ type: "spring", stiffness: 400, damping: 10 }}
            className="bg-q-dark-2/50 border border-q-neon-cyan/20 rounded-xl p-6 text-center flex flex-col items-center"
          >
            <div className="p-4 rounded-full bg-gradient-to-br from-q-neon-cyan/10 to-q-neon-magenta/10 mb-4">
              {mod.icon}
            </div>
            <h3 className="text-xl font-orbitron font-bold text-white mb-3">{mod.title}</h3>
            <p className="text-q-light/80 font-rajdhani text-sm flex-grow">{mod.description}</p>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
};

export default Cards;