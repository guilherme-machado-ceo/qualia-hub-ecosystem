import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Atom, Brain, Shield, Code, Database, GitBranch, ExternalLink } from 'lucide-react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('overview')

  const features = [
    {
      icon: <Code className="h-6 w-6" />,
      title: "Gurudev-QC SDK",
      description: "SDK para desenvolvimento de algoritmos quânticos usando princípios holísticos",
      status: "Em Desenvolvimento"
    },
    {
      icon: <Atom className="h-6 w-6" />,
      title: "Simulador Quântico",
      description: "Simulador para testar algoritmos sem hardware quântico real",
      status: "Funcional"
    },
    {
      icon: <Brain className="h-6 w-6" />,
      title: "IA Quântica",
      description: "Aplicações demonstrativas de inteligência artificial quântica",
      status: "Planejado"
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Criptografia Pós-Quântica",
      description: "Demonstrações de segurança resistente a ataques quânticos",
      status: "Planejado"
    }
  ]

  const roadmapPhases = [
    {
      phase: "Fase 0 (2025-2026)",
      title: "Monitoramento e Posicionamento",
      description: "Publicação de whitepapers, participação em eventos-chave, radar de tendências consolidado."
    },
    {
      phase: "Fase 1 (2026-2028)",
      title: "Alianças Estratégicas",
      description: "Parcerias com centros acadêmicos, programas de mentoria, publicações conjuntas."
    },
    {
      phase: "Fase 2 (2028-2030)",
      title: "Modelo Teórico Gurudev-QC",
      description: "Elaboração de paper base seminal, construção de modelos de linguagem iniciais."
    },
    {
      phase: "Fase 3 (2030-2032)",
      title: "MVPs Teóricos",
      description: "Compiladores exploratórios, ferramentas de simulação, repositórios abertos."
    },
    {
      phase: "Fase 4 (2032-2035)",
      title: "Integração com Hardware",
      description: "Parcerias industriais, registro de patentes, captação de early users."
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center">
                <Atom className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">QIQU</h1>
                <p className="text-sm text-slate-400">Quantum Intelligence Quotient Unit</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-purple-400 border-purple-400">
                Hubstry DeepTech
              </Badge>
              <Button variant="outline" size="sm" className="text-white border-slate-600">
                <GitBranch className="h-4 w-4 mr-2" />
                GitHub
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4 bg-slate-800 border-slate-700">
            <TabsTrigger value="overview" className="text-slate-300 data-[state=active]:text-white">
              Visão Geral
            </TabsTrigger>
            <TabsTrigger value="features" className="text-slate-300 data-[state=active]:text-white">
              Recursos
            </TabsTrigger>
            <TabsTrigger value="roadmap" className="text-slate-300 data-[state=active]:text-white">
              Roadmap
            </TabsTrigger>
            <TabsTrigger value="docs" className="text-slate-300 data-[state=active]:text-white">
              Documentação
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="mt-6">
            <div className="grid gap-6 md:grid-cols-2">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Sobre o QIQU</CardTitle>
                  <CardDescription className="text-slate-400">
                    Núcleo conceitual e exploratório da Hubstry DeepTech
                  </CardDescription>
                </CardHeader>
                <CardContent className="text-slate-300">
                  <p className="mb-4">
                    O QIQU representa o braço conceitual e exploratório da Hubstry DeepTech,
                    dedicado ao monitoramento, pesquisa teórica e construção de uma visão
                    estratégica no campo da computação quântica.
                  </p>
                  <p>
                    Sua atuação abrange desdobramentos em Inteligência Artificial, criptografia,
                    linguagens de programação e infraestrutura de dados, com foco em linguagens
                    holísticas e simbólicas como Gurudev.
                  </p>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Filosofia</CardTitle>
                  <CardDescription className="text-slate-400">
                    "Escutar o tempo" - Kiku (聞く / 菊)
                  </CardDescription>
                </CardHeader>
                <CardContent className="text-slate-300">
                  <p className="mb-4">
                    O projeto QIQU se propõe a "escutar o tempo", capturando as tendências
                    quase imperceptíveis que emergem dos paradigmas tecnológicos quânticos.
                  </p>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Badge variant="secondary" className="bg-purple-900 text-purple-200">QI</Badge>
                      <span className="text-sm">Quantum Intelligence</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant="secondary" className="bg-blue-900 text-blue-200">QU</Badge>
                      <span className="text-sm">Quantum Unit</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="features" className="mt-6">
            <div className="grid gap-6 md:grid-cols-2">
              {features.map((feature, index) => (
                <Card key={index} className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <div className="flex items-center space-x-3">
                      <div className="p-2 rounded-lg bg-purple-900/50">
                        {feature.icon}
                      </div>
                      <div>
                        <CardTitle className="text-white">{feature.title}</CardTitle>
                        <Badge
                          variant={feature.status === 'Funcional' ? 'default' : 'secondary'}
                          className={feature.status === 'Funcional' ? 'bg-green-900 text-green-200' : 'bg-yellow-900 text-yellow-200'}
                        >
                          {feature.status}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-300">{feature.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="roadmap" className="mt-6">
            <div className="space-y-6">
              {roadmapPhases.map((phase, index) => (
                <Card key={index} className="bg-slate-800 border-slate-700">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-white">{phase.title}</CardTitle>
                      <Badge variant="outline" className="text-purple-400 border-purple-400">
                        {phase.phase}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-slate-300">{phase.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="docs" className="mt-6">
            <div className="grid gap-6 md:grid-cols-2">
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Whitepaper QIQU</CardTitle>
                  <CardDescription className="text-slate-400">
                    Documento fundacional do projeto
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-slate-300 mb-4">
                    Versão 0.1 - Julho de 2025. Documento que apresenta a visão,
                    estratégia e roadmap do projeto QIQU.
                  </p>
                  <Button variant="outline" size="sm" className="text-purple-400 border-purple-400">
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Ler Whitepaper
                  </Button>
                </CardContent>
              </Card>

              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Gurudev-QC SDK</CardTitle>
                  <CardDescription className="text-slate-400">
                    Documentação técnica do SDK
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-slate-300 mb-4">
                    Guias de instalação, exemplos de uso e referência da API
                    para o SDK Gurudev-QC.
                  </p>
                  <Button variant="outline" size="sm" className="text-blue-400 border-blue-400">
                    <Code className="h-4 w-4 mr-2" />
                    Ver Documentação
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-900/50 backdrop-blur-sm mt-12">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <p className="text-slate-400 text-sm">
              © 2025 QIQU - Hubstry DeepTech. Todos os direitos reservados.
            </p>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white">
                <GitBranch className="h-4 w-4 mr-2" />
                Contribuir
              </Button>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
