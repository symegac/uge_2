import unittest
from opgave_3.src import fejlhåndtering as fh

valid_output = {
    "id": 1,
    "name": "Jens Hansen",
    "email": "jens.hansen@gmail.com",
    "purchase_amount": 12.34
}

class TestCase(unittest.TestCase):
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
        self.assertEqual(fh.check_id('1', 1), 1)

        # Tomt kunde-id er ugyldigt og returnerer None
        self.assertIsNone(fh.check_id(''))
        # Kunde-id med bogstaver eller andre tegn end cifre er ugyldigt og returnerer None
        self.assertIsNone(fh.check_id("nan"))
        self.assertIsNone(fh.check_id("ABC123"))
        self.assertIsNone(fh.check_id("1.1"))
        # Negativt kunde-id er ugyldigt og returnerer None
        self.assertIsNone(fh.check_id("-123"))

        # Et ellers gyldigt kunde-id, der ikke står på rette plads i rækkefølgen,
        # er ugyldigt, da der er risiko for overskrivelse af andre data og returnerer None
        self.assertNotEqual(fh.check_id('1', 2), 1)
        self.assertIsNone(fh.check_id('1', 2))

    def test_check_name(self):
        pass

    def test_check_email(self):
        pass

    def test_check_amount(self):
        pass

    def test_check_data(self):
        pass

if __name__ == "__main__":
    unittest.main()