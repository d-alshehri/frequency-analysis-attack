"""
Member 2 - Test data.

Sample plaintexts of different lengths, plus helpers to encrypt them with
a random monoalphabetic substitution key so the real answer is known.

Run on its own to print ready-made ciphertexts:  python samples.py
"""

import random
import string

from decrypt import decrypt


SHORT_TEXT = (
    "Meet me at the old library after the meeting and bring the secret notes."
)

MEDIUM_TEXT = (
    "Encryption is the process of turning a readable message into a form "
    "that only the intended reader can understand. For thousands of years, "
    "people have used simple methods to hide their words from enemies, "
    "rivals and curious neighbors. One of the oldest ideas is the "
    "substitution cipher, in which every letter of the alphabet is replaced "
    "by a different letter. At first glance the result looks like nonsense, "
    "and a casual reader would give up quickly. However, the hidden message "
    "still carries the fingerprints of the language it was written in. "
    "Common letters such as E, T and A appear again and again, while rare "
    "letters such as Q, X and Z hardly appear at all. A patient attacker can "
    "use these patterns to break the code."
)

LONG_TEXT = (
    "Long before computers existed, people relied on secret writing to "
    "protect letters, military orders and trade secrets. Kings, merchants "
    "and spies all needed a way to send information that would remain "
    "private even if the messenger was captured. The simplest solution was "
    "to swap each letter of the message for another letter, using a key that "
    "only the sender and the receiver knew. This kind of system is called a "
    "monoalphabetic substitution cipher, and for many centuries it was "
    "considered almost impossible to break.\n\n"
    "In the ninth century, the scholar Al-Kindi, who worked in Baghdad, "
    "wrote a book that changed the history of secret writing. He noticed "
    "that in any long piece of text some letters are used much more often "
    "than others. If a cipher only replaces each letter with a different "
    "symbol, those patterns do not disappear. They simply move to new "
    "symbols. By counting the symbols in a secret message and comparing the "
    "counts with the normal pattern of the language, a careful reader could "
    "start to guess which symbol stood for which letter. This idea is now "
    "known as frequency analysis, and it is one of the earliest examples of "
    "cryptanalysis.\n\n"
    "The method became famous in Europe many years later. In the sixteenth "
    "century, letters written in cipher by Mary, Queen of Scots, were "
    "intercepted and handed to an expert code breaker. By studying how often "
    "each symbol appeared, he was able to recover the hidden messages, which "
    "revealed a plot against Queen Elizabeth. The decrypted letters were "
    "used as evidence at her trial, and the result showed how dangerous it "
    "can be to trust a weak cipher.\n\n"
    "Frequency analysis works best when the message is long. A short note of "
    "one or two sentences may not contain enough letters for the usual "
    "pattern to appear, so the most common symbol might stand for T or A "
    "instead of E. Analysts therefore combine letter counts with other "
    "clues. They look for short words such as the, and, of and to, for "
    "repeated pairs of letters, and for words that make sense once a few "
    "letters are known. Each correct guess makes the next guess easier, "
    "until the whole message can be read.\n\n"
    "Today, the lesson of frequency analysis is still important for anyone "
    "who designs or uses security systems. A good cipher must hide every "
    "statistical pattern of the original data, not only the shape of the "
    "letters. Modern algorithms such as the Advanced Encryption Standard mix "
    "and transform the data many times, so the output looks random even "
    "when the input is a simple sentence repeated again and again. Learning "
    "how classical ciphers were broken helps students understand why these "
    "strong methods are necessary and why old techniques should never be "
    "used to protect real information."
)

SAMPLES = {
    "short": SHORT_TEXT,
    "medium": MEDIUM_TEXT,
    "long": LONG_TEXT,
}


def generate_key(seed=None):
    """
    Return a random substitution key such as {"A": "Q", "B": "M", ...}.

    Passing the same seed always gives the same key, so results can be
    repeated.
    """
    rng = random.Random(seed)
    shuffled = list(string.ascii_uppercase)
    rng.shuffle(shuffled)

    return dict(zip(string.ascii_uppercase, shuffled))


def invert_key(key):
    """Return the real decryption key: {cipher_letter: plain_letter}."""
    return {cipher: plain for plain, cipher in key.items()}


def encrypt(plaintext, key):
    """
    Encrypt with a monoalphabetic substitution key.

    Substitution encryption is the same letter-replacement operation as
    decryption, just with the real key, so decrypt() is reused here.
    """
    return decrypt(plaintext, key)


if __name__ == "__main__":
    key = generate_key(seed=7)

    for name, text in SAMPLES.items():
        print(f"===== {name.upper()} sample ciphertext =====")
        print(encrypt(text, key).replace("\n\n", " "))
        print()
