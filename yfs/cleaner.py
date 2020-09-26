from pydantic import BaseModel as Base


class large_numer_suffix(Base):
    T: int = 1_000_000_000_000
    B: int = 1_000_000_000
    M: int = 1_000_000


class ValueCleanerBase(Base):
    @staticmethod
    def remove_comma(value: str):
        return value.replace(",", "").strip()

    @staticmethod
    def remove_brakets(value: str):
        return value.replace("(", "").replace(")", "").strip()

    @staticmethod
    def remove_percent_sign(value: str):
        return value.replace("%", "").strip()

    @classmethod
    def remove_brakets_and_precent_sign(cls, value: str):
        value = cls.remove_brakets(value)
        return cls.remove_percent_sign(value)

    @staticmethod
    def value_is_missing(value):
        #     "N/A",
        #     "N/A (N/A)",
        #     "N/A x N/A",
        #     "N/A - N/A",
        #     "undefined - undefined",
        if not isinstance(value, str):
            return False

        if "N/A" in value:
            return True
        elif "undefined" in value:
            return True
        elif "+-" in value:  # ¯\_(ツ)_/¯ it happens.
            return True
        elif "-+" in value:
            return True
        elif value == "":
            return True
        elif value == " ":
            return True
        else:
            return False

    @staticmethod
    def has_large_number_suffix(value: str):
        for suffix, _ in large_numer_suffix():
            if suffix in value:
                return True
        else:
            return False

    @staticmethod
    def clean_large_number(value: str):
        for suffix, multiplier in large_numer_suffix():
            if suffix in value:
                return round(float(value.replace(suffix, "")) * multiplier)

    @classmethod
    def common_value_cleaner(cls, value: str):
        value = cls.remove_comma(value)

        if cls.has_large_number_suffix(value):
            value = cls.clean_large_number(value)

        return value
