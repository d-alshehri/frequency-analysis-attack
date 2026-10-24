"""
Member 2 - Accuracy experiments for the report's Results section.

Encrypts the sample texts with random substitution keys, runs the
frequency attack, and measures how much of the original was recovered.

Run with:  python evaluate.py
"""

import string

from decrypt import assign_letter, build_mapping, decrypt
from samples import SAMPLES, encrypt, generate_key, invert_key


SEEDS = [1, 2, 3, 4, 5]


def count_letters_in(text):
    """Number of A-Z letters in the text."""
    return sum(char in string.ascii_letters for char in text)


def letter_accuracy(original, recovered):
    """Percentage of letters in the original text that were recovered correctly."""
    pairs = [
        (o.upper(), r.upper())
        for o, r in zip(original, recovered)
        if o in string.ascii_letters
    ]

    if not pairs:
        return 0.0

    correct = sum(o == r for o, r in pairs)
    return correct / len(pairs) * 100


def mapping_accuracy(mapping, key):
    """Percentage of distinct ciphertext letters whose guess is correct."""
    if not mapping:
        return 0.0

    true_mapping = invert_key(key)
    correct = sum(true_mapping[c] == p for c, p in mapping.items())
    return correct / len(mapping) * 100


def attack_accuracy(plaintext, seed):
    """Encrypt, attack, and return (mapping accuracy, letter accuracy)."""
    key = generate_key(seed)
    ciphertext = encrypt(plaintext, key)
    mapping = build_mapping(ciphertext)
    recovered = decrypt(ciphertext, mapping)

    return mapping_accuracy(mapping, key), letter_accuracy(plaintext, recovered)


def letter_window(text, start, n):
    """Return the part of text that covers n letters, starting at letter number start."""
    positions = [i for i, char in enumerate(text) if char in string.ascii_letters]
    end = min(start + n, len(positions)) - 1

    return text[positions[start]:positions[end] + 1]


def simulate_refinement(plaintext, seed, steps):
    """
    Simulate an analyst fixing one wrong letter at a time, starting with the
    most frequent wrongly-mapped ciphertext letter (as a person would after
    recognising a word).

    Returns a list of letter accuracies: index 0 is the automatic result,
    index i is the result after i manual corrections.
    """
    key = generate_key(seed)
    true_mapping = invert_key(key)
    ciphertext = encrypt(plaintext, key)
    mapping = build_mapping(ciphertext)

    history = [letter_accuracy(plaintext, decrypt(ciphertext, mapping))]

    for _ in range(steps):
        wrong = [c for c, p in mapping.items() if true_mapping[c] != p]
        if not wrong:
            break

        cipher_letter = wrong[0]
        mapping = assign_letter(mapping, cipher_letter, true_mapping[cipher_letter])
        history.append(letter_accuracy(plaintext, decrypt(ciphertext, mapping)))

    return history


def average(values):
    return sum(values) / len(values)


def experiment_samples():
    print("Experiment 1: accuracy on the three sample texts")
    print(f"(average over {len(SEEDS)} random keys)\n")
    print(f"{'Sample':<10}{'Letters':>9}{'Mapping acc.':>15}{'Text acc.':>12}")
    print("-" * 46)

    for name, text in SAMPLES.items():
        results = [attack_accuracy(text, seed) for seed in SEEDS]
        print(
            f"{name:<10}{count_letters_in(text):>9}"
            f"{average([r[0] for r in results]):>14.1f}%"
            f"{average([r[1] for r in results]):>11.1f}%"
        )


def experiment_length(windows=5):
    corpus = SAMPLES["medium"] + " " + SAMPLES["long"]
    total = count_letters_in(corpus)
    lengths = [n for n in (50, 100, 250, 500, 1000, 2000) if n < total] + [total]

    print("\nExperiment 2: accuracy vs. ciphertext length")
    print(f"(average over {windows} different parts of the text)\n")
    print(f"{'Letters':>9}{'Mapping acc.':>15}{'Text acc.':>12}")
    print("-" * 36)

    for n in lengths:
        if n == total:
            starts = [0]
        else:
            starts = [round(k * (total - n) / (windows - 1)) for k in range(windows)]

        results = [
            attack_accuracy(letter_window(corpus, start, n), seed=1)
            for start in starts
        ]
        print(
            f"{n:>9}"
            f"{average([r[0] for r in results]):>14.1f}%"
            f"{average([r[1] for r in results]):>11.1f}%"
        )


def experiment_refinement(steps=8):
    print("\nExperiment 3: effect of manual refinement (long sample, key seed 1)\n")
    print(f"{'Corrections':>12}{'Text acc.':>12}")
    print("-" * 24)

    for i, accuracy in enumerate(simulate_refinement(SAMPLES["long"], 1, steps)):
        print(f"{i:>12}{accuracy:>11.1f}%")


if __name__ == "__main__":
    experiment_samples()
    experiment_length()
    experiment_refinement()
