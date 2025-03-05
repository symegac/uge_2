import os.path
import matplotlib
from collections import Counter

# Config
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/")
DATA_FILE = "Navne_liste.txt"

with open(os.path.join(DATA_DIR, DATA_FILE), "r", encoding="UTF-8") as file:
    raw_input = file.readline()
    
sorted_names = sorted(raw_input.split(','), key=lambda x: (x, len(x)))

letter_counter = Counter()
for name in sorted_names:
    for letter in name.lower():
        letter_counter[letter] += 1

if __name__ == "__main__":
    print(sorted_names)
    print(letter_counter)