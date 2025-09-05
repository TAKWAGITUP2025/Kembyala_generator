class AmountConverter:
    @staticmethod
    def number_to_words_french(number):
        units = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
        teens = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", 
                "dix-sept", "dix-huit", "dix-neuf"]
        tens = ["", "dix", "vingt", "trente", "quarante", "cinquante", 
               "soixante", "soixante", "quatre-vingt", "quatre-vingt"]
        
        def convert_less_than_hundred(n):
            if n < 10: return units[n]
            elif 10 <= n < 20: return teens[n - 10]
            elif 20 <= n < 100:
                if n == 80: return "quatre-vingts"
                if n % 10 == 0: return tens[n // 10]
                if 70 <= n < 80: return tens[6] + "-" + teens[n - 60]
                if 90 <= n < 100: return tens[8] + "-" + teens[n - 80]
                return tens[n // 10] + "-" + units[n % 10]
        
        def convert_less_than_thousand(n):
            if n < 100: return convert_less_than_hundred(n)
            hundred = n // 100
            remainder = n % 100
            res = "cent" if hundred == 1 else f"{units[hundred]} cent"
            return f"{res} {convert_less_than_hundred(remainder)}" if remainder > 0 else res
        
        if number == 0: return "zéro"
        
        parts = []
        if "." in str(number):
            integer_part, decimal_part = str(number).split(".")
            decimal_part = decimal_part.ljust(2, "0")[:2]
        else:
            integer_part, decimal_part = str(number), "00"
        
        num = int(integer_part)
        
        if num >= 1000000:
            million = num // 1000000
            parts.append(f"{convert_less_than_thousand(million)} million{'s' if million > 1 else ''}")
            num %= 1000000
        
        if num >= 1000:
            thousand = num // 1000
            parts.append(f"{convert_less_than_thousand(thousand)} mille")
            num %= 1000
        
        if num > 0: parts.append(convert_less_than_thousand(num))
        
        result = " ".join(parts)
        if decimal_part != "00": result += f" et {decimal_part}/100"
        return f"{result.capitalize()} dinars"

    @staticmethod
    def convert_amount_to_words(amount_str):
        try:
            amount_str = amount_str.replace(" ", "").replace(",", ".")
            amount = float(amount_str)
            return AmountConverter.number_to_words_french(amount)
        except ValueError:
            return ""