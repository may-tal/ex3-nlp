import unittest
import translator_date
import arrow

class TranslatorTest(unittest.TestCase):

    def setUp(self):
        self.translator = translator_date.DateTranslator()
        self.translator_specific = translator_date.DateTranslator("20200219")
        self.arr = arrow.utcnow().to("Israel")
        self.arr_specific = arrow.get(2020, 2, 19)

    def test_before(self):
        self._test_all("בעוד")

    def test_after(self):
        self._test_all("לפני")

    def test_today(self):
        self._single_run(0, 0, 0, "היום.", 1)

    def test_yesterday(self):
        self._single_run(1, 0, 0, "אתמול.", -1)

    def test_tomorrow(self):
        self._single_run(1, 0, 0, "מחר.", 1)


    def _test_all(self, before_after):
        pos_or_neg = 1 if before_after == "בעוד" else -1
        for i in range(1,32):
            for j in range(1, 13):
                for k in range(1, 13):
                    phrase = before_after
                    phrase += " " + \
                              self._return_num_as_string(i) + " ימים ו" + \
                              self._return_num_as_string(j) + " שבועות ו" + \
                              self._return_num_as_string(k) + " חודשים."
                    print(phrase)
                    self._single_run (i, j, k, phrase, pos_or_neg)

    def _single_run(self, i, j, k, phrase, pos_or_neg):
        # given = self.translator.run (phrase)
        # should = self.arr.shift (days=i * pos_or_neg, weeks=j * pos_or_neg, months=k * pos_or_neg).format("YYYYMMDD")
        # self.assertEqual (given, should, "For days=" + str (i) + " Weeks=" + str (j) + " Months=" + str (k))

        given_specific = self.translator_specific.run (phrase)
        print("--------------20200219")
        print(given_specific)
        should_specific = self.arr_specific.shift(days=i * pos_or_neg, weeks=j * pos_or_neg, months=k * pos_or_neg).format ("YYYYMMDD")
        print(should_specific)
        self.assertEqual (given_specific, should_specific,
                          "For days=" + str (i) + " Weeks=" + str (j) + " Months=" + str (k))

    def _return_num_as_string(self, num):
        if num == 1:
            return "אחד"
        if num == 2:
            return "שני"
        if num == 3:
            return "שלושה"
        if num == 4:
            return "ארבעה"
        if num == 5:
            return "חמישה"
        if num == 6:
            return "שישה"
        if num == 7:
            return "שיבעה"
        if num == 8:
            return "שמונה"
        if num == 9:
            return "תישעה"
        if num == 10:
            return "עשרה"
        if num == 11:
            return "אחד עשר"
        if num == 12:
            return "שנים עשר"
        if num == 13:
            return "שלושה עשר"
        if num == 14:
            return "ארבעה עשר"
        if num == 15:
            return "חמישה עשר"
        if num == 16:
            return "שישה עשר"
        if num == 17:
            return "שיבעה עשר"
        if num == 18:
            return "שמונה עשר"
        if num == 19:
            return "תישעה עשר"
        if num == 20:
            return "עשרים"
        if num == 21:
            return "עשרים ואחד"
        if num == 22:
            return "עשרים ושניים"
        if num == 23:
            return "עשרים ושלושה"
        if num == 24:
            return "עשרים וארבעה"
        if num == 25:
            return "עשרים וחמישה"
        if num == 26:
            return "עשרים ושישה"
        if num == 27:
            return "עשרים ושיבעה"
        if num == 28:
            return "עשרים ושמונה"
        if num == 29:
            return "עשרים ותישעה"
        if num == 30:
            return "שלושים"
        if num == 31:
            return "שלושים ואחד"


if __name__ == '__main__':
    unittest.main()
