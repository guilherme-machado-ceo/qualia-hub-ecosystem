"""
Simulador Gurudev-QC

Este módulo contém o simulador quântico para executar circuitos Gurudev-QC.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
import random
from .compiler import GurudevQCCompiler


class GurudevQCSimulator:
    """
    Simulador quântico para executar circuitos compilados pelo Gurudev-QC Compiler.
    
    Este simulador permite testar e depurar algoritmos Gurudev-QC sem a necessidade
    de hardware quântico real, fornecendo resultados probabilísticos baseados na
    mecânica quântica.
    """
    
    def __init__(self, shots: int = 1024):
        """
        Inicializa o simulador.
        
        Args:
            shots: Número de execuções para estatísticas de medição
        """
        self.shots = shots
        self.compiler = GurudevQCCompiler()
    
    def run(self, circuit: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa um circuito quântico compilado.
        
        Args:
            circuit: Circuito quântico compilado pelo GurudevQCCompiler
            
        Returns:
            Resultados da simulação incluindo contagens de medição
        """
        num_qubits = circuit['qubits']
        
        # Inicializa o estado quântico |00...0⟩
        state_vector = np.zeros(2**num_qubits, dtype=complex)
        state_vector[0] = 1.0
        
        # Aplica as portas quânticas
        for gate in circuit['gates']:
            state_vector = self._apply_gate(state_vector, gate, num_qubits)
        
        # Realiza as medições
        measurement_results = self._measure(
            state_vector, 
            circuit['measurements'], 
            num_qubits
        )
        
        return {
            'final_state': state_vector,
            'measurement_counts': measurement_results,
            'shots': self.shots,
            'circuit_info': circuit
        }
    
    def run_gurudev_code(self, gurudev_code: str) -> Dict[str, Any]:
        """
        Compila e executa código Gurudev-QC diretamente.
        
        Args:
            gurudev_code: Código fonte em Gurudev-QC
            
        Returns:
            Resultados da simulação
        """
        circuit = self.compiler.compile(gurudev_code)
        return self.run(circuit)
    
    def _apply_gate(self, state: np.ndarray, gate: Dict[str, Any], num_qubits: int) -> np.ndarray:
        """
        Aplica uma porta quântica ao estado.
        
        Args:
            state: Vetor de estado atual
            gate: Informações da porta a ser aplicada
            num_qubits: Número total de qubits
            
        Returns:
            Novo vetor de estado após aplicar a porta
        """
        gate_type = gate['gate']
        target = gate['target']
        
        if gate_type == 'H':
            return self._apply_single_qubit_gate(state, target, self.compiler._hadamard_gate(), num_qubits)
        elif gate_type == 'X':
            return self._apply_single_qubit_gate(state, target, self.compiler._pauli_x_gate(), num_qubits)
        elif gate_type == 'Y':
            return self._apply_single_qubit_gate(state, target, self.compiler._pauli_y_gate(), num_qubits)
        elif gate_type == 'Z':
            return self._apply_single_qubit_gate(state, target, self.compiler._pauli_z_gate(), num_qubits)
        elif gate_type == 'CNOT':
            control = gate['control']
            return self._apply_cnot_gate(state, control, target, num_qubits)
        elif gate_type == 'RZ':
            angle = gate['angle']
            return self._apply_single_qubit_gate(
                state, target, self.compiler._rotation_z_gate(angle), num_qubits
            )
        
        return state
    
    def _apply_single_qubit_gate(self, state: np.ndarray, target: int, gate_matrix: np.ndarray, num_qubits: int) -> np.ndarray:
        """
        Aplica uma porta de um qubit ao estado.
        
        Args:
            state: Vetor de estado atual
            target: Qubit alvo
            gate_matrix: Matriz da porta quântica
            num_qubits: Número total de qubits
            
        Returns:
            Novo vetor de estado
        """
        new_state = np.zeros_like(state)
        
        for i in range(2**num_qubits):
            # Extrai o bit do qubit alvo
            target_bit = (i >> target) & 1
            
            # Calcula o índice com o bit do qubit alvo invertido
            flipped_i = i ^ (1 << target)
            
            # Aplica a matriz da porta
            new_state[i] += gate_matrix[target_bit, 0] * state[i]
            new_state[i] += gate_matrix[target_bit, 1] * state[flipped_i]
        
        return new_state
    
    def _apply_cnot_gate(self, state: np.ndarray, control: int, target: int, num_qubits: int) -> np.ndarray:
        """
        Aplica uma porta CNOT ao estado.
        
        Args:
            state: Vetor de estado atual
            control: Qubit de controle
            target: Qubit alvo
            num_qubits: Número total de qubits
            
        Returns:
            Novo vetor de estado
        """
        new_state = state.copy()
        
        for i in range(2**num_qubits):
            control_bit = (i >> control) & 1
            
            if control_bit == 1:
                # Se o qubit de controle é 1, inverte o qubit alvo
                flipped_i = i ^ (1 << target)
                new_state[i] = state[flipped_i]
        
        return new_state
    
    def _measure(self, state: np.ndarray, measurement_qubits: List[int], num_qubits: int) -> Dict[str, int]:
        """
        Realiza medições nos qubits especificados.
        
        Args:
            state: Vetor de estado final
            measurement_qubits: Lista de qubits a serem medidos
            num_qubits: Número total de qubits
            
        Returns:
            Dicionário com contagens dos resultados de medição
        """
        probabilities = np.abs(state)**2
        counts = {}
        
        for _ in range(self.shots):
            # Escolhe um estado baseado nas probabilidades
            measured_state = np.random.choice(len(state), p=probabilities)
            
            # Extrai os bits dos qubits medidos
            result_bits = []
            for qubit in measurement_qubits:
                bit = (measured_state >> qubit) & 1
                result_bits.append(str(bit))
            
            result_string = ''.join(result_bits)
            counts[result_string] = counts.get(result_string, 0) + 1
        
        return counts
    
    def get_state_probabilities(self, state: np.ndarray) -> Dict[str, float]:
        """
        Calcula as probabilidades de cada estado computacional.
        
        Args:
            state: Vetor de estado
            
        Returns:
            Dicionário com probabilidades de cada estado
        """
        probabilities = {}
        num_qubits = int(np.log2(len(state)))
        
        for i, amplitude in enumerate(state):
            prob = abs(amplitude)**2
            if prob > 1e-10:  # Apenas estados com probabilidade significativa
                binary_state = format(i, f'0{num_qubits}b')
                probabilities[binary_state] = prob
        
        return probabilities
    
    def visualize_results(self, results: Dict[str, Any]) -> str:
        """
        Cria uma visualização textual dos resultados.
        
        Args:
            results: Resultados da simulação
            
        Returns:
            String com visualização dos resultados
        """
        output = "=== Resultados da Simulação Gurudev-QC ===\n\n"
        
        # Informações do circuito
        circuit = results['circuit_info']
        output += f"Qubits: {circuit['qubits']}\n"
        output += f"Portas aplicadas: {len(circuit['gates'])}\n"
        output += f"Shots: {results['shots']}\n\n"
        
        # Contagens de medição
        output += "Contagens de Medição:\n"
        counts = results['measurement_counts']
        total_shots = sum(counts.values())
        
        for state, count in sorted(counts.items()):
            percentage = (count / total_shots) * 100
            output += f"  |{state}⟩: {count} ({percentage:.1f}%)\n"
        
        # Probabilidades do estado final
        output += "\nProbabilidades do Estado Final:\n"
        probs = self.get_state_probabilities(results['final_state'])
        
        for state, prob in sorted(probs.items()):
            percentage = prob * 100
            output += f"  |{state}⟩: {percentage:.1f}%\n"
        
        return output


# Exemplo de uso
if __name__ == "__main__":
    simulator = GurudevQCSimulator(shots=1000)
    
    # Exemplo de código Gurudev-QC para criar um estado de Bell
    bell_state_code = """
    # Estado de Bell em Gurudev-QC
    qubits: 2
    harmony 0      # Cria superposição no qubit 0
    entangle 0 1   # Emaranha os qubits 0 e 1
    measure: 0
    measure: 1
    """
    
    print("Executando código Gurudev-QC:")
    print(bell_state_code)
    
    results = simulator.run_gurudev_code(bell_state_code)
    print(simulator.visualize_results(results))

