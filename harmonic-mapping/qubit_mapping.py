# harmonic-mapping/qubit_mapping.py

import numpy as np

def convert_harmonic_series_to_states(fundamental_frequency, num_harmonics):
    """
    Converts a harmonic series into a representation of quantum states.

    In this model, each harmonic is mapped to a "qubit" whose state is
    determined by its frequency and amplitude (simplified here).
    The |0> state can represent a base or unmeasured harmonic, while the
    |1> state represents an "excited" or detected harmonic.

    The superposition is represented by the set of all states.

    Args:
        fundamental_frequency (float): The base frequency (f0) of the series.
        num_harmonics (int): The number of harmonics to generate.

    Returns:
        list: A list of dictionaries, where each dictionary represents a
              quantum state mapped from a harmonic.
    """
    print(f"Mapping {num_harmonics} harmonics from the fundamental {fundamental_frequency} Hz to quantum states...")

    quantum_states = []

    # Generate the harmonic series
    harmonic_series = [fundamental_frequency * n for n in range(1, num_harmonics + 1)]

    for i, freq in enumerate(harmonic_series):
        # Simplified mapping:
        # - The phase could be mapped to the angle in the complex plane.
        # - The normalized amplitude can be mapped to the probability.

        # Example: normalized amplitude (here we use a decreasing value)
        amplitude = 1.0 / (i + 1)

        # The quantum state is a vector [alpha, beta] where |alpha|^2 + |beta|^2 = 1
        # alpha: amplitude of the |0> component
        # beta:  amplitude of the |1> component

        # Here, we model the probability of being in state |1> as the normalized amplitude
        prob_state_1 = amplitude**2

        alpha = np.sqrt(1 - prob_state_1)
        beta = np.sqrt(prob_state_1) # The phase could be complex, simplified here

        state = {
            'harmonic': i + 1,
            'frequency': freq,
            'normalized_amplitude': amplitude,
            'quantum_state_vector': [alpha, beta],
            'probability_state_1': prob_state_1
        }
        quantum_states.append(state)

    return quantum_states

def main():
    """
    Main function to run the mapping example.
    """
    print("--- Mapping Harmonic Series to Quantum States ---")

    F0 = 440.0  # Fundamental frequency (e.g., A4 440 Hz)
    N_HARMONICS = 8 # Number of harmonics to consider

    # Perform the conversion
    states = convert_harmonic_series_to_states(F0, N_HARMONICS)

    print("\nConversion complete. Resulting states:")
    for state in states:
        print(
            f"  - Harmonic {state['harmonic']} ({state['frequency']:.2f} Hz): "
            f"P(|1>) = {state['probability_state_1']:.3f}, "
            f"Vector = [{state['quantum_state_vector'][0]:.3f}, {state['quantum_state_vector'][1]:.3f}]"
        )

    # Example of how the superposition of all states can be viewed
    # The system's wave function is the combination of all these individual states
    print("\nThe complete system is in a superposition of all the states above.")

if __name__ == "__main__":
    main()