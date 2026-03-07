import re
from fastapi.responses import JSONResponse

replacements = [
            ('ŋ', 'ng'), ('ɔ', 'o'), ('ə', 'ê'), ('ɛ', 'e'), ('ɡ', 'g'), ('ɪ', 'i'),
            ('ɲ', 'ny'), ('ʃ', 'sy'), ('ʊ', 'u'), ('ʒ', 'j'), ('ʔ', 'k'),('ˈ', '')
            ]

class Resp:
    @staticmethod
    def build_response(data: dict = None):
        response = {
            "data": data or {}
        }
        return JSONResponse(content=response)

class normalization_id:
    def __init__(self):
        self.units = ['nol', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan']
        self.teens = ['sepuluh', 'sebelas', 'dua belas', 'tiga belas', 'empat belas', 'lima belas', 'enam belas', 'tujuh belas', 'delapan belas', 'sembilan belas']
        self.tens = ['nol', 'sepuluh', 'dua puluh', 'tiga puluh', 'empat puluh', 'lima puluh', 'enam puluh', 'tujuh puluh', 'delapan puluh', 'sembilan puluh']
        self.thousands = ['ribu', 'juta', 'miliar', 'triliun']
        self.months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

        self.roman_numerals = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000,
            'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900
        }
    def create_pronunciation_mapping(self):
        return {  # letter mapping
            'A': 'a', 'B': 'be', 'C': 'ce', 'D': 'de', 'E': 'e',
            'F': 'ef', 'G': 'ge', 'H': 'ha', 'I': 'i', 'J': 'je',
            'K': 'ka', 'L': 'el', 'M': 'em', 'N': 'en', 'O': 'o',
            'P': 'pe', 'Q': 'ku', 'R': 'er', 'S': 'es', 'T': 'te',
            'U': 'u', 'V': 've', 'W': 'we', 'X': 'ik', 'Y': 'ye',
            'Z': 'zet'
        }
    
    def spell_out(self, text):
        mapping = self.create_pronunciation_mapping()
        spelled_out = ' '.join(mapping.get(char, char) for char in text.upper())
        return spelled_out

    def spelling_process(self, text):
        def abr(text):
            abr_list = re.findall(r'\b[A-Z0-9]{1,}\b', text)

            for abr in abr_list:
                if abr.isdigit():
                    continue
                spelled_out = self.spell_out(abr)
                text = text.replace(abr, spelled_out)
            
            return text

        spelled_out_text = abr(text)
        return spelled_out_text
    
    def number_to_words(self, n):
        if n == 0:
            return "nol"
        elif n < 10:
            return self.units[n]
        elif n < 20:
            return self.teens[n - 10]
        elif n < 100:
            if n % 10 == 0:
                return self.tens[n // 10]
            else:
                return self.tens[n // 10] + " " + self.units[n % 10]
        elif n < 200:
            if n == 100:
                return "seratus"
            else:
                return "seratus " + self.number_to_words(n % 100)
        elif n == 1000:
            return "seribu"
        elif n < 1000:
            if n % 100 == 0:
                return self.units[n // 100] + " ratus"
            else:
                return self.units[n // 100] + " ratus " + ("" if n % 100 == 0 else self.number_to_words(n % 100))
        elif n < 1000000:
            if n == 1000:
                return "seribu"
            elif n % 1000 == 0:
                return self.number_to_words(n // 1000) + " ribu"
            else:
                return self.number_to_words(n // 1000) + " ribu " + self.number_to_words(n % 1000)
        else:
            for i, v in enumerate(self.thousands):
                if n < 1000 ** (i + 1):
                    if n // (1000 ** i) == 1 and i == 1:
                        return "seribu" + ("" if n % (1000 ** i) == 0 else " " + self.number_to_words(n % (1000 ** i)))
                    else:
                        return self.number_to_words(n // (1000 ** i)) + " " + self.thousands[i] + ("" if n % (1000 ** i) == 0 else " " + self.number_to_words(n % (1000 ** i)))

    def normalize_url(self, word):
        url = word.replace('://', ' ')
        url = url.replace('.', ' dot ')
        url = url.replace('https', 'HTTPS').replace('http', 'HTTP').replace('www', 'WWW')
        url = re.sub(r'\d', lambda x: ' ' + self.units[int(x.group())] + ' ', url).replace('  ', ' ')
        return url.strip()

    def normalize_email(self, word):
        email = word.replace('.', ' dot ').replace('@', ' at ')
        email = re.sub(r'\d', lambda x: ' ' + self.units[int(x.group())] + ' ', email).replace('  ', ' ')
        return email.strip()

    def normalize_date(self, word, delimiter='/'):
        day, month, year = word.split(delimiter)
        if day.isdigit() and month.isdigit() and year.isdigit():
            day, month, year = int(day), int(month), int(year)
            if day <= 31 and month <= 12 and year <= 9999:
                    return self.number_to_words(day) + ' ' + self.months[month - 1] + ' ' + self.number_to_words(year)
            elif day <= 12 and month <= 31 and year <= 9999:
                    return self.number_to_words(int(month)) + ' ' + self.months[int(day) - 1] + ' ' + self.number_to_words(int(year))
            else :
                return self.number_to_words(int(year)) + ' ' + self.months[int(month) - 1] + ' ' + self.number_to_words(int(day))

    def normalize_currencyss(self, text):
        word = re.sub(r'\b(Rp|USD|EUR)(\d+(?:\.\d{3})*(?:,\d+)?)', r'\1|\2', text)
        words = re.split(r'[\s|]', word)
        parts = [word for word in words if word]
        if len(parts) == 2 and parts[0] == "Rp":
            before_comma = parts[0]
            after_comma = parts[1]
            if '.' in after_comma:
                decimal_part = after_comma.split('.')[1]
                pure_part = after_comma.split('.')[0]
                if len(decimal_part) > 2:
                    return self.normalize_pure_number(after_comma) + ' rupiah'
                elif len(decimal_part) == 1:
                    return 'Rp ' + self.number_to_words(int(pure_part)) + ' titik ' + ' '.join(self.units[int(digit)] for digit in decimal_part)
                elif len(decimal_part) == 2:
                    return 'Rp ' + self.number_to_words(int(pure_part)) + ' titik ' + ' '.join(self.units[int(digit)] for digit in decimal_part)
            else:
                return self.normalize_pure_number(after_comma) + ' rupiah'
        return text

    def normalize_currencySS(self, text):
        match = re.match(r'Rp(\d+(?:\.\d{3})*(?:,\d{2})?)', text)
        if match:
            number_str = match.group(1).replace('.', '').replace(',', '.')
            number = float(number_str)
            integer_part = int(number)
            decimal_part = round(number - integer_part, 2) * 100
            
            if decimal_part == 0:
                return self.number_to_words(integer_part) + " rupiah"
            else:
                decimal_words = " ".join(self.units[int(digit)] for digit in str(int(decimal_part)))
                return self.number_to_words(integer_part) + " koma " + decimal_words + " rupiah"
        return text

    def normalize_currency(self, text):
        matchrp = re.match(r'Rp(\d+(?:\.\d{3})*(?:,\d{2})?)', text)
        matcheur = re.match(r'EUR(\d+(?:\.\d{3})*(?:,\d{2})?)', text)
        matchusd = re.match(r'USD(\d+(?:\.\d{3})*(?:,\d{2})?)', text)
        matchsgd = re.match(r'SGD(\d+(?:\.\d{3})*(?:,\d{2})?)', text)
        if matchrp:
            number_str = matchrp.group(1).replace('.', '').replace(',', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            if decimal_part == None or decimal_part == "00":
                return self.number_to_words(whole_number_part) + " rupiah"
            else:
                return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} rupiah"
        elif matcheur:
            number_str = matcheur.group(1).replace('.', '').replace(',', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            if decimal_part == None or decimal_part == "00":
                return self.number_to_words(whole_number_part) + " euro"
            else:
                return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} euro"
        elif matchusd:
            number_str = matchusd.group(1).replace('.', '').replace(',', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            if decimal_part == None or decimal_part == "00":
                return self.number_to_words(whole_number_part) + " dolar amerika"
            else:
                return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} dolar amerika"
        elif matchsgd:
            number_str = matchsgd.group(1).replace('.', '').replace(',', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            if decimal_part == None or decimal_part == "00":
                return self.number_to_words(whole_number_part) + " dolar singapura"
            else:
                return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} dolar singapura"
        return text

    def normalize_units(self, text):
        unit_mapping = {
            r'\bkm\b': 'kilometer',
            r'\bcm\b': 'centimeter',
            r'\bmm\b': 'millimeter',
            r'\bm\b': 'meter',
            r'\bg\b': 'gram',
            r'\bkg\b': 'kilogram',
            r'\bml\b': 'milliliter',
            r'\bl\b': 'liter',
        }
        for unit, full_form in unit_mapping.items():
            text = re.sub(unit, full_form, text)
        return text

                
    def normalize_percentage(self, word, delimiter=','):
        parts = word.replace('%', '').split(delimiter)
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            before_comma = parts[0]
            after_comma = parts[1]
            return self.number_to_words(int(before_comma)) + ' koma ' + ' '.join(self.units[int(digit)] for digit in after_comma) + ' persen'
        return word

    def normalize_point(self, word, delimiter='.'):
        parts = word.split(delimiter)
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit() and len(parts[1]) == 1:
            before_comma = parts[0]
            after_comma = parts[1]
            return self.number_to_words(int(before_comma)) + ' titik ' + ' '.join(self.units[int(digit)] for digit in after_comma)
        elif len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit() and len(parts[1]) == 2:
            before_comma = parts[0]
            after_comma = parts[1]
            return self.number_to_words(int(before_comma)) + ' titik ' + ' '.join(self.units[int(digit)] for digit in after_comma)
        return word

    def normalize_fraction(self, word, delimiter='.'):
        parts = word.replace('%', '').split(delimiter)
        if len(parts) == 2 and '/' in parts[1]:
            fraction_parts = parts[1].split('/')
            if parts[0].isdigit() and fraction_parts[0].isdigit() and fraction_parts[1].isdigit():
                before_fraction = parts[0]
                after_fraction = fraction_parts[0]
                denominator = fraction_parts[1]
                return self.number_to_words(int(before_fraction)) + ' koma ' + self.number_to_words(int(after_fraction)) + ' per ' + self.number_to_words(int(denominator))
        return word

    def normalize_comma_number(self, word):
        parts = word.split(',')
        if all(part.isdigit() for part in parts):
            before_comma = self.number_to_words(int(parts[0]))
            after_comma = ' koma ' + ' '.join(self.units[int(digit)] for digit in parts[1])
            return before_comma + after_comma
        return word

    def normalize_thousand_point_commass(self, text):
        match = re.match(r'(\d+(?:\.\d{3})*(?:,\d{2})?)', text)
        if match:
            number_str = match.group(1).replace('.', '').replace(',', '.')
            number = float(number_str)
            integer_part = int(number)
            decimal_part = round(number - integer_part, 2) * 100
            
            integer_words = self.number_to_words(integer_part)
            if decimal_part > 0:
                decimal_words = " ".join(self.units[int(digit)] for digit in str(int(decimal_part)))
                return integer_words + " koma " + decimal_words
            else:
                return integer_words
        return text

    def normalize_thousand_point_comma(self, word):
        number = word.replace('.', '').replace(',', '.')
        parts = number.split('.')
        whole_number_part = int(parts[0])
        decimal_part = parts[1] if len(parts) > 1 else None
        if decimal_part:
            return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)}"
        return self.number_to_words(whole_number_part)

    def normalize_division(self, word):
        parts = word.split('/')
        if all(part.isdigit() for part in parts):
            return self.number_to_words(int(parts[0])) + ' per ' + self.number_to_words(int(parts[1]))
        return word

    def normalize_pure_number(self, word):
        if '-an' in word:
            return self.normalize_an_suffix(word)
        word = word.replace('.', '')
        if word.isdigit():
            if word.startswith('0'):
                return ' '.join(self.units[int(digit)] for digit in word)
            return self.number_to_words(int(word))
        return word

    def normalize_percentage_number(self, word):
        number_part = int(word[:-1])
        return self.number_to_words(number_part) + ' persen'

    def normalize_number_to_word(self, word):
        number_part = int(word[:-1])
        return self.number_to_words(number_part)

    def normalize_bracket(self, word):
        bracket = word.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '')
        return bracket

    def normalize_text_with_digits(self, word):
        idx = next((i for i, char in enumerate(word) if char.isdigit()), None)
        word_text = word[:idx]
        word_number = word[idx:]
        word_number = ' '.join(self.units[int(digit)] for digit in word_number if digit.isdigit())
        return word_text + " " + word_number

    def roman_to_int(self, s):
        i = 0
        num = 0
        while i < len(s):
            if i + 1 < len(s) and s[i:i+2] in self.roman_numerals:
                num += self.roman_numerals[s[i:i+2]]
                i += 2
            else:
                num += self.roman_numerals[s[i]]
                i += 1
        return num

    def normalize_roman(self, word):
        if all(char in self.roman_numerals for char in word):
            num = self.roman_to_int(word)
            return self.number_to_words(num)
        return word

    def normalize_an_suffix(self, word):
        if re.match(r'^\d+\.?\d*-an$', word):
            base_number = word[:-3].replace('.', '')
            if base_number.isdigit():
                if int(base_number) % 1000 == 0:
                    return self.number_to_words(int(base_number)) + "an"
                else:
                    return self.number_to_words(int(base_number)) + "an"
        return word

    def normalize_time_HHMM(self, hour, minute):
        hour = int(hour.lstrip('0') or '0')  
        minute = int(minute.lstrip('0') or '0') 
        hour_str = self.number_to_words(hour) if hour > 0 else self.normalize_pure_number("00")
        minute_str = self.number_to_words(minute) if minute > 0 else self.normalize_pure_number("0")
        if hour == 0 and minute == 0:
            return f"{hour_str} lewat {minute_str} menit"
        elif hour > 0 and minute == 0:
            return hour_str
        else:
            return f"{hour_str} lewat {minute_str} menit"

    def normalize_time_HHMMSS(self, hour, minute, seconds):
        hour = int(hour.lstrip('0') or '0')
        minute = int(minute.lstrip('0') or '0')
        seconds = int(seconds.lstrip('0') or '0')
        hour_str = self.number_to_words(hour) if hour > 0 else self.normalize_pure_number("00")
        minute_str = self.number_to_words(minute) if minute > 0 else self.normalize_pure_number("0")
        seconds_str = self.number_to_words(seconds) if seconds > 0 else self.normalize_pure_number("0")
        if hour == 0 and minute == 0 and seconds == 0:
            return f"{hour_str}"
        elif hour > 0 and minute == 0 and seconds == 0:
            return f"{hour_str}"
        elif hour == 0 and minute > 0 and seconds == 0:
            return f"{hour_str} lewat {minute_str} menit"
        elif hour == 0 and minute == 0 and seconds > 0:
            return f"{hour_str} lewat {seconds_str} detik"
        elif hour > 0 and minute > 0 and seconds == 0:
            return f"{hour_str} lewat {minute_str} menit"
        elif hour > 0 and minute == 0 and seconds > 0:
            return f"{hour_str} lewat {seconds_str} detik"
        elif hour == 0 and minute > 0 and seconds > 0:
            return f"{hour_str} lewat {minute_str} menit {seconds_str} detik"
        else:  # hour > 0 and minute > 0 and seconds > 0
            return f"{hour_str} lewat {minute_str} menit {seconds_str} detik"

    def extract_currency_large(self, text):
        matchrp = re.match(r'(?i)(rp|idr)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:,\d{1,2})?)\s?(juta|miliar|triliun)', text)
        matchusd = re.match(r'(?i)(usd)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:,\d{1,2})?)\s?(juta|miliar|triliun)', text)
        matcheur = re.match(r'(?i)(eur)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:,\d{1,2})?)\s?(juta|miliar|triliun)', text)
        matchsgd = re.match(r'(?i)(sgd)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:,\d{1,2})?)\s?(juta|miliar|triliun)', text)
        if matchrp:
            currency = matchrp.group(1)
            number_str = matchrp.group(2).replace('.', '').replace(',', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            large_number = str.lower(matchrp.group(3))
            if decimal_part == None or decimal_part == "00":
                return f"{self.number_to_words(whole_number_part)} {large_number} rupiah"
            else:
                return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} {large_number} rupiah"
        elif matchusd:
            currency = matchusd.group(1)
            number_str = matchusd.group(2).replace('.', '').replace(',', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            large_number = str.lower(matchusd.group(3))
            if decimal_part == None or decimal_part == "00":
                return f"{self.number_to_words(whole_number_part)} {large_number} dolar amerika"
            else:
                return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} {large_number} dolar amerika"
        elif matcheur:
            currency = matcheur.group(1)
            number_str = matcheur.group(2).replace('.', '').replace(',', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            large_number = str.lower(matcheur.group(3))
            if decimal_part == None or decimal_part == "00":
                return f"{self.number_to_words(whole_number_part)} {large_number} euro"
            else:
                return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} {large_number} euro"
        elif matchsgd:
            currency = matchsgd.group(1)
            number_str = matchsgd.group(2).replace('.', '').replace(',', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            large_number = str.lower(matchsgd.group(3))
            if decimal_part == None or decimal_part == "00":
                return f"{self.number_to_words(whole_number_part)} {large_number} dolar singapura"
            else:
                return f"{self.number_to_words(whole_number_part)} koma {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} {large_number} dolar singapura"

    def split_text(self, text):
        regex = r'\b(?:https?://|www\.)\S+|[\w\.-]+@[\w\.-]+|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d+/\d+|(?:Rp|IDR|USD|EUR|SGD)\s?\d+(?:,\d{1,3})?(?:\.\d{3})*(?:,\d{1,3})?(?: ?(?:[Jj][Uu][Tt][Aa]|[Mm][Ii][Ll][Ii][Aa][Rr]|[Tt][Rr][Ii][Ll][Ii][Uu][Nn]))?%?|\d+\.\d{3}(?:\.\d{3})*(?:,\d{1,3})?%?|\d+,\d+%?|\d+\.\d+%?|\d+%|\d{1,2}:\d{2}(?::\d{2})?|[^\w\s]|[\w-]+'
        
        words = re.findall(regex, text)
        normalized_words = []

        for word in words:
            if re.match(r'(?i)(Rp|IDR|USD|EUR|SGD)\s?\d+(?:,\d{1,3})?(?:\.\d{3})*(?:,\d{1,3})?(?: ?(?:[Jj][Uu][Tt][Aa]|[Mm][Ii][Ll][Ii][Aa][Rr]|[Tt][Rr][Ii][Ll][Ii][Uu][Nn]))?', word):
                word = re.sub(r'\b(Rp|IDR|USD|EUR|SGD)\s?(\d+(?:,\d{1,3})?(?:\.\d{3})*(?:,\d{1,3})?(?: ?(?:[Jj][Uu][Tt][Aa]|[Mm][Ii][Ll][Ii][Aa][Rr]|[Tt][Rr][Ii][Ll][Ii][Uu][Nn]))?)\b', r'\1\2', word, flags=re.IGNORECASE)
                normalized_words.append(word)
            elif re.match(r'[\w\.-]+@[\w\.-]+|\b(?:https?://|www\.)\S+|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}:\d{2}(?::\d{2})?|\d+/\d+$', word):
                normalized_words.append(word)
            elif any(char.isdigit() for char in word):
                if word.endswith(',') or word.endswith('.'):
                    number_part = word.rstrip(',.')
                    punctuation_part = word[len(number_part):]
                    if number_part:
                        normalized_words.append(number_part)
                    if punctuation_part:
                        normalized_words.append(punctuation_part)
                else:
                    normalized_words.append(word)
            else:
                normalized_words.append(word)

        final_words = []
        for word in normalized_words:
            if re.match(r'[\(\)\[\]\{\}]+.*|.*[\(\)\[\]\{\}]+', word):
                final_words.extend(re.findall(r'\(|\)|\[|\]|\{|\}|[^\(\)\[\]\{\}]+', word))
            else:
                final_words.append(word)
        final_words = [word for word in final_words if word]

        return final_words

    def num_char(self, text):
        words = self.split_text(text)
        normalized_words = []
        for word in words:
            if re.search(r'([a-zA-Z]*)(\d+)([a-zA-Z]+)', word):
                split_word = re.findall(r'([a-zA-Z]*)(\d+)([a-zA-Z]+)', word)
                for char1, num, char2 in split_word:
                    if char1:
                        normalized_words.append(char1)
                    normalized_words.append(num)
                    normalized_words.append(char2)
            else:
                normalized_words.append(word)
        normalized_words = [re.sub(r'\s([,.!?])', r'\1', word) for word in normalized_words]
        return normalized_words

    def normalize_numbers(self, text):
        words = self.num_char(text)
        normalized_words = []

        for word in words:
            if word.endswith(',') and word[:-1].isdigit() :
                normalized_words.append(self.normalize_number_to_word(word)+',')
            elif word.endswith('.') and word[:-1].isdigit() :
                normalized_words.append(self.normalize_number_to_word(word)+'.')
            elif re.match(r'\b(\d{1,2})\:(\d{2})\:(\d{2})\b', word):
                time_match = re.match(r'\b(\d{1,2})\:(\d{2})\:(\d{2})\b', word)
                if time_match:
                    hour, minute, seconds = time_match.groups()
                    normalized_words.append(self.normalize_time_HHMMSS(hour, minute, seconds))
                else:
                    normalized_words.append(word)
            elif re.match(r'\b(\d{1,2})\.(\d{2})\b', word):
                time_match = re.match(r'\b(\d{1,2})\.(\d{2})\b', word)
                if time_match:
                    hour, minute = time_match.groups()
                    normalized_words.append(self.normalize_time_HHMM(hour, minute))
                else:
                    normalized_words.append(word)
            elif re.match(r'\b(\d{1,2})\:(\d{2})\b', word):
                time_match = re.match(r'\b(\d{1,2})\:(\d{2})\b', word)
                if time_match:
                    hour, minute = time_match.groups()
                    normalized_words.append(self.normalize_time_HHMM(hour, minute))
                else:
                    normalized_words.append(word)
            elif re.match(r'(https?|ftp)://[^\s/$.?#].[^\s]*', word) or re.match(r'www\.[^\s/$.?#].[^\s]*', word) or re.match(r'http\.[^\s/$.?#].[^\s]*', word):
                normalized_words.append(self.normalize_url(word))
            elif re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', word):
                normalized_words.append(self.normalize_email(word))
            elif re.match(r'^\d+(?:\.\d{3})*(?:,\d{2})$', word):
                normalized_words.append(self.normalize_thousand_point_comma(word))
            elif re.match(r'(?i)(rp|idr|usd|sgd|eur)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:,\d{1,2})?)\s?(juta|miliar|triliun)', word):
                normalized_words.append(self.extract_currency_large(word))
            elif re.match(r'(?:Rp|rP|RP|rp|IDR|USD|EUR|SGD)(\d+(?:\.\d{3})*(?:,\d{2})?)', word):
                normalized_words.append(self.normalize_currency(word))
            elif '/' in word and len(word.split('/')) == 3:
                normalized_words.append(self.normalize_date(word, '/'))
            elif '-' in word and len(word.split('-')) == 3:
                normalized_words.append(self.normalize_date(word, '-'))
            elif (',' in word or '.' in word) and '%' in word:
                normalized_words.append(self.normalize_percentage(word, ',' if ',' in word else '.'))
            elif ('.' in word or ',' in word) and '/' in word:
                normalized_words.append(self.normalize_fraction(word, '.' if '.' in word else ','))
            elif ',' in word:
                normalized_words.append(self.normalize_comma_number(word))
            elif '/' in word:
                normalized_words.append(self.normalize_division(word))
            elif '(' in word or ')' in word or '[' in word or ']' in word or '{' in word or '}' in word:
                normalized_words.append(self.normalize_bracket(word))
            elif word.isdigit():
                normalized_words.append(self.normalize_pure_number(word))
            elif any(unit in word for unit in ['km', 'cm', 'mm', 'm', 'g', 'kg', 'ml', 'l']):
                normalized_words.append(self.normalize_units(word))
            elif '.' in word and len(word.split('.')[1]) == 1 :
                normalized_words.append(self.normalize_point(word))
            elif '.' in word and len(word.split('.')[1]) == 2 :
                normalized_words.append(self.normalize_point(word))
            elif '.' in word and word.replace('.', '').isdigit():
                normalized_words.append(self.normalize_pure_number(word))
            elif word.endswith('%') and word[:-1].isdigit():
                normalized_words.append(self.normalize_percentage_number(word))
            elif re.match(r'^\d+\.?\d*-an$', word):
                normalized_words.append(self.normalize_an_suffix(word))
            elif any(char.isdigit() for char in word):
                normalized_words.append(self.normalize_text_with_digits(word))
            else:
                normalized_words.append(word)

        normalized_words = [word for word in normalized_words if word]
        normalized_text = ' '.join(normalized_words)
        normalized_text = re.sub(r'\s([,.!?])', r'\1', normalized_text) 
        
        return normalized_text
    
    def preprocess(self, text):
        text = self.spelling_process(text)
        text = self.normalize_numbers(text)
        return text

class normalization_en:
    def __init__(self):
        self.units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        self.teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
        self.tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        self.thousands = ["", "thousand", "million", "billion", "trillion"]
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    def create_pronunciation_mapping(self):
        return { # letter mapping
            'A': 'ei', 'B': 'bi', 'C': 'ci', 'D': 'di', 'E': 'i','F': 'ef', 'G': 'ji', 'H': 'eij', 'I': 'ai',
            'J': 'jei','K': 'kei', 'L': 'el', 'M': 'em', 'N': 'en', 'O': 'o','P': 'pi',  'Q': 'kyu', 'R': 'ar',
            'S': 'es', 'T': 'ti','U': 'yu', 'V': 'vi', 'W': 'dobl iu', 'X': 'ex', 'Y': 'wai','Z': 'zi'
        }

    def spell_out(self, text):
        mapping = self.create_pronunciation_mapping()
        spelled_out = ' '.join(mapping.get(char, char) for char in text.upper())
        return spelled_out

    def spelling_process(self, text):
        def abr(text):
            abr_list = re.findall(r'\b[A-Z0-9]{1,}\b', text)

            for abr in abr_list:
                if abr.isdigit():
                    continue
                spelled_out = self.spell_out(abr)
                text = text.replace(abr, spelled_out)
            
            return text

        spelled_out_text = abr(text)
        return spelled_out_text

    def number_to_words(self, n):
        if n == 0:
            return "zero"
        elif n < 10:
            return self.units[n]
        elif n < 20:
            return self.teens[n - 10]
        elif n < 100:
            if n % 10 == 0:
                return self.tens[n // 10]
            else:
                return self.tens[n // 10] + " " + self.units[n % 10]
        elif n < 1000:
            if n % 100 == 0:
                return self.units[n // 100] + " hundred"
            else:
                return self.units[n // 100] + " hundred and " + self.number_to_words(n % 100)
        else:
            for i, v in enumerate(self.thousands):
                if n < 1000 ** (i + 1):
                    if n % (1000 ** i) == 0:
                        return self.number_to_words(n // (1000 ** i)) + " " + v
                    else:
                        if (n % (1000 ** i)) < 100:
                            return self.number_to_words(n // (1000 ** i)) + " " + v + " and " + self.number_to_words(n % (1000 ** i))
                        else:
                            return self.number_to_words(n // (1000 ** i)) + " " + v + " " + self.number_to_words(n % (1000 ** i))
        
    def split_text(self, text):
        regex = r'\b(?:https?://|www\.)\S+|[\w\.-]+@[\w\.-]+|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d+/\d+|(?:Rp|IDR|USD|EUR|SGD)\s?\d+(?:,\d{1,3})?(?:\.\d{3})*(?:,\d{1,3})?(?: ?(?:[Jj][Uu][Tt][Aa]|[Mm][Ii][Ll][Ii][Aa][Rr]|[Tt][Rr][Ii][Ll][Ii][Uu][Nn]))?%?|\d+\.\d{3}(?:\.\d{3})*(?:,\d{1,3})?%?|\d+,\d+%?|\d+\.\d+%?|\d+%|\d{1,2}:\d{2}(?::\d{2})?|[^\w\s]|[\w-]+'
        words = re.findall(regex, text)
        normalized_words = []

        for word in words:
            if re.match(r'(?i)(Rp|IDR|USD|EUR|SGD)\s?\d+(?:,\d{1,3})?(?:\.\d{3})*(?:,\d{1,3})?(?: ?(?:[Jj][Uu][Tt][Aa]|[Mm][Ii][Ll][Ii][Aa][Rr]|[Tt][Rr][Ii][Ll][Ii][Uu][Nn]))?', word):
                word = re.sub(r'\b(Rp|IDR|USD|EUR|SGD)\s?(\d+(?:,\d{1,3})?(?:\.\d{3})*(?:,\d{1,3})?(?: ?(?:[Jj][Uu][Tt][Aa]|[Mm][Ii][Ll][Ii][Aa][Rr]|[Tt][Rr][Ii][Ll][Ii][Uu][Nn]))?)\b', r'\1\2', word, flags=re.IGNORECASE)
                normalized_words.append(word)
            elif re.match(r'[\w\.-]+@[\w\.-]+|\b(?:https?://|www\.)\S+|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}:\d{2}(?::\d{2})?|\d+/\d+$', word):
                normalized_words.append(word)
            elif any(char.isdigit() for char in word):
                if word.endswith(',') or word.endswith('.'):
                    number_part = word.rstrip(',.')
                    punctuation_part = word[len(number_part):]
                    if number_part:
                        normalized_words.append(number_part)
                    if punctuation_part:
                        normalized_words.append(punctuation_part)
                else:
                    normalized_words.append(word)
            else:
                normalized_words.append(word)

        final_words = []
        for word in normalized_words:
            if re.match(r'[\(\)\[\]\{\}]+.*|.*[\(\)\[\]\{\}]+', word):
                final_words.extend(re.findall(r'\(|\)|\[|\]|\{|\}|[^\(\)\[\]\{\}]+', word))
            else:
                final_words.append(word)

        final_words = [word for word in final_words if word]

        return final_words

    def num_char(self, text):
        words = self.split_text(text)
        normalized_words = []
        for word in words:
            if re.search(r'([a-zA-Z]*)(\d+)([a-zA-Z]+)', word):
                split_word = re.findall(r'([a-zA-Z]*)(\d+)([a-zA-Z]+)', word)
                for char1, num, char2 in split_word:
                    if char1:
                        normalized_words.append(char1)
                    normalized_words.append(num)
                    normalized_words.append(char2)
            else:
                normalized_words.append(word)
        normalized_words = [re.sub(r'\s([,.!?])', r'\1', word) for word in normalized_words]
        return normalized_words

    def normalize_number_to_word(self, word):
        number_part = int(word[:-1])
        return self.number_to_words(number_part)

    def normalize_url(self, word):
        url = word.replace('://', ' ')
        url = url.replace('.', ' dot ')
        url = url.replace('https', 'HTTPS').replace('http', 'HTTP').replace('www', 'WWW')
        url = re.sub(r'\d', lambda x: ' ' + self.units[int(x.group())] + ' ', url).replace('  ', ' ')
        return url.strip()

    def normalize_email(self, word):
        email = word.replace('.', ' dot ').replace('@', ' at ')
        email = re.sub(r'\d', lambda x: ' ' + self.units[int(x.group())] + ' ', email).replace('  ', ' ')
        return email.strip()

    def normalize_thousand_point_comma(self, word):
        number = word.replace(',', '').replace('.', '.')
        parts = number.split('.')
        whole_number_part = int(parts[0])
        decimal_part = parts[1] if len(parts) > 1 else None

        if decimal_part:
            return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)}"
        return self.number_to_words(whole_number_part)

    def extract_currency_large(self, text):
        matchrp = re.match(r'(?i)(rp|idr)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:\.\d{1,2})?)\s?(juta|miliar|triliun)', text)
        matchusd = re.match(r'(?i)(usd)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:\.\d{1,2})?)\s?(juta|miliar|triliun)', text)
        matcheur = re.match(r'(?i)(eur)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:\.\d{1,2})?)\s?(juta|miliar|triliun)', text)
        matchsgd = re.match(r'(?i)(sgd)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:\.\d{1,2})?)\s?(juta|miliar|triliun)', text)

        if matchrp:
            currency = "Indonesian Rupiah"
            number_str = matchrp.group(2).replace(',', '').replace('.', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            large_number = matchrp.group(3).lower().replace("juta", "million").replace("miliar", "billion").replace("triliun", "trillion")
            if decimal_part is None or decimal_part == "00":
                return f"{self.number_to_words(whole_number_part)} {large_number} {currency}"
            else:
                return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} {large_number} {currency}"

        elif matchusd:
            currency = "US Dollar"
            number_str = matchusd.group(2).replace(',', '').replace('.', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            large_number = matchusd.group(3).lower().replace("juta", "million").replace("miliar", "billion").replace("triliun", "trillion")
            if decimal_part is None or decimal_part == "00":
                return f"{self.number_to_words(whole_number_part)} {large_number} {currency}"
            else:
                return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} {large_number} {currency}"

        elif matcheur:
            currency = "Euro"
            number_str = matcheur.group(2).replace(',', '').replace('.', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            large_number = matcheur.group(3).lower().replace("juta", "million").replace("miliar", "billion").replace("triliun", "trillion")
            if decimal_part is None or decimal_part == "00":
                return f"{self.number_to_words(whole_number_part)} {large_number} {currency}"
            else:
                return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} {large_number} {currency}"

        elif matchsgd:
            currency = "Singapore Dollar"
            number_str = matchsgd.group(2).replace(',', '').replace('.', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            large_number = matchsgd.group(3).lower().replace("juta", "million").replace("miliar", "billion").replace("triliun", "trillion")
            if decimal_part is None or decimal_part == "00":
                return f"{self.number_to_words(whole_number_part)} {large_number} {currency}"
            else:
                return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} {large_number} {currency}"

    def normalize_currency(self, text):
        matchrp = re.match(r'IDR(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        matcheur = re.match(r'EUR(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        matchusd = re.match(r'USD(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        matchsgd = re.match(r'SGD(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        if matchrp:
            number_str = matchrp.group(1).replace(',', '').replace('.', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            if decimal_part is None or decimal_part == "00":
                return self.number_to_words(whole_number_part) + " rupiah"
            else:
                return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} rupiah"
        elif matcheur:
            number_str = matcheur.group(1).replace(',', '').replace('.', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            if decimal_part is None or decimal_part == "00":
                return self.number_to_words(whole_number_part) + " euros"
            else:
                return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} euros"
        elif matchusd:
            number_str = matchusd.group(1).replace(',', '').replace('.', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            if decimal_part is None or decimal_part == "00":
                return self.number_to_words(whole_number_part) + " US dollars"
            else:
                return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} US dollars"
        elif matchsgd:
            number_str = matchsgd.group(1).replace(',', '').replace('.', '.')
            parts = number_str.split('.')
            whole_number_part = int(parts[0])
            decimal_part = parts[1] if len(parts) > 1 else None
            if decimal_part is None or decimal_part == "00":
                return self.number_to_words(whole_number_part) + " Singapore dollars"
            else:
                return f"{self.number_to_words(whole_number_part)} point {' '.join(self.number_to_words(int(digit)) for digit in decimal_part)} Singapore dollars"
        return text

    def normalize_date(self, word, delimiter='/'):
        day, month, year = word.split(delimiter)
        if day.isdigit() and month.isdigit() and year.isdigit():
            day, month, year = int(day), int(month), int(year)
            if day <= 31 and month <= 12 and year <= 9999:
                    return self.number_to_words(day) + ' ' + self.months[month - 1] + ' ' + self.number_to_words(year)
            elif day <= 12 and month <= 31 and year <= 9999:
                    return self.number_to_words(int(month)) + ' ' + self.months[int(day) - 1] + ' ' + self.number_to_words(int(year))
            else :
                return self.number_to_words(int(year)) + ' ' + self.months[int(month) - 1] + ' ' + self.number_to_words(int(day))

    def normalize_percentage(self, word, delimiter=','):

        parts = word.replace('%', '').split(delimiter)
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            before_comma = parts[0]
            after_comma = parts[1]
            before_comma_words = self.number_to_words(int(before_comma))
            after_comma_words = ' '.join(self.units[int(digit)] for digit in after_comma)
            return f"{before_comma_words} point {after_comma_words} percent"
        
        return word

    def normalize_fraction(self, word, delimiter='.'):
        parts = word.replace('%', '').split(delimiter)
        if len(parts) == 2 and '/' in parts[1]:
            fraction_parts = parts[1].split('/')
            if parts[0].isdigit() and fraction_parts[0].isdigit() and fraction_parts[1].isdigit():
                before_fraction = parts[0]
                after_fraction = fraction_parts[0]
                denominator = fraction_parts[1]
                return self.number_to_words(int(before_fraction)) + ' point ' + self.number_to_words(int(after_fraction)) + ' over ' + self.number_to_words(int(denominator))
        return word

    def normalize_comma_number(self, word):
        parts = word.split(',')
        if all(part.isdigit() for part in parts):
            before_comma = self.number_to_words(int(parts[0]))
            after_comma = ' point ' + ' '.join(self.units[int(digit)] for digit in parts[1])
            return before_comma + after_comma
        return word

    def normalize_division(self, word):
        parts = word.split('/')
        if all(part.isdigit() for part in parts):
            return self.number_to_words(int(parts[0])) + ' per ' + self.number_to_words(int(parts[1]))
        return word

    def normalize_bracket(self, word):
        bracket = word.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '')
        return bracket

    def normalize_units(self, text):
        unit_mapping = {
            r'\bkm\b': 'kilometer',
            r'\bcm\b': 'centimeter',
            r'\bmm\b': 'millimeter',
            r'\bm\b': 'meter',
            r'\bg\b': 'gram',
            r'\bkg\b': 'kilogram',
            r'\bml\b': 'milliliter',
            r'\bl\b': 'liter',
            r'\btbsp\b': 'tablespoon',
            r'\bteaspoon\b': 'teaspoon',
        }
        for unit, full_form in unit_mapping.items():
            text = re.sub(unit, full_form, text)
        return text

    def normalize_point(self, word, delimiter='.'):
        parts = word.split(delimiter)
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit() and len(parts[1]) == 1:
            before_point = parts[0]
            after_point = parts[1]
            return self.number_to_words(int(before_point)) + ' point ' + ' '.join(self.units[int(digit)] for digit in after_point)
        elif len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit() and len(parts[1]) == 2:
            before_point = parts[0]
            after_point = parts[1]
            return self.number_to_words(int(before_point)) + ' point ' + ' '.join(self.units[int(digit)] for digit in after_point)
        return word

    def normalize_percentage_number(self, word):
        number_part = int(word[:-1])
        return self.number_to_words(number_part) + ' percent'

    def normalize_text_with_digits(self, word):
        idx = next((i for i, char in enumerate(word) if char.isdigit()), None)
        word_text = word[:idx]
        word_number = word[idx:]

        if word_number.isdigit():
            normalized_number = self.number_to_words(int(word_number))
            return word_text + " " + normalized_number
        
        return word_text + " " + word_number

    def normalize_numbers(self, text):
        words = self.num_char(text)
        normalized_words = []

        for word in words:
            if word.endswith(',') and word[:-1].isdigit() :
                normalized_words.append(self.normalize_number_to_word(word)+',')
            elif word.endswith('.') and word[:-1].isdigit() :
                normalized_words.append(self.normalize_number_to_word(word)+'.')
            elif re.match(r'(https?|ftp)://[^\s/$.?#].[^\s]*', word) or re.match(r'www\.[^\s/$.?#].[^\s]*', word) or re.match(r'http\.[^\s/$.?#].[^\s]*', word):
                normalized_words.append(self.normalize_url(word))
            elif re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', word):
                normalized_words.append(self.normalize_email(word))
            elif re.match(r'^\d{1,3}(?:,\d{3})*(?:\.\d+)?$', word):
                normalized_words.append(self.normalize_thousand_point_comma(word))
            elif re.match(r'(?i)(rp|idr|usd|sgd|eur)\s?(\d{1,3}(?:[\.,]\d{1,3})*(?:\.\d{1,2})?)\s?(million|billion|trillion)', word):
                normalized_words.append(self.extract_currency_large(word))
            elif re.match(r'(?:Rp|rP|RP|rp|IDR|USD|EUR|SGD)(\d+(?:\.\d{3})*(?:,\d{2})?)', word):
                normalized_words.append(self.normalize_currency(word))
            elif re.match(r'(?:IDR|USD|EUR|SGD)(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', word):
                normalized_words.append(self.normalize_currency(word))
            elif '/' in word and len(word.split('/')) == 3:
                normalized_words.append(self.normalize_date(word, '/'))
            elif '-' in word and len(word.split('-')) == 3:
                normalized_words.append(self.normalize_date(word, '-'))
            elif (',' in word or '.' in word) and '%' in word:
                normalized_words.append(self.normalize_percentage(word, ',' if ',' in word else '.'))
            elif ('.' in word or ',' in word) and '/' in word:
                normalized_words.append(self.normalize_fraction(word, '.' if '.' in word else ','))
            elif ',' in word:
                normalized_words.append(self.normalize_comma_number(word))
            elif '/' in word:
                normalized_words.append(self.normalize_division(word))
            elif '(' in word or ')' in word or '[' in word or ']' in word or '{' in word or '}' in word:
                normalized_words.append(self.normalize_bracket(word))
            elif any(unit in word for unit in ['km', 'cm', 'mm', 'm', 'g', 'kg', 'ml', 'l', 'tbsp', 'tsp']):
                normalized_words.append(self.normalize_units(word))
            elif '.' in word and len(word.split('.')[1]) == 1 :
                normalized_words.append(self.normalize_point(word))
            elif '.' in word and len(word.split('.')[1]) == 2 :
                normalized_words.append(self.normalize_point(word))
            elif word.endswith('%') and word[:-1].isdigit():
                normalized_words.append(self.normalize_percentage_number(word))
            elif any(char.isdigit() for char in word):
                normalized_words.append(self.normalize_text_with_digits(word))
            else:
                normalized_words.append(word)

        normalized_words = [word for word in normalized_words if word]
        normalized_text = ' '.join(normalized_words)
        normalized_text = re.sub(r'\s([,.!?])', r'\1', normalized_text) 
        
        return normalized_text
    
    def preprocess(self, text):
        text = self.spelling_process(text)
        text = self.normalize_numbers(text)
        return text
    
def split_and_recombine_text(text, desired_length=50, max_length=70):
    """Split text it into chunks of a desired length trying to keep sentences intact."""
    text = re.sub(r'\n\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[“”]', '"', text)

    rv = []
    in_quote = False
    current = ""
    split_pos = []
    pos = -1
    end_pos = len(text) - 1

    def seek(delta):
        nonlocal pos, in_quote, current
        is_neg = delta < 0
        for _ in range(abs(delta)):
            if is_neg:
                pos -= 1
                current = current[:-1]
            else:
                pos += 1
                current += text[pos]
            if text[pos] == '"':
                in_quote = not in_quote
        return text[pos]

    def peek(delta):
        p = pos + delta
        return text[p] if p < end_pos and p >= 0 else ""

    def commit():
        nonlocal rv, current, split_pos
        rv.append(current)
        current = ""
        split_pos = []

    while pos < end_pos:
        c = seek(1)
        # do we need to force a split?
        if len(current) >= max_length:
            if len(split_pos) > 0 and len(current) > (desired_length / 2):
                # we have at least one sentence and we are over half the desired length, seek back to the last split
                d = pos - split_pos[-1]
                seek(-d)
            else:
                # no full sentences, seek back until we are not in the middle of a word and split there
                while c not in '!?.\n ' and pos > 0 and len(current) > desired_length:
                    c = seek(-1)
            commit()
        # check for sentence boundaries
        elif not in_quote and (c in '!?\n' or (c == '.' and peek(1) in '\n ')):
            # seek forward if we have consecutive boundary markers but still within the max length
            while pos < len(text) - 1 and len(current) < max_length and peek(1) in '!?.':
                c = seek(1)
            split_pos.append(pos)
            if len(current) >= desired_length:
                commit()
        # treat end of quote as a boundary if its followed by a space or newline
        elif in_quote and peek(1) == '"' and peek(2) in '\n ':
            seek(2)
            split_pos.append(pos)
    rv.append(current)

    # clean up, remove lines with only whitespace or punctuation
    rv = [s.strip() for s in rv]
    rv = [s for s in rv if len(s) > 0 and not re.match(r'^[\s\.,;:!?]*$', s)]

    return rv

def cleanup_text(text):
    for src, dst in replacements:
        text = text.replace(src, dst)
    return text