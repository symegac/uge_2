import os.path

# Config
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/")
DATA_FILE = "app_log.txt"
OUTPUT_DIR = os.path.join(DATA_DIR, "output/")
PRIORITY = ["WARNING", "ERROR"]

with open(os.path.join(DATA_DIR, DATA_FILE)) as file:
    raw_data = file.readlines()

for log_type in PRIORITY:
    with open(os.path.join(OUTPUT_DIR, f"{log_type.lower()}s.txt"), 'w', encoding="UTF-8") as file:
        for log in raw_data:
            if log_type in log:
                file.write(log)

# Alternativt, hvis man ved, at loggen altid har beskedtypen i tredje position:
#
# # for log in raw_data:
# #    msg_type = log.split(' ')[2]
# #    if msg_type in log_type:
# #        file.write(log)