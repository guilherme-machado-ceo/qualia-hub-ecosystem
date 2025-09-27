import { motion } from 'framer-motion';
import { Atom, Brain, Shield, Code, GitBranch, Share2, Sun, Moon } from 'lucide-react';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import Roadmap from '@/components/Roadmap';

// --- Header Component ---
const Header = () => {
  const { theme, setTheme } = useTheme();

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 bg-q-dark/80 backdrop-blur-sm border-b border-q-dark-2 z-50"
    >
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-full bg-gradient-to-br from-q-neon-cyan to-q-neon-magenta flex items-center justify-center shadow-[0_0_15px_rgba(0,255,255,0.5)]">
            <Atom className="h-6 w-6 text-white animate-pulse" />
          </div>
          <h1 className="text-2xl font-orbitron font-bold text-white">QIQU</h1>
        </div>
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="icon" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>
          <a href="https://github.com/guilherme-machado-ceo/qiqu-project" target="_blank" rel="noopener noreferrer">
            <Button variant="outline" className="border-q-neon-cyan text-q-neon-cyan hover:bg-q-neon-cyan hover:text-q-dark font-tech-mono">
              <GitBranch className="h-4 w-4 mr-2" />
              GitHub
            </Button>
          </a>
        </div>
      </div>
    </motion.header>
  );
};

// --- Hero Section Component ---
const Hero = () => (
  <div className="relative pt-32 pb-20 text-center bg-grid-pattern">
    <div className="absolute inset-0 bg-gradient-to-b from-q-dark via-q-dark to-transparent z-0"></div>
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="relative z-10"
    >
      <h1 className="text-5xl md:text-7xl font-orbitron font-extrabold text-white mb-4">
        Quantum Intelligence Quotient Unit
      </h1>
      <p className="text-lg md:text-xl text-q-light max-w-3xl mx-auto font-rajdhani">
        Explorando a fronteira da computação quântica e protocolos harmônicos para construir o futuro da inteligência de sistemas.
      </p>
    </motion.div>
  </div>
);

// --- Module Card Component ---
const ModuleCard = ({ icon, title, description, status }) => (
  <motion.div
    whileHover={{ scale: 1.05, boxShadow: "0px 0px 20px rgba(0, 255, 255, 0.3)" }}
    transition={{ type: "spring", stiffness: 300 }}
    className="bg-q-dark-2 border border-q-neon-cyan/20 rounded-lg p-6 flex flex-col items-start"
  >
    <div className="p-3 rounded-full bg-gradient-to-br from-q-neon-cyan to-q-neon-magenta mb-4">
      {icon}
    </div>
    <h3 className="text-xl font-orbitron font-bold text-white mb-2">{title}</h3>
    <p className="text-q-light font-rajdhani flex-grow mb-4">{description}</p>
    <span className="text-xs font-tech-mono text-q-neon-green">{status}</span>
  </motion.div>
);

// --- Main App Component ---
function App() {
  const modules = [
    { icon: <Brain className="h-6 w-6 text-white" />, title: "Simulação Quântica", description: "Simulador quântico de alta performance baseado em princípios harmônicos.", status: "✅ Stable" },
    { icon: <Shield className="h-6 w-6 text-white" />, title: "Emulação de Segurança", description: "Emulação de protocolos de segurança quântica como QKD.", status: "🧪 Testing" },
    { icon: <Code className="h-6 w-6 text-white" />, title: "Mapeamento Harmônico", description: "Compilador para traduzir séries harmônicas em estados quânticos.", status: "🚧 In Progress" },
    { icon: <Atom className="h-6 w-6 text-white" />, title: "Integração com Hubstry", description: "Testes de compatibilidade com os protocolos Hubstry IoT e HALE.", status: "✅ Stable" },
  ];

  return (
    <div className="min-h-screen bg-q-dark text-q-light">
      <Header />
      <main>
        <Hero />
        <div className="container mx-auto px-4 py-12">
          <h2 className="text-4xl font-orbitron font-bold text-center text-white mb-10">Módulos Principais</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {modules.map((mod, i) => (
              <ModuleCard key={i} {...mod} />
            ))}
          </div>
        </div>
        <Roadmap />
      </main>
      <Footer />
    </div>
  );
}

// --- Footer Component ---
const Footer = () => (
  <footer className="border-t border-q-dark-2 mt-20 py-8">
    <div className="container mx-auto px-4 text-center">
      <p className="text-sm text-q-light/70 font-rajdhani mb-2">
        © {new Date().getFullYear()} QIQU - Hubstry DeepTech.
      </p>
      <div className="flex justify-center items-center space-x-4">
        <a href="https://github.com/guilherme-machado-ceo/hubstry-hale-ecosystem" target="_blank" rel="noopener noreferrer" className="text-q-neon-cyan hover:underline font-tech-mono text-sm">
          Hubstry HALE
        </a>
        <span className="text-q-light/50">|</span>
        <a href="https://github.com/guilherme-machado-ceo/iot-protocol-hubstry" target="_blank" rel="noopener noreferrer" className="text-q-neon-cyan hover:underline font-tech-mono text-sm">
          IoT Protocol
        </a>
      </div>
    </div>
  </footer>
);

export default App;