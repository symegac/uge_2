import os.path
import matplotlib.pyplot as plt
from collections import Counter

# Konfiguration
data_dir = os.path.join(os.path.dirname(__file__), "../data/")
data_file = "Navne_liste.txt"

# Åbner fil med navneliste (bruger readline, da der kun er én linje)
with open(os.path.join(data_dir, data_file), "r", encoding="utf-8") as file:
    raw_input = file.readline()

# Sorterer liste alfabetisk og derefter efter længde
sorted_names = sorted(raw_input.split(','), key=lambda x: (x, len(x)))

# En counter er den mest pythoniske måde at tælle på
letter_counter = Counter()
for name in sorted_names:
    for letter in name.lower():
        letter_counter[letter] += 1

# AVANCERET UDVIDELSE
# Sorterer counter alfabetisk
sorted_letter_counter = dict(sorted(letter_counter.items(), key=lambda x: x[0]))
# Sorterer efter frekvens (zip for at gå fra [(k0, v0), (k1, v1), ...] til [(k0, k1, ...), (v0, v1, ...)], som lettere kan inputtes i matplotlib)
most_frequent_letters = list(zip(*letter_counter.most_common()))

# Laver to subplots i Matplotlib
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("Frequency of letters in names")

# Første plot viser distributionen
plt.subplot(121)
plt.title("Distribution", size="medium")
bar_chart = plt.bar(sorted_letter_counter.keys(), sorted_letter_counter.values())
plt.bar_label(bar_chart, sorted_letter_counter.values(), size="x-small")
plt.xlabel("Letter")
plt.ylabel("No. of occurrences")

# Andet plot sorterer efter mest frekvente bogstav
plt.subplot(122)
plt.title("Most frequent letters", size="medium")
barh_chart = plt.barh(most_frequent_letters[0], most_frequent_letters[1])
plt.bar_label(barh_chart, most_frequent_letters[1], size="x-small")
plt.xlabel("No. of occurrences")
plt.ylabel("Letter")
ax2.invert_yaxis()

plt.show()
