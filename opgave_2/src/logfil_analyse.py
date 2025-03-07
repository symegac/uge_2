import os.path

# Konfiguration
data_dir = os.path.join(os.path.dirname(__file__), "../data/")
data_file = "app_log.txt"
output_dir = os.path.join(data_dir, "output/")
log_types = ["WARNING", "ERROR"]

with open(os.path.join(data_dir, data_file)) as file:
    raw_data = file.readlines()

for log_type in log_types:
    with open(os.path.join(output_dir, f"{log_type.lower()}s.txt"), 'w', encoding="UTF-8") as file:
        for log in raw_data:
            if log_type in log:
                file.write(log)

# Alternativt, hvis man ved, at loggen altid har beskedtypen i tredje position:
#
# # for log in raw_data:
# #    msg_type = log.split(' ')[2]
# #    if msg_type in log_type:
# #        file.write(log)
