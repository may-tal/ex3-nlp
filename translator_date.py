import time
import arrow
import delorean
from enum import Enum
from datetime import date

BEFORE = -1
AFTER = 1

class Token(Enum):
    NUM = 1
    PLUS = 2
    MINUS = 3
    WEEK = 5
    DAY = 4
    MONTH = 6
    END = 7


class DateTranslator:
    NUMBER = {"אחד": 1,
              "שני": 2,
              "שלושה": 3,
              "ארבעה": 4,
              "חמישה": 5,
              "שישה": 6,
              "שיבעה": 7,
              "שמונה": 8,
              "תישעה": 9,
              "עשרה": 10,
              "אחד עשר": 11,
              "שנים עשר": 12,
              "שלושה עשר": 13,
              "ארבעה עשר": 14,
              "חמישה עשר": 15,
              "שישה עשר": 16,
              "שיבעה עשר": 17,
              "שמונה עשר": 18,
              "תישעה עשר": 19,
              "עשרים": 20,
              "עשרים ואחד": 21,
              "עשרים ושניים": 22,
              "עשרים ושלושה": 23,
              "עשרים וארבעה": 24,
              "עשרים וחמישה": 25,
              "עשרים ושישה": 26,
              "עשרים ושבעה": 27,
              "עשרים ושמונה": 28,
              "עשרים ותשעה": 29,
              "שלושים": 30,
              "שלושים ואחד": 31}

    def __init__(self, init_date=None):
        if init_date:
            self.date = arrow.get(init_date)
        else:
            self.date = arrow.get(str(date.today()).replace("-", ""))
        self.lookahead = None
        self.offset = 0

    def advance(self, date_tokens):
        if self.lookahead[0] != Token.END:
            self.offset += 1
            self.lookahead = date_tokens[self.offset]

    def translate_date(self, date_tokens):
        """
        :return: a string with the translated date in format yyyymmdd
        """
        return self.expr(date_tokens)

    def expr(self, date_tokens):
        if self.lookahead[0] == Token.MINUS:
            sign = BEFORE
        elif self.lookahead[0] == Token.PLUS:
            sign = AFTER
        else:
            print("error")
            return -1

        self.advance(date_tokens)
        cur_date = self.date
        while self.lookahead[0] != Token.END:
            cur_date = self.term(sign, date_tokens, cur_date)
            self.advance(date_tokens)

        return cur_date

    def term(self, sign, date_tokens, cur_date):
        num = self.lookahead[1]
        num = num * sign
        self.advance(date_tokens)
        unit = self.lookahead
        if unit[0] == Token.DAY:
            res = cur_date.shift(days=num)
        elif unit[0] == Token.WEEK:
            res = cur_date.shift(weeks=num)
        else:
            res = cur_date.shift(months=num)
        return res

    def tokenizer(self, date_phrase):
        """
        :param date_phrase:
        :return: list of tokens
        """
        tokens = []
        token_map = {'בעוד': Token.PLUS, 'לפני': Token.MINUS, '.': Token.END, 'יום': Token.DAY, 'ימים': Token.DAY,
                     'שבוע': Token.WEEK, 'שבועות': Token.WEEK, 'חודש': Token.MONTH, "חודשים": Token.MONTH}
        parts = date_phrase.split()
        parts[-1] = parts[-1][:-1]
        parts.append('.')
        double_digit = False
        single = False
        for i in range(len(parts)):
            if double_digit:
                double_digit = False
                continue

            if single:
                single = False
                if parts[i] == "אחד":
                    continue

            # if word start with "and" remove it
            if parts[i][0] == "ו":
                parts[i] = parts[i][1:]

            if parts[i] in DateTranslator.NUMBER or parts[i] == "שנים":
                if parts[i] + " " + parts[i+1] in DateTranslator.NUMBER:
                    tokens.append((Token.NUM, DateTranslator.NUMBER[parts[i] + " " + parts[i+1]]))
                    double_digit = True
                else:
                    tokens.append((Token.NUM, DateTranslator.NUMBER[parts[i]]))

            elif parts[i] in token_map:
                if parts[i] == "יום" or parts[i] == "שבוע" or parts[i] == "חודש":
                    tokens.append((Token.NUM, 1))
                    single = True
                tokens.append((token_map[parts[i]], 0))

            elif parts[i] == "יומיים":
                tokens.append((Token.NUM, 2))
                tokens.append((Token.DAY, 0))
            elif parts[i] == "שבועיים":
                tokens.append((Token.NUM, 2))
                tokens.append((Token.WEEK, 0))
            elif parts[i] == "חודשיים":
                tokens.append((Token.NUM, 2))
                tokens.append((Token.MONTH, 0))
            elif parts[i] == "היום":
                tokens.append((Token.MINUS, 0))
                tokens.append((Token.NUM, 0))
                tokens.append((Token.DAY, 0))
            elif parts[i] == "אתמול":
                tokens.append((Token.MINUS, 0))
                tokens.append((Token.NUM, 1))
                tokens.append((Token.DAY, 0))
            elif parts[i] == "מחר":
                tokens.append((Token.PLUS, 0))
                tokens.append((Token.NUM, 1))
                tokens.append((Token.DAY, 0))
        return tokens

    def run(self, date_phrase):
        """
        :return: translated date in format yyyymmdd
        """
        tokens = self.tokenizer(date_phrase)
        self.lookahead = tokens[0]
        self.offset = 0
        return str(self.translate_date(tokens)).split('T')[0].replace("-", "")


# def main():
#     date_translator = DateTranslator("20200219")
#     print(date_translator.run("לפני אחד ימים ושלושה שבועות ושני חודשים."))
#     a = arrow.get("20200219")
#     a= a.shift(days=-1)
#     a = a.shift(months=-2)
#     a= a.shift(weeks=-3)
#
#     print(a)
# main()

