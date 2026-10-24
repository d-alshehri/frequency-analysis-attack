"""
Member 2 - Letter mapping and approximate decryption.

Uses the frequency functions from frequency.py to estimate which plaintext
letter each ciphertext letter stands for, then applies that estimate to
produce an approximate plaintext. The user can then refine the mapping by
hand (swap_letters / assign_letter) when a word becomes recognisable.

Run on its own for a terminal demo:  python decrypt.py
"""

import string

from frequency import analyze_frequency, get_english_frequencies


def build_mapping(ciphertext):
    """
    Estimate a ciphertext-to-plaintext letter mapping.

    The most frequent ciphertext letter is matched with the most frequent
    English letter (E), the second most frequent with the second (T),
    and so on.

    Returns:
        A dictionary such as {"X": "E", "Q": "T", ...}, ordered from the
        most to the least frequent ciphertext letter. Only letters that
        appear in the ciphertext are included.
    """
    cipher_letters = [item["letter"] for item in analyze_frequency(ciphertext)]
    english_letters = [letter for letter, _ in get_english_frequencies()]

    return dict(zip(cipher_letters, english_letters))


def decrypt(ciphertext, mapping):
    """
    Replace each ciphertext letter using the given mapping.

    Spaces, digits and punctuation are kept as they are, and every letter
    keeps its original case. Letters that are not in the mapping are left
    unchanged.
    """
    result = []

    for char in ciphertext:
        upper = char.upper()

        if char in string.ascii_letters and upper in mapping:
            plain = mapping[upper]
            result.append(plain if char.isupper() else plain.lower())
        else:
            result.append(char)

    return "".join(result)


def _check_letter(value, name):
    """Return value as an uppercase A-Z letter, or raise ValueError."""
    letter = str(value).strip().upper()

    if len(letter) != 1 or letter not in string.ascii_uppercase:
        raise ValueError(f"{name} must be a single letter A-Z, got {value!r}")

    return letter


def swap_letters(mapping, first, second):
    """
    Manual refinement: swap two plaintext letters in the mapping.

    Example: if the output shows "TEH" where "THE" is expected,
    swap_letters(mapping, "E", "H") fixes both guesses at once.

    Returns a new dictionary; the original mapping is not changed.
    """
    first = _check_letter(first, "first")
    second = _check_letter(second, "second")

    new_mapping = {}

    for cipher, plain in mapping.items():
        if plain == first:
            new_mapping[cipher] = second
        elif plain == second:
            new_mapping[cipher] = first
        else:
            new_mapping[cipher] = plain

    return new_mapping


def assign_letter(mapping, cipher_letter, plain_letter):
    """
    Manual refinement: decide that one ciphertext letter means plain_letter.

    To keep the mapping one-to-one, the ciphertext letter that previously
    decrypted to plain_letter takes over cipher_letter's old guess.

    Returns a new dictionary; the original mapping is not changed.
    """
    cipher_letter = _check_letter(cipher_letter, "cipher_letter")
    plain_letter = _check_letter(plain_letter, "plain_letter")

    if cipher_letter not in mapping:
        raise ValueError(
            f"{cipher_letter} does not appear in the ciphertext"
        )

    new_mapping = dict(mapping)
    old_plain = new_mapping[cipher_letter]

    for other, plain in new_mapping.items():
        if plain == plain_letter and other != cipher_letter:
            new_mapping[other] = old_plain
            break

    new_mapping[cipher_letter] = plain_letter
    return new_mapping


def frequency_attack(ciphertext):
    """
    Run the full attack in one call (intended for the GUI).

    Returns:
        A dictionary with:
        - "frequencies": ciphertext letter statistics from analyze_frequency
        - "mapping": the estimated {cipher_letter: plain_letter} mapping
        - "plaintext": the approximate decryption
    """
    mapping = build_mapping(ciphertext)

    return {
        "frequencies": analyze_frequency(ciphertext),
        "mapping": mapping,
        "plaintext": decrypt(ciphertext, mapping),
    }


def _print_mapping(mapping):
    print("Cipher -> Plain")
    print("  ".join(f"{c}->{p}" for c, p in mapping.items()))


if __name__ == "__main__":
    ciphertext = input("Enter ciphertext: ")
    result = frequency_attack(ciphertext)
    mapping = result["mapping"]

    print("\nEstimated mapping (most frequent first):")
    _print_mapping(mapping)
    print("\nApproximate plaintext:")
    print(result["plaintext"])

    print(
        "\nRefine the mapping:"
        "\n  swap E H  -> swap plaintext letters E and H"
        "\n  set Q E   -> ciphertext letter Q decrypts to E"
        "\n  (press Enter to finish)"
    )

    while True:
        command = input("\n> ").strip().split()

        if not command:
            break

        try:
            if len(command) == 3 and command[0].lower() == "swap":
                mapping = swap_letters(mapping, command[1], command[2])
            elif len(command) == 3 and command[0].lower() == "set":
                mapping = assign_letter(mapping, command[1], command[2])
            else:
                print("Use 'swap E H' or 'set Q E'.")
                continue
        except ValueError as error:
            print(error)
            continue

        _print_mapping(mapping)
        print(decrypt(ciphertext, mapping))
