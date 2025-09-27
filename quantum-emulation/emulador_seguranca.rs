// quantum-emulation/emulador_seguranca.rs

use rand::Rng;

/// Represents a quantum key, encoded using harmonic properties.
struct QuantumKey {
    bits: Vec<u8>,
    encoding_basis: Vec<char>, // '+' or 'x' basis
}

/// Represents a communication channel based on Hubstry's harmonic protocol.
struct HarmonicChannel {
    frequency: f64,
    noise_level: f64,
}

/// Emulates the Quantum Key Distribution (QKD) BB84 protocol.
/// This function simulates the key generation, transmission over a noisy
/// harmonic channel, and security verification.
///
/// # Arguments
/// * `channel` - The harmonic channel used for transmission.
/// * `key_length` - The number of bits in the generated key.
///
/// # Returns
/// A tuple containing the generated key and the quantum bit error rate (QBER).
fn emulate_qkd_bb84(channel: &HarmonicChannel, key_length: usize) -> (QuantumKey, f64) {
    println!(
        "Emulating QKD over harmonic channel at {:.2} Hz with noise level {:.3}",
        channel.frequency, channel.noise_level
    );

    let mut rng = rand::thread_rng();

    // 1. Alice generates a random key and random encoding bases.
    let alice_key = QuantumKey {
        bits: (0..key_length).map(|_| rng.gen_range(0..=1)).collect(),
        encoding_basis: (0..key_length)
            .map(|_| if rng.gen() { '+' } else { 'x' })
            .collect(),
    };

    // 2. Bob chooses random measurement bases.
    let bob_measurement_basis: Vec<char> = (0..key_length)
        .map(|_| if rng.gen() { '+' } else { 'x' })
        .collect();

    // 3. Simulate transmission and measurement, introducing noise.
    let mut bob_measured_bits = Vec::with_capacity(key_length);
    for i in 0..key_length {
        let mut bit = alice_key.bits[i];
        // Introduce an error based on the channel's noise level.
        if rng.gen::<f64>() < channel.noise_level {
            bit = 1 - bit; // Flip the bit to simulate an error.
        }
        bob_measured_bits.push(bit);
    }

    // 4. Sifting: Alice and Bob compare bases and keep only the bits where bases matched.
    let mut sifted_key_indices = Vec::new();
    for i in 0..key_length {
        if alice_key.encoding_basis[i] == bob_measurement_basis[i] {
            sifted_key_indices.push(i);
        }
    }

    // 5. QBER Calculation: A subset of the sifted key is used to estimate the error rate.
    let sample_size = sifted_key_indices.len() / 2;
    let mut errors = 0;
    for i in 0..sample_size {
        let index = sifted_key_indices[i];
        if alice_key.bits[index] != bob_measured_bits[index] {
            errors += 1;
        }
    }

    let qber = if sample_size > 0 {
        errors as f64 / sample_size as f64
    } else {
        0.0
    };

    // The final key is the remaining part of the sifted key.
    let final_key_bits: Vec<u8> = sifted_key_indices[sample_size..]
        .iter()
        .map(|&i| alice_key.bits[i])
        .collect();

    let final_key = QuantumKey {
        bits: final_key_bits,
        encoding_basis: Vec::new(), // Basis info is not part of the final key
    };

    (final_key, qber)
}

fn main() {
    println!("--- Quantum Security Emulation: BB84 Protocol ---");

    // Define a harmonic channel for secure communication.
    // Higher harmonics might be chosen for their lower energy and higher security potential.
    let secure_channel = HarmonicChannel {
        frequency: 440.0 * 16.0, // 16th harmonic
        noise_level: 0.05,       // 5% noise/error probability
    };

    let key_length = 128;
    let (sifted_key, qber) = emulate_qkd_bb84(&secure_channel, key_length);

    println!("\nEmulation complete.");
    println!("  - Final sifted key length: {}", sifted_key.bits.len());
    println!("  - Estimated QBER: {:.2}%", qber * 100.0);

    // If QBER is below a certain threshold, the key is considered secure.
    if qber < 0.1 {
        println!("  - Security status: Key is considered SECURE.");
    } else {
        println!("  - Security status: Key is COMPROMISED (QBER too high).");
    }
}