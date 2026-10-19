#to test frequency.py functions

import unittest

from frequency import (
    count_letters,
    calculate_percentages,
    analyze_frequency,
    get_english_frequencies
)


class TestFrequencyAnalysis(unittest.TestCase):

    def test_count_letters(self):
        counts = count_letters("ABBA CAB")

        self.assertEqual(counts["A"], 3)
        self.assertEqual(counts["B"], 3)
        self.assertEqual(counts["C"], 1)

    def test_percentages(self):
        percentages = calculate_percentages(
            count_letters("ABBA CAB")
        )

        self.assertAlmostEqual(percentages["A"], 300 / 7)
        self.assertAlmostEqual(percentages["C"], 100 / 7)

    def test_sorting(self):
        results = analyze_frequency("ABBA CAB")

        self.assertEqual(
            [item["letter"] for item in results],
            ["A", "B", "C"]
        )

    def test_empty_text(self):
        self.assertEqual(analyze_frequency("123 !?"), [])

    def test_english_reference(self):
        frequencies = get_english_frequencies()

        self.assertEqual(len(frequencies), 26)
        self.assertEqual(frequencies[0][0], "E")

        values = [value for _, value in frequencies]
        self.assertEqual(values, sorted(values, reverse=True))


if __name__ == "__main__":
    unittest.main()

#use python -m unittest -v test_frequency.py to test