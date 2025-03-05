import os.path
import re
import typing

# Konfiguration
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/")
SOURCE_FILE = "source_data.csv"
OUTPUT_DIR = os.path.join(DATA_DIR, "output/")
DOMAINS = ["gmail.com", "hotmail.com", "yahoo.com"]

error_log = []

def print_error(line: int, message: str, value: typing.Any = None) -> None:
    error_message = f"FEJL i række {line + 1}: {message}{f" ({value=})" if value else ""}"
    print(error_message)
    error_log.append(error_message)

def check_cols(entry: list, line: int, tried: bool = False) -> list[str] | None:
    split_entry = entry.split(',')
    # Tjekker om er langt nok
    if len(split_entry) != 4:
        if tried:
            print("    Kunne IKKE fikse!")
            print_error(line, "Der er for mange kommaer i rækken.", entry)
            return
        print(f"Mulig fejl i række {line + 1}: Der er for mange kommaer i rækken. Forsøger at fikse...")
        new_entry = re.sub(",+", ',', entry)
        check_cols(new_entry, line, True)

    if tried:
        print("    Fikset!")
    return split_entry

def check_id(customer_id: str, line: int) -> int | None:
    # Tjekker om feltet 'customer_id' er tomt
    if not customer_id:
        print_error(line, "Der er intet kunde-id angivet.")
        customer_id = line
        return
    # Tjekker om 'customer_id' indeholder bogstaver (f.eks. 'nan')
    if customer_id.isalpha():
        print_error(line, "Kunde-id'et indeholder et eller flere bogstaver.", customer_id)
        return
    # Tjekker om 'customer_id' står på den korrekte plads
    try:
        if int(customer_id) != line:
            if customer_id[0] == '-':
                print_error(line, "Kunde-id'et er negativt.", customer_id)
                return
            print_error(line, "Kunde-id'et svarer ikke til placeringen i listen, muligvis en dublet der kan overskrive data.", customer_id)
            return
    except (TypeError, ValueError):
        print_error(line, "Ugyldigt kunde-id angivet.", customer_id)
        return

    return int(customer_id)

def check_name(name: str, line: int) -> str | None:
    # Tjekker om feltet 'name' er tomt
    if not name:
        print_error(line, "Intet navn angivet.")
        return
    # Tjekker om 'name' indeholder andre tegn end bogstaver, mellemrum og bindestreger
    if re.search(r"[^A-Za-z\-\ ]", name):
        print_error(line, "Kundenavnet indeholder ugyldige tegn.", name)
        return
    # TODO: Tjek for "Dr., Mr., Mrs., Ms." etc. (samme i email, da denne måske er genereret ud fra de to første ord i navnet)
    # Også efterstillede titler som "MD, PhD, DVM" etc.
    # Også om alle ord i navnet starter med en majuskel (pas dog på med "van, von" o.lign.)

    return name

def check_email(email: str, line, tried: bool = False) -> str | None:
    # Tjekker om feltet 'email' er tomt
    if not email:
        print_error(line, "Ingen emailadresse angivet.")
        return
    # Tjekker om emailadressen har et ugyldigt navn og specificerer typiske fejl
    if not re.match(r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}$", email):
        if tried:
            print("    Kunne IKKE fikse!")
            print_error(line, "Emailadressen indeholder intet @.", email)
            return
        if '@' not in email:
            print(f"Mulig fejl i række {line + 1}. Emailadressen indeholder intet @. Forsøger at fikse... value='{email}'")
            for domain in DOMAINS:
                if email.endswith(domain):
                    new_email = email[:-len(domain)] + '@' + email[-len(domain):]
                    new_email = check_email(new_email, line, True)
                    if new_email is not None:
                        return new_email
            else:
                print_error(line, "Emailadressen indeholder intet @.", email)
                return
        if email.endswith('@'):
            print_error(line, "Emailadressen mangler et domæne efter @.", email)
            return
        if email.startswith('@'):
            print_error(line, "Emailadressen mangler en lokal adresse før @.", email)
            return
        if not re.match(r"^[A-z0-9._%+-]+@", email):
            print_error(line, "Emailadressen har en ugyldig lokal adresse før @.", email)
            return
        if not re.search(r"@[A-z0-9.-]+\.[A-z]{2,}$", email):
            print_error(line, "Emailadressen har et ugyldigt domæne efter @.", email)
            return
        print_error(line, "Emailadressen er muligvis ugyldig", email)
        return
    # Tjekker for andre ting, der ikke er gyldige i en emailadresse
    if re.search(r"[._-]{2,}", email):
        print_error(line, "Emailadressen er ugyldig, da den indeholder duplikerede særlige tegn.", email)
        return
    if re.search(r"^[._-]", email) or re.search(r"[._-]$", email):
        print_error(line, "Emailadressen er ugyldig, da den begynder eller slutter på et særligt tegn.", email)
        return

    if tried:
        print("    Fikset!")
    return email

def check_amount(purchase_amount: str, line: int) -> float | None:
    # Tjekker om feltet 'purchase_amount' er tomt
    if not purchase_amount:
        print_error(line, "Intet beløb angivet.")
        return
    # Tjekker om 'purchase_amount' er et tal
    try:
        amount = float(purchase_amount)
    except (TypeError, ValueError):
        print_error(line, "Ugyldigt beløb angivet.", purchase_amount)
        return
    if amount < 0:
        print_error(line, "Beløbet må ikke være negativt", purchase_amount)
        return

    return float(purchase_amount)

def check_data(dir: str = DATA_DIR, filename: str = SOURCE_FILE) -> list[dict[str]]:
    try:
        with open(os.path.join(dir, filename)) as file:
            raw_data = file.readlines()
    except FileNotFoundError:
        print("Den angivne datafil findes ikke.")
        return

    valid_entries = []

    for line, entry in enumerate(raw_data):
        # Springer over header
        if line == 0:
            continue

        # Tjekker om rækken består af 4 datafelter (dvs. indeholder 3 kommaer)
        split_entry = check_cols(entry, line)
        if split_entry is None:
            continue

        customer_id = check_id(split_entry[0].strip(), line)
        if customer_id is None:
            continue

        name = check_name(split_entry[1].strip(), line)
        if name is None:
            continue

        email = check_email(split_entry[2].strip(), line)
        if email is None:
            continue

        purchase_amount = check_amount(split_entry[3].strip(), line)
        if purchase_amount is None:
            continue

        # De tilbageværende entries burde være valide og kan indsættes i en liste,
        # der kan bruges til at skrive til output-filen
        valid_entries.append({
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "purchase_amount": purchase_amount
        })
    
    return valid_entries

def save_data(entries: list[dict[str]] | list[str], dir: str = OUTPUT_DIR, filename: str = "output.csv", append: bool = False) -> None:
    try:
        with open(os.path.join(dir, filename), "a" if append else "w", encoding="UTF-8") as file:
            for entry in entries:
                if isinstance(entry, dict):
                    entry = ','.join(str(value) for value in entry.values())
                try:
                    file.write(entry + '\n')
                except:
                    print("Fejl ved skrivning til output-fil. Filen er muligvis skrivebeskyttet.")
    except FileNotFoundError:
        print("Fejl ved skrivning til output-fil. Den angivne fil eller filsti eksisterer ikke.")

if __name__ == "__main__":
    result = check_data()
    print(f"Valid entries: {len(result)}")
    save_data(result)
    save_data(error_log, filename="log.txt")