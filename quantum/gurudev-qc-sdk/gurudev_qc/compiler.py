"""
Compilador Gurudev-QC

Este módulo contém o compilador que traduz código Gurudev para circuitos quânticos.
"""

import numpy as np
from typing import List, Dict, Any, Optional
import json


class GurudevQCCompiler:
    """
    Compilador que traduz linguagem Gurudev para circuitos quânticos.
    
    A linguagem Gurudev-QC é uma extensão da linguagem Gurudev que incorpora
    conceitos de computação quântica, permitindo a expressão de algoritmos
    quânticos de forma holística e simbólica.
    """
    
    def __init__(self):
        self.quantum_gates = {
            'H': self._hadamard_gate,
            'X': self._pauli_x_gate,
            'Y': self._pauli_y_gate,
            'Z': self._pauli_z_gate,
            'CNOT': self._cnot_gate,
            'RZ': self._rotation_z_gate,
        }
        
        self.gurudev_mappings = {
            'harmony': 'H',  # Hadamard para criar superposição (harmonia)
            'flip': 'X',     # Pauli-X para inversão
            'phase': 'Z',    # Pauli-Z para mudança de fase
            'entangle': 'CNOT',  # CNOT para emaranhamento
            'rotate': 'RZ',  # Rotação Z
        }
    
    def compile(self, gurudev_code: str) -> Dict[str, Any]:
        """
        Compila código Gurudev-QC para um circuito quântico.
        
        Args:
            gurudev_code: Código fonte em Gurudev-QC
            
        Returns:
            Dicionário representando o circuito quântico compilado
        """
        lines = gurudev_code.strip().split('\n')
        circuit = {
            'qubits': 0,
            'gates': [],
            'measurements': []
        }
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if line.startswith('qubits:'):
                circuit['qubits'] = int(line.split(':')[1].strip())
            elif line.startswith('measure:'):
                qubit = int(line.split(':')[1].strip())
                circuit['measurements'].append(qubit)
            else:
                gate_info = self._parse_gate(line)
                if gate_info:
                    circuit['gates'].append(gate_info)
        
        return circuit
    
    def _parse_gate(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Analisa uma linha de código e extrai informações sobre a porta quântica.
        
        Args:
            line: Linha de código Gurudev-QC
            
        Returns:
            Dicionário com informações da porta ou None se inválida
        """
        parts = line.split()
        if len(parts) < 2:
            return None
            
        gurudev_op = parts[0]
        target = int(parts[1])
        
        if gurudev_op in self.gurudev_mappings:
            quantum_gate = self.gurudev_mappings[gurudev_op]
            
            gate_info = {
                'gate': quantum_gate,
                'target': target,
                'gurudev_concept': gurudev_op
            }
            
            # Para portas de dois qubits como CNOT
            if quantum_gate == 'CNOT' and len(parts) >= 3:
                gate_info['control'] = target
                gate_info['target'] = int(parts[2])
            
            # Para portas parametrizadas como rotações
            if quantum_gate == 'RZ' and len(parts) >= 3:
                gate_info['angle'] = float(parts[2])
            
            return gate_info
        
        return None
    
    def _hadamard_gate(self):
        """Matriz da porta Hadamard"""
        return np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    
    def _pauli_x_gate(self):
        """Matriz da porta Pauli-X"""
        return np.array([[0, 1], [1, 0]])
    
    def _pauli_y_gate(self):
        """Matriz da porta Pauli-Y"""
        return np.array([[0, -1j], [1j, 0]])
    
    def _pauli_z_gate(self):
        """Matriz da porta Pauli-Z"""
        return np.array([[1, 0], [0, -1]])
    
    def _cnot_gate(self):
        """Matriz da porta CNOT"""
        return np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1],
                        [0, 0, 1, 0]])
    
    def _rotation_z_gate(self, angle: float):
        """Matriz da porta de rotação Z"""
        return np.array([[np.exp(-1j * angle / 2), 0],
                        [0, np.exp(1j * angle / 2)]])
    
    def export_qasm(self, circuit: Dict[str, Any]) -> str:
        """
        Exporta o circuito compilado para formato QASM.
        
        Args:
            circuit: Circuito quântico compilado
            
        Returns:
            Código QASM representando o circuito
        """
        qasm_code = f"OPENQASM 2.0;\ninclude \"qelib1.inc\";\n"
        qasm_code += f"qreg q[{circuit['qubits']}];\n"
        qasm_code += f"creg c[{len(circuit['measurements'])}];\n\n"
        
        for gate in circuit['gates']:
            if gate['gate'] == 'H':
                qasm_code += f"h q[{gate['target']}];\n"
            elif gate['gate'] == 'X':
                qasm_code += f"x q[{gate['target']}];\n"
            elif gate['gate'] == 'Y':
                qasm_code += f"y q[{gate['target']}];\n"
            elif gate['gate'] == 'Z':
                qasm_code += f"z q[{gate['target']}];\n"
            elif gate['gate'] == 'CNOT':
                qasm_code += f"cx q[{gate['control']}],q[{gate['target']}];\n"
            elif gate['gate'] == 'RZ':
                qasm_code += f"rz({gate['angle']}) q[{gate['target']}];\n"
        
        for i, qubit in enumerate(circuit['measurements']):
            qasm_code += f"measure q[{qubit}] -> c[{i}];\n"
        
        return qasm_code


# Exemplo de uso
if __name__ == "__main__":
    compiler = GurudevQCCompiler()
    
    # Exemplo de código Gurudev-QC
    gurudev_code = """
    # Algoritmo de superposição simples em Gurudev-QC
    qubits: 2
    harmony 0    # Aplica Hadamard ao qubit 0 (cria harmonia/superposição)
    entangle 0 1 # Emaranha os qubits 0 e 1
    measure: 0
    measure: 1
    """
    
    circuit = compiler.compile(gurudev_code)
    print("Circuito compilado:")
    print(json.dumps(circuit, indent=2))
    
    print("\nCódigo QASM:")
    print(compiler.export_qasm(circuit))

