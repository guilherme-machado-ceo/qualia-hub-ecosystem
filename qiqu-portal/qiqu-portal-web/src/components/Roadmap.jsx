import { motion } from 'framer-motion';
import { GitCommit, Milestone } from 'lucide-react';

const roadmapPhases = [
  {
    tag: "A",
    title: "Protocolo Harmônico Atual",
    description: "A base, com o protocolo IoT funcional sobre princípios harmônicos clássicos.",
  },
  {
    tag: "B",
    title: "Simulação Quântica Avançada",
    description: "Desenvolvimento de simuladores (Rust/Python) para modelar o comportamento quântico sobre a estrutura harmônica.",
  },
  {
    tag: "C",
    title: "Emulação Quântica Híbrida",
    description: "Criação de emuladores (DSP/FPGA) para validar os modelos em hardware clássico controlado.",
  },
  {
    tag: "D",
    title: "Integração com Hardware Quântico",
    description: "Mapeamento dos canais harmônicos para execução em QPUs reais, migrando da emulação para a computação genuína.",
  },
  {
    tag: "E",
    title: "Computação Quântica Distribuída",
    description: "Utilização de uma rede de dispositivos Hubstry para formar um sistema de computação quântica distribuída.",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.3,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, x: -50 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      type: 'spring',
      stiffness: 100,
    },
  },
};

const Roadmap = () => {
  return (
    <div className="container mx-auto px-4 py-12">
      <h2 className="text-4xl font-orbitron font-bold text-center text-white mb-16">
        Roadmap Evolutivo
      </h2>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
        className="relative"
      >
        {/* The connecting line */}
        <div className="absolute left-10 top-0 h-full w-0.5 bg-q-neon-cyan/20" aria-hidden="true"></div>

        {roadmapPhases.map((phase, index) => (
          <motion.div
            key={index}
            variants={itemVariants}
            className="relative pl-20 pb-12"
          >
            <div className="absolute left-[2.1rem] top-0">
              <div className="h-8 w-8 rounded-full bg-q-dark-2 border-2 border-q-neon-cyan flex items-center justify-center">
                <span className="font-tech-mono text-q-neon-cyan font-bold">{phase.tag}</span>
              </div>
            </div>
            <div className="bg-q-dark-2/50 p-6 rounded-lg border border-q-dark-2 hover:border-q-neon-magenta/50 transition-colors duration-300">
              <h3 className="text-xl font-orbitron font-bold text-q-neon-magenta mb-2">{phase.title}</h3>
              <p className="font-rajdhani text-q-light/80">{phase.description}</p>
            </div>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
};

export default Roadmap;