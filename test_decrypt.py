# to test decrypt.py, samples.py and evaluate.py functions

import unittest

from decrypt import (
    build_mapping,
    decrypt,
    swap_letters,
    assign_letter,
    frequency_attack
)
from samples import SAMPLES, encrypt, generate_key, invert_key
from evaluate import letter_accuracy, mapping_accuracy, attack_accuracy


class TestMapping(unittest.TestCase):

    def test_matches_frequency_order(self):
        # X appears most, then Q, then Z -> E, T, A
        mapping = build_mapping("XXXX QQQ ZZ")

        self.assertEqual(mapping, {"X": "E", "Q": "T", "Z": "A"})

    def test_one_to_one(self):
        mapping = build_mapping(SAMPLES["long"])

        self.assertEqual(len(set(mapping.values())), len(mapping))

    def test_only_letters_in_ciphertext(self):
        mapping = build_mapping("Abc, abc! 123")

        self.assertEqual(set(mapping), {"A", "B", "C"})

    def test_empty_ciphertext(self):
        self.assertEqual(build_mapping("123 !?"), {})


class TestDecrypt(unittest.TestCase):

    def test_keeps_spaces_and_punctuation(self):
        mapping = {"X": "H", "Q": "I", "Z": "A"}

        self.assertEqual(decrypt("Xq, z!", mapping), "Hi, a!")

    def test_keeps_case(self):
        mapping = {"X": "H", "Q": "I"}

        self.assertEqual(decrypt("XQ xq Xq", mapping), "HI hi Hi")

    def test_unmapped_letters_unchanged(self):
        self.assertEqual(decrypt("abc", {"A": "Z"}), "zbc")

    def test_true_key_recovers_plaintext(self):
        key = generate_key(seed=42)
        ciphertext = encrypt(SAMPLES["medium"], key)

        self.assertNotEqual(ciphertext, SAMPLES["medium"])
        self.assertEqual(
            decrypt(ciphertext, invert_key(key)),
            SAMPLES["medium"]
        )


class TestManualRefinement(unittest.TestCase):

    def setUp(self):
        self.mapping = {"X": "E", "Q": "T", "Z": "A"}

    def test_swap_letters(self):
        swapped = swap_letters(self.mapping, "E", "T")

        self.assertEqual(swapped, {"X": "T", "Q": "E", "Z": "A"})

    def test_swap_does_not_change_original(self):
        swap_letters(self.mapping, "E", "T")

        self.assertEqual(self.mapping, {"X": "E", "Q": "T", "Z": "A"})

    def test_assign_letter_keeps_one_to_one(self):
        updated = assign_letter(self.mapping, "Z", "E")

        self.assertEqual(updated, {"X": "A", "Q": "T", "Z": "E"})

    def test_assign_unused_letter(self):
        updated = assign_letter(self.mapping, "Q", "h")

        self.assertEqual(updated, {"X": "E", "Q": "H", "Z": "A"})

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            assign_letter(self.mapping, "B", "E")   # B not in ciphertext
        with self.assertRaises(ValueError):
            swap_letters(self.mapping, "E", "12")
        with self.assertRaises(ValueError):
            assign_letter(self.mapping, "X", "")


class TestFullAttack(unittest.TestCase):

    def test_frequency_attack_output(self):
        ciphertext = encrypt(SAMPLES["short"], generate_key(seed=3))
        result = frequency_attack(ciphertext)

        self.assertEqual(
            set(result),
            {"frequencies", "mapping", "plaintext"}
        )
        self.assertEqual(
            result["plaintext"],
            decrypt(ciphertext, result["mapping"])
        )
        self.assertEqual(len(result["plaintext"]), len(ciphertext))

    def test_accuracy_functions(self):
        self.assertEqual(letter_accuracy("Hello!", "Hello!"), 100)
        self.assertEqual(letter_accuracy("ab", "aX"), 50)

        key = generate_key(seed=5)
        self.assertEqual(mapping_accuracy(invert_key(key), key), 100)

    def test_long_text_beats_short_text(self):
        _, short_accuracy = attack_accuracy(SAMPLES["short"][:30], seed=1)
        _, long_accuracy = attack_accuracy(SAMPLES["long"], seed=1)

        self.assertGreater(long_accuracy, short_accuracy)


if __name__ == "__main__":
    unittest.main()

# use python -m unittest -v test_decrypt.py to test
