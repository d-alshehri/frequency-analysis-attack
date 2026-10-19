# Approximate English letter frequencies (percentages).
ENGLISH_FREQUENCIES = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25,
    "E": 12.70, "F": 2.23, "G": 2.02, "H": 6.09,
    "I": 6.97, "J": 0.15, "K": 0.77, "L": 4.03,
    "M": 2.41, "N": 6.75, "O": 7.51, "P": 1.93,
    "Q": 0.10, "R": 5.99, "S": 6.33, "T": 9.06,
    "U": 2.76, "V": 0.98, "W": 2.36, "X": 0.15,
    "Y": 1.97, "Z": 0.07
}

#this code stores percentege for every letter, it uses sorted to order letters from most to least frequent, and it returns list of letter-percentage
def get_english_frequencies():
    """Return English letters sorted by reference frequency."""
    return sorted(
        ENGLISH_FREQUENCIES.items(),
        key=lambda item: item[1],
        reverse=True
    )


#s
from collections import Counter
import string


def count_letters(text):
    """Count alphabetic letters A-Z, ignoring case."""
    text = text.upper()

    return Counter(
        char for char in text
        if char in string.ascii_uppercase
    )


def calculate_percentages(counts):
    """Calculate each letter's percentage among all letters."""
    total = sum(counts.values())

    if total == 0:
        return {}

    return {
        letter: count / total * 100
        for letter, count in counts.items()
    }


def analyze_frequency(ciphertext):
    """
    Analyze ciphertext and return sorted letter statistics.

    Returns:
        A list of dictionaries containing:
        letter, count, and percentage.
    """
    counts = count_letters(ciphertext)
    percentages = calculate_percentages(counts)

    results = [
        {
            "letter": letter,
            "count": count,
            "percentage": percentages[letter]
        }
        for letter, count in counts.items()
    ]

    results.sort(
        key=lambda item: (-item["count"], item["letter"])
    )

    return results


def get_english_frequencies():
    """Return English reference frequencies in descending order."""
    return sorted(
        ENGLISH_FREQUENCIES.items(),
        key=lambda item: item[1],
        reverse=True
    )
