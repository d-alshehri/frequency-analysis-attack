
from frequency import analyze_frequency, get_english_frequencies

ciphertext = input("Enter ciphertext: ")

print("\nCiphertext frequency analysis")
print("-" * 42)
print(f"{'Letter':<10}{'Count':<10}{'Percentage':>12}")

for item in analyze_frequency(ciphertext):
    print(
        f"{item['letter']:<10}"
        f"{item['count']:<10}"
        f"{item['percentage']:>11.2f}%"
    )

print("\nTop English reference letters:")
for letter, percentage in get_english_frequencies()[:5]:
    print(f"{letter}: {percentage:.2f}%")
