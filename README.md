# SPAC Uge 2
## Setup (CLI)
1. Start med at hente en kopi af projektet (sørg for at være det sted i filsystemet, hvor du vil gemme projektet)
> git clone https://github.com/symegac/uge_2.git
2. Naviger til den nye mappe og lav et virtuelt miljø:
> cd uge_2
>
> py -m venv .venv
3. Aktivér miljøet i din foretrukne shell, her bash som eksempel (kør .bat-filen i samme mappe hvis cmd eller .ps1-filen hvis powershell):
> source .venv/Scripts/activate
4. Installér så dependencies:
> pip install -r requirements.txt
5. Nu er du klar til at køre Python-filerne!

## Generelt
Jeg synes jeg kom til at lave meget mere på nogle af opgaverne, end jeg egentlig havde behøvet, hvilket gik ud over den tid, jeg havde til overs til resten af opgaverne. Men det var heldigvis meget lærerigt.
Jeg ved ikke om jeg kan komme med nogle specifikke ord på, hvad jeg helst vil have feedback på. Men alle råd om, hvad der kan forbedres, tager jeg glædeligt imod. F.eks. manglen af <code>if __name__ == "__main__"</code> i nogle af filerne og newline i slutningen af filer.

## Opgaver
### Opgave 1
> py opgave_1/src/navnesortering.py

En rimelig enkel opgave, hvor man sorterer en liste af navne og derefter tæller antallet af bogstaver.
Den avancerede udvidelse var der lidt mere udfordring i, da jeg skulle lære Matplotlib for første gang. Der er næsten alt for mange måder at gøre de samme ting på! Men jeg fik lavet nogle grafer, der kan ses [her](opgave_1/data/output/bar_plots.png).

### Opgave 2
> py opgave_2/src/logfil_analyse.py

Denne opgave var også ret ligetil. Jeg fik sendt alle advarsler og fejl til hhv. [warnings.txt](opgave_2/data/output/warnings.txt) og [errors.txt](opgave_2/data/output/errors.txt).

### Opgave 3
> py opgave_3/src/fejlhåndtering.py

Denne opgave var i teorien ikke så svær, da man egentlig kun skulle læse/skrive og tjekke, om en række data var gyldig med try/except.
Men da man skulle prøve at lave så deskriptive fejlbeskeder som muligt, voksede projektet hurtigt, da der var så mange forskellige typer fejl i datasættet at differentiere mellem. Så der er en masse kode, der ikke er blevet optimeret og refaktoriseret, fordi jeg blev ved med at skrive om.

Jeg fik endda lavet et halvt testmodul, for at tjekke om mine funktioner for hvert datafelt kunne klare de forskellige typer fejl korrekt. Men det var kun to tests, jeg fik skrevet i sidste ende.
For at køre testmodulet:
> py -m opgave_3.tests.test_fejlhåndtering

### Opgave 4
> py opgave_4/src/pandas_intro.py

Det tog lidt tid at omstille sig til måden Pandas gjorde tingene på ift. SQL, men det var ikke så slemt, og de fleste af delopgaverne kunne klares på en linje.

I opgave 3.4 brugte jeg alt for lang tid på at finde rundt i Pandas og Matplotlib for at justere udseendet af grafen. Der er alt for mange måder at indstille de samme ting på, så man bliver helt forvirret. Men så er der nogle gange også noget, som kun kan justeres på én måde, som kan tage en evighed at finde frem til i dokumentationen, f.eks. kursivering af ticklabels. Men [grafen](opgave_4/data/output/bar_plot.png) blev heldigvis ret flot til sidst, så det hårde arbejde betalte sig.

### Supplerende opgave
> py suppl_opgave/northwind.py

(Lige i denne opgave har jeg ikke fået lavet data-src-tests-strukturen af en eller anden grund)

Den ekstra opgave var ret svær for mig at komme i gang med, da jeg ikke kendte adgangskoden til MySql. Jeg måtte [nulstille koden](https://dev.mysql.com/doc/refman/8.4/en/resetting-permissions.html) for at få det til at virke.

Det var lidt svært at finde rundt i Workbench i starten, men jeg fik importeret databasen gennem SQL-scriptet og fik også bygget et diagram i Workbench, som kan tilgås [her](suppl_opgave/suppl_opg_2.1.pdf).

Jeg kendte allerede lidt til SQL, så det gik rimelig godt med at få skrevet de forskellige queries. Der var dog to af dem, som ikke syntes at give samme antal rækker som i opgavebeskrivelsens facit. Min SQL-fil kan findes [her](suppl_opgave/uge3_opgave4.sql).

Jeg syntes det var meget mere intuitivt at lave selve analysen direkte i SQL-queriet end at udtrække nogle data med SQL og så analysere med Pandas. Men det var da meget lærerigt, da man skulle lære nogle nye ting i Pandas, f.eks. pendanten til SQL's <code> SELECT (col1 * col2) AS col3</code>.

Der var rigtigt nok mange fejl i databasen, som vi fik at vide. De primære var, at ikke-ASCII-tegn var forsvundet, og at apostroffer var blevet til bindestreger i den ene tabel. En liste over fejl, som jeg fandt kan findes [her](suppl_opgave/Fejl%20i%20Northwind-data.txt).