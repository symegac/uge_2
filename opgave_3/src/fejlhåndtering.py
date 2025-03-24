import os.path
import re
import typing

# Konfiguration
data_dir = os.path.join(os.path.dirname(__file__), "../data/")
data_file = "source_data.csv"
output_dir = os.path.join(data_dir, "output/")
known_domains = ["gmail.com", "hotmail.com", "yahoo.com"]
terminal_log = False

# Logging
error_log = []

#TODO: Skal laves om til en enkelt str parameter i stedet for en bool for hver type besked
def print_error(
        message: str,
        line: int = -1,
        value: typing.Any = None,
        try_fix: bool = False,
        short: bool = False,
        io: bool = False
    ) -> None:
    if short:
        error_message = "    "
    elif io:
        error_message = "I/O FEJL "
    elif try_fix:
        error_message = f"Mulig fejl i række {line + 1}: "
    else:
        error_message = f"FEJL i række {line + 1}: "
    error_message += message
    if value is not None:
        value = value.strip()
        error_message += f" ({value=})"

    if terminal_log:
        print(error_message)
    error_log.append(error_message)

# I/O
def load_data(dir: str = data_dir, filename: str = data_file) -> list[str]:
    try:
        with open(os.path.join(dir, filename)) as file:
            raw_data = file.readlines()
    except FileNotFoundError:
        print_error("ved læsning af datafil: Den angivne datafil findes ikke.", io=True)
    except PermissionError:
        print_error("ved læsning af datafil: Filen er muligvis læsebeskyttet.", io=True)
    except:
        print_error("ved læsning af datafil: Ukendt fejl.", io=True)
    else:
        return raw_data

def save_data(entries: list[dict[str]] | list[str], dir: str = output_dir, filename: str = "output.csv", append: bool = False) -> None:
    try:
        with open(os.path.join(dir, filename), 'a' if append else 'w', encoding="utf-8") as file:
            for entry in entries:
                if isinstance(entry, dict):
                    entry = ','.join(str(value) for value in entry.values())
                file.write(entry + '\n')
    except FileNotFoundError:
        print_error("ved skrivning til output-fil: Den angivne fil eller filsti eksisterer ikke.", io=True)
    except PermissionError:
        print_error("ved skrivning til output-fil: Filen er muligvis skrivebeskyttet.", io=True)
    except TypeError:
        print_error("ved skrivning til output-fil: Datatypen kan ikke skrives til filen. Inputdata skal helst have en af følgende former: list[dict[str]] | list[str].", io=True)
    except:
        print_error("ved skrivning til output-fil: Ukendt fejl.", io=True)

# DATAVALIDERING
def check_cols(entry: str, line: int = -1, tried: bool = False) -> list[str] | None:
    split_entry = entry.split(',')
    # Forsøger at rette automatisk med dårlig rekursion
    if len(split_entry) != 4:
        if tried:
            print_error("Kunne IKKE fikse!", short=True)
            print_error("Der er for få/mange kommaer i rækken.", line, entry)
            return
        print_error("Der er for få/mange kommaer i rækken. Forsøger at fikse...", line, entry, True)

        # Fjerner dobbeltkomma mellem to ellers angivne datafelter
        new_entry = re.sub(r"(?<=[\w\d.-]),{2}(?=[\w\d.-])", ',', entry)
        # Fjerner begyndende komma, hvis et ciffer mellem 0 og 9 følger (dvs. et kunde-id) 
        if re.match(r"^,\d+", new_entry):
            new_entry = new_entry[1:]

        # Tjekker tilrettet streng
        new_entry = check_cols(new_entry, line, True)
        if new_entry is None:
            return
        split_entry = new_entry
        print_error("FIKSET!", short=True)

    return split_entry

def check_id(customer_id: str, line: int = -1) -> int | None:
    # Tjekker om feltet 'customer_id' er tomt
    # Kunne måske løses ved at sige customer_id = line, med det er farligt at gætte værdien af 'customer_id', da det er primary key
    if not customer_id:
        print_error("Der er intet kunde-id angivet.", line)
        return
    # Tjekker om 'customer_id' indeholder andre tegn end cifre (f.eks. "nan", "ABC123", "1.1", "-123")
    if not customer_id.isdigit():
        if customer_id[0] == '-' and customer_id[1:].isdigit():
            print_error("Kunde-id'et er negativt.", line, customer_id)
            return
        print_error("Kunde-id'et indeholder et eller flere ugyldige tegn.", line, customer_id)
        return
    # Tjekker om 'customer_id' står på den korrekte plads (og for en sikkerheds skyld om id'et er et heltal)
    try:
        if int(customer_id) != line:
            print_error("Kunde-id'et svarer ikke til placeringen i listen, muligvis en dublet der kan overskrive data.", line, customer_id)
            return
    except (TypeError, ValueError):
        print_error("Ugyldigt kunde-id angivet.", line, customer_id)
        return

    return int(customer_id)

def check_name(name: str, line: int = -1) -> str | None:
    # Tjekker om feltet 'name' er tomt
    if not name:
        print_error("Intet navn angivet.", line)
        return
    # Tjekker om 'name' indeholder andre tegn end bogstaver, mellemrum og bindestreger
    if re.search(r"[^A-zÀ-ÿ'\-\ ]", name):
        print_error("Kundenavnet indeholder ugyldige tegn.", line, name)
        return
    # TODO: 
    # Tjek for "Dr., Mr., Mrs., Ms." etc. (samme i email, da denne måske er genereret ud fra de to første ord i navnet)
    # Også efterstillede titler som "MD, PhD, DVM" etc.
        # Disse hører ikke til navnet
    # Også efterstillet "Jr., Sr., II, III" etc.
        # Disse er dog en faktisk del af navnet
    # Også om alle ord i navnet starter med en majuskel, da nogle af de gyldige navne er fuldt lowercase
        # Pas dog på med "van, von, d', l', de, da, di, do, den, van der, van den, de la, ter" o.lign.
        # Der er også navne som https://en.wikipedia.org/wiki/Jacob_deGrom, https://en.wikipedia.org/wiki/Charles_ffoulkes og https://en.wikipedia.org/wiki/Richard_ffrench-Constant
        # Og Ramund hin Unge, Leif den Lykkelige (Leifur heppni Eiríksson), Erik den Røde (Eiríkur rauði Þorvaldsson)
        # Cees 't Hart, tidligere direktør i Carlsberg
        # Der er en grund til at det er lettere bare at have efternavne som all caps
        # https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
        # Det er lettere bare at lade være

    return name

def check_email(email: str, line: int = -1, tried: bool = False) -> str | None:
    # Tjekker om feltet 'email' er tomt
    if not email:
        print_error("Ingen emailadresse angivet.", line)
        return
    # Tjekker om emailadressen har et ugyldigt navn og specificerer typiske fejl
    if not re.match(r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}$", email):
        if tried:
            print_error("Kunne IKKE fikse!", short=True)
            print_error("Emailadressen indeholder intet @.", line, email)
            return
        # Forsøger at autorette manglende @ med dårlig rekursion, burde udskilles til ny funktion
        if '@' not in email:
            print_error("Emailadressen indeholder intet @. Forsøger at fikse...", line, email, True)
            for domain in known_domains:
                if email.endswith(domain):
                    new_email = email[:-len(domain)] + '@' + email[-len(domain):]
                    new_email = check_email(new_email, line, True)
                    if new_email is not None:
                        print_error("FIKSET!", short=True)
                        return new_email
            else:
                print_error("Emailadressen indeholder intet @.", line, email)
                return
        if email.endswith('@'):
            print_error("Emailadressen mangler et domæne efter @.", line, email)
            return
        if email.startswith('@'):
            print_error("Emailadressen mangler en lokal adresse før @.", line, email)
            return
        if not re.match(r"^[A-z0-9._%+-]+@", email):
            print_error("Emailadressen har en ugyldig lokal adresse før @.", line, email)
            return
        if not re.search(r"@[A-z0-9.-]+\.[A-z]{2,}$", email):
            print_error("Emailadressen har et ugyldigt domæne efter @.", line, email)
            return
        print_error("Emailadressen er muligvis ugyldig", line, email)
        return
    # Tjekker for andre ting, der ikke er gyldige i en emailadresse
    if re.search(r"[._-]{2,}", email):
        print_error("Emailadressen er ugyldig, da den indeholder duplikerede særlige tegn.", line, email)
        return
    if re.search(r"^[._-]", email) or re.search(r"[._-]$", email):
        print_error("Emailadressen er ugyldig, da den begynder eller slutter på et særligt tegn.", line, email)
        return

    return email

def check_amount(purchase_amount: str, line: int = -1) -> float | None:
    # Tjekker om feltet 'purchase_amount' er tomt
    if not purchase_amount:
        print_error("Intet beløb angivet.", line)
        return
    # Tjekker om 'purchase_amount' er et tal
    try:
        amount = float(purchase_amount)
    except (TypeError, ValueError):
        print_error("Ugyldigt beløb angivet.", line, purchase_amount)
        return
    # Tjekker om 'purchase_amount' er positivt
    if amount < 0:
        print_error("Beløbet må ikke være negativt", line, purchase_amount)
        return

    return amount

def check_entry(entry: str, line: int) -> dict[str] | None:
    # Tjekker om rækken består af 4 datafelter (dvs. indeholder 3 kommaer)
    split_entry = check_cols(entry, line)
    if split_entry is None:
        return

    # Tjekker om kunde-id'et er gyldigt
    customer_id = check_id(split_entry[0].strip(), line)
    if customer_id is None:
        return

    # Tjekker om navnet er gyldigt
    name = check_name(split_entry[1].strip(), line)
    if name is None:
        return

    # Tjekker om emailadressen er gyldig
    email = check_email(split_entry[2].strip(), line)
    if email is None:
        return

    # Tjekker om beløbet er gyldigt
    purchase_amount = check_amount(split_entry[3].strip(), line)
    if purchase_amount is None:
        return

    valid_entry = {
        "customer_id": customer_id,
        "name": name,
        "email": email,
        "purchase_amount": purchase_amount
    }
    return valid_entry

def check_data(data: list[str], header: bool = True) -> list[dict[str]] | None:
    valid_entries = []

    # Tjekker om der er data i datasættet
    if not data:
        print_error("Det angivne datasæt indeholder ingen data.", io=True)
        return

    for line, entry in enumerate(data):
        # Springer over header
        if header and line == 0:
            continue

        checked_entry = check_entry(entry, line if header else line + 1)
        if checked_entry is None:
            continue

        # De tilbageværende entries burde være gyldige og kan indsættes i en liste,
        # der kan bruges til at skrive til output-filen.
        # Man kunne også bare bruge ','.join() i stedet for at lave en dict, som alligevel laves om til en csv-streng
        valid_entries.append(checked_entry)

    return valid_entries if valid_entries else None

if __name__ == "__main__":
    raw_data = load_data()
    result = check_data(raw_data)
    print(f"Gyldige rækker: {len(result)}")
    save_data(result)
    save_data(error_log, filename="log.txt")
