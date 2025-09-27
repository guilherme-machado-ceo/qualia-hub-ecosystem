# harmonic-mapping/mapeamento_qubit.py

import numpy as np

def converter_serie_harmonica_para_estados(frequencia_fundamental, num_harmonicos):
    """
    Converte uma série harmônica em uma representação de estados quânticos.

    Neste modelo, cada harmônico é mapeado para um "qubit" cujo estado é
    determinado por sua frequência e amplitude (aqui simplificada).
    O estado |0> pode representar um harmônico base ou não medido, enquanto
    o estado |1> representa um harmônico "excitado" ou detectado.

    A superposição é representada pelo conjunto de todos os estados.

    Args:
        frequencia_fundamental (float): A frequência base (f0) da série.
        num_harmonicos (int): O número de harmônicos a serem gerados.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um
              estado quântico mapeado a partir de um harmônico.
    """
    print(f"Mapeando {num_harmonicos} harmônicos da fundamental {frequencia_fundamental} Hz para estados quânticos...")

    estados_quanticos = []

    # Gera a série harmônica
    serie_harmonica = [frequencia_fundamental * n for n in range(1, num_harmonicos + 1)]

    for i, freq in enumerate(serie_harmonica):
        # Mapeamento simplificado:
        # - A fase pode ser mapeada para o ângulo no plano complexo.
        # - A amplitude (normalizada) pode ser mapeada para a probabilidade.

        # Exemplo: amplitude normalizada (aqui usamos um valor decrescente)
        amplitude = 1.0 / (i + 1)

        # O estado quântico é um vetor [alpha, beta] onde |alpha|^2 + |beta|^2 = 1
        # alpha: amplitude da componente |0>
        # beta:  amplitude da componente |1>

        # Aqui, modelamos a probabilidade de estar no estado |1> como a amplitude normalizada
        prob_estado_1 = amplitude**2

        alpha = np.sqrt(1 - prob_estado_1)
        beta = np.sqrt(prob_estado_1) # A fase pode ser complexa, aqui simplificamos

        estado = {
            'harmonico': i + 1,
            'frequencia': freq,
            'amplitude_normalizada': amplitude,
            'estado_quantico_vetor': [alpha, beta],
            'probabilidade_estado_1': prob_estado_1
        }
        estados_quanticos.append(estado)

    return estados_quanticos

def main():
    """
    Função principal para executar o exemplo de mapeamento.
    """
    print("--- Mapeamento de Série Harmônica para Estados Quânticos ---")

    F0 = 440.0  # Frequência fundamental (ex: Lá 440 Hz)
    N_HARMONICOS = 8 # Número de harmônicos a serem considerados

    # Realiza a conversão
    estados = converter_serie_harmonica_para_estados(F0, N_HARMONICOS)

    print("\nConversão completa. Estados resultantes:")
    for estado in estados:
        print(
            f"  - Harmônico {estado['harmonico']} ({estado['frequencia']:.2f} Hz): "
            f"P(|1>) = {estado['probabilidade_estado_1']:.3f}, "
            f"Vetor = [{estado['estado_quantico_vetor'][0]:.3f}, {estado['estado_quantico_vetor'][1]:.3f}]"
        )

    # Exemplo de como a superposição de todos os estados pode ser vista
    # A função de onda do sistema é a combinação de todos esses estados individuais
    print("\nO sistema completo está em uma superposição de todos os estados acima.")

if __name__ == "__main__":
    main()