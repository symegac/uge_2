import unittest
from opgave_3.src import fejlhåndtering as fh

valid_output = {
    "customer_id": 1,
    "name": "Jens Hansen",
    "email": "jens.hansen@gmail.com",
    "purchase_amount": 12.34
}

class TestFejlH(unittest.TestCase):
    def test_check_cols(self):
        valid_split = ["1", "Jens Hansen", "jens.hansen@gmail.com", "12.34"]

        # Streng med tre kommaer returnerer fire datafelter
        self.assertEqual(
            fh.check_cols(",,,"),
            ['', '', '', '']
        )
        self.assertEqual(
            fh.check_cols("1,Jens Hansen,jens.hansen@gmail.com,12.34"),
            valid_split
        )

        # Streng med for få/mange kommaer er ugyldig og returnerer None
        self.assertIsNone(fh.check_cols(",,"))
        self.assertIsNone(fh.check_cols(",,,,"))

        # Indledende ekstra komma fikses automatisk
        self.assertEqual(
            fh.check_cols(",1,Jens Hansen,jens.hansen@gmail.com,12.34"),
            valid_split
        )
        # Dobbeltkomma mellem to udfyldte datafelter fikses automatisk
        self.assertEqual(
            fh.check_cols("1,,Jens Hansen,,jens.hansen@gmail.com,,12.34"),
            valid_split
        )

        # Dobbeltkomma + tomt datafelt (dvs. trippeltkomma) bliver ikke rettet og returnerer None
        self.assertIsNone(fh.check_cols("1,Jens Hansen,,,12.34"))

    def test_check_id(self):
        # Et heltal er gyldigt kunde-id
        self.assertEqual(fh.check_id('1', line=1), 1)

        # Tomt kunde-id er ugyldigt og returnerer None
        self.assertIsNone(fh.check_id(''))
        # Kunde-id med bogstaver eller andre tegn end cifre er ugyldigt og returnerer None
        self.assertIsNone(fh.check_id("nan"))
        self.assertIsNone(fh.check_id("ABC123"))
        self.assertIsNone(fh.check_id("1.1"))
        # Negativt kunde-id er ugyldigt og returnerer None
        self.assertIsNone(fh.check_id("-123"))

        # Et ellers gyldigt kunde-id, der ikke står på rette plads i rækkefølgen,
        # er ugyldigt, da der er risiko for overskrivelse af andre data, og det returnerer None
        self.assertNotEqual(fh.check_id('1', line=2), 1)
        self.assertIsNone(fh.check_id('1', line=2))

    #TODO: Skriv test færdig
    def test_check_name(self):
        self.assertEqual(
            fh.check_name("Jens Hansen"),
            valid_output["name"]
        )
        # æøå +europæiske accenter også gyldige nu
        self.assertIsNotNone(fh.check_name("Ølla Trompetbakke"))
        self.assertIsNotNone(fh.check_name("Åge Kjærøe"))
        self.assertIsNotNone(fh.check_name("Frédéric Müller von Allgäu-Großebersdorf"))
        self.assertIsNotNone(fh.check_name("Lúcia Mouriño González-Örebro"))
        self.assertIsNotNone(fh.check_name("François d'Haÿ-les-Roses"))

    def test_check_email(self):
        self.assertEqual(
            fh.check_email("jens.hansen@gmail.com"),
            valid_output["email"]
        )

        self.assertIsNone(fh.check_email(''))

        # Emailadresser må kun indeholde ét @, den overordnede struktur skal holdes
        self.assertIsNone(fh.check_email("jens.hansen@@gmail.com"))
        self.assertIsNone(fh.check_email("jens.hans@en@gmail.com"))
        # Manglende @ før gmail.com, hotmail.com og yahoo.com fikses automatisk
        for domain in fh.known_domains:
            self.assertEqual(
                fh.check_email(f"jens.hansen{domain}"),
                f"jens.hansen@{domain}"
            )
        # Men andre domæner gør ikke
        self.assertIsNone(fh.check_email("jens.hansenexample.com"))

        # Manglende domæne
        self.assertIsNone(fh.check_email("jens.hansen@"))
        # Manglende lokaladresse
        self.assertIsNone(fh.check_email("@gmail.com"))
        # Ugyldigt domæne
        self.assertIsNone(fh.check_email("jens.hansen@gmailcom"))
        self.assertIsNone(fh.check_email("jens.hansen@gmail.c"))
        self.assertIsNone(fh.check_email("jens.hansen@gmail.c-o-m"))
        self.assertIsNone(fh.check_email("jens.hansen@gmail/com"))
        # Ugyldig lokaladresse
        self.assertIsNone(fh.check_email("jens/hansen@gmail.com"))

        # Duplikerede særlige tegn er ugyldige
        self.assertIsNone(fh.check_email("jens.hansen@gmail..com"))
        self.assertIsNone(fh.check_email("jens..hansen@gmail.com"))
        self.assertIsNone(fh.check_email("jens--hansen@gmail.com"))
        self.assertIsNone(fh.check_email("jens__hansen@gmail.com"))
        # Særlige tegn i start eller slut af email er ugyldige
        self.assertIsNone(fh.check_email("-jens.hansen@gmail.com_"))
        self.assertIsNone(fh.check_email("jens.hansen@gmail.com_"))
        self.assertIsNone(fh.check_email(".jens.hansen@gmail.com"))
        # Men særlige tegn i sig selv er gyldige
        self.assertIsNotNone(fh.check_email(r"jens-hansen_mail+test\%redir@g-m_ail.com"))

        # TODO: Mangler at tjekke for særlige tegn i starten af domæne og slutningen af lokaladresse
        # Disse tests fejler
        # self.assertIsNone(fh.check_email("jens.hansen@.gmail.com"))
        # self.assertIsNone(fh.check_email("jens.hansen.@gmail.com"))

    # TODO: Skriv test
    def test_check_amount(self):
        pass

    # TODO: Skriv test færdig
    def test_check_entry(self):
        self.assertEqual(
            fh.check_entry("1,Jens Hansen,jens.hansen@gmail.com,12.34", line=1),
            valid_output
        )

    def test_check_data(self):
        # Tom data er ugyldig
        self.assertIsNone(fh.check_data([]))
        self.assertIsNone(fh.check_data(''))
        self.assertIsNone(fh.check_data(' '))
        self.assertIsNone(fh.check_data(None))
        self.assertIsNone(fh.check_data(",,,"))

        # En dict er ikke gyldigt input
        self.assertIsNone(fh.check_data(valid_output))
        # En str er ikke gydligt input
        self.assertIsNone(fh.check_data("1,Jens Hansen,jens.hansen@gmail.com,12.34"))

        # Gyldigt input med og uden en header
        self.assertEqual(
            fh.check_data(["placeholderheader", "1,Jens Hansen,jens.hansen@gmail.com,12.34"], header=True),
            [valid_output]
        )
        self.assertEqual(
            fh.check_data(["1,Jens Hansen,jens.hansen@gmail.com,12.34"], header=False),
            [valid_output]
        )
        # Men fejler hvis omvendt
        self.assertIsNone(fh.check_data(["placeholderheader", "1,Jens Hansen,jens.hansen@gmail.com,12.34"], header=False))
        self.assertIsNone(fh.check_data(["1,Jens Hansen,jens.hansen@gmail.com,12.34"], header=True))

        # Flere rækker
        self.assertEqual(
            fh.check_data(
                [
                    "placeholderheader",
                    "1,Jens Hansen,jens.hansen@gmail.com,12.34",
                    "2,Ølla Trompetbakke,oella.trompetbakke@example.com,56.78"
                ],
                header=True
            ),
            [
                valid_output,
                {
                    "customer_id": 2,
                    "name": "Ølla Trompetbakke",
                    "email": "oella.trompetbakke@example.com",
                    "purchase_amount": 56.78
                }
            ]
        )

if __name__ == "__main__":
    unittest.main()
