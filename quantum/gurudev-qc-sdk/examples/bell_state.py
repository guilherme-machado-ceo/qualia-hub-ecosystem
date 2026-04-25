#!/usr/bin/env python3
"""
Exemplo: Estado de Bell usando Gurudev-QC SDK

Este exemplo demonstra como criar um estado de Bell (estado emaranhado)
usando a linguagem Gurudev-QC e o SDK.
"""

import sys
import os

# Adiciona o diretório pai ao path para importar o módulo gurudev_qc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gurudev_qc import GurudevQCSimulator


def main():
    """Executa o exemplo do estado de Bell."""
    
    print("=== Exemplo: Estado de Bell com Gurudev-QC ===\n")
    
    # Código Gurudev-QC para criar um estado de Bell
    bell_state_code = """
    # Estado de Bell: |Φ+⟩ = (|00⟩ + |11⟩)/√2
    # Em Gurudev-QC, usamos conceitos holísticos para expressar operações quânticas
    
    qubits: 2
    
    # 'harmony' representa a criação de superposição (Hadamard)
    # Filosoficamente, harmony cria equilíbrio entre estados |0⟩ e |1⟩
    harmony 0
    
    # 'entangle' representa o emaranhamento quântico (CNOT)
    # Filosoficamente, entangle conecta os destinos dos qubits
    entangle 0 1
    
    # Medimos ambos os qubits para observar a correlação
    measure: 0
    measure: 1
    """
    
    print("Código Gurudev-QC:")
    print(bell_state_code)
    print("\n" + "="*50 + "\n")
    
    # Cria o simulador
    simulator = GurudevQCSimulator(shots=1000)
    
    # Executa o código
    results = simulator.run_gurudev_code(bell_state_code)
    
    # Mostra os resultados
    print(simulator.visualize_results(results))
    
    # Análise dos resultados
    print("\n=== Análise dos Resultados ===")
    print("Em um estado de Bell perfeito, esperamos:")
    print("- 50% de probabilidade para |00⟩")
    print("- 50% de probabilidade para |11⟩")
    print("- 0% de probabilidade para |01⟩ e |10⟩")
    print("\nIsso demonstra o emaranhamento quântico: quando medimos")
    print("o primeiro qubit, o resultado do segundo qubit está")
    print("perfeitamente correlacionado.")
    
    # Verifica se os resultados estão corretos
    counts = results['measurement_counts']
    total = sum(counts.values())
    
    bell_states = counts.get('00', 0) + counts.get('11', 0)
    non_bell_states = counts.get('01', 0) + counts.get('10', 0)
    
    print(f"\nEstatísticas:")
    print(f"Estados de Bell (|00⟩ + |11⟩): {bell_states}/{total} ({bell_states/total*100:.1f}%)")
    print(f"Estados não-Bell (|01⟩ + |10⟩): {non_bell_states}/{total} ({non_bell_states/total*100:.1f}%)")
    
    if bell_states > 0.9 * total:
        print("✅ Sucesso! O estado de Bell foi criado corretamente.")
    else:
        print("⚠️  Aviso: Resultados inesperados. Verifique a implementação.")


if __name__ == "__main__":
    main()

