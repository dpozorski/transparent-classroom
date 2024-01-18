from typing import Dict, Any
from datetime import date, datetime


class Formatter(object):
    """
    Formatter Class

    Helper class for formatting values for model (de)serialization.

    Attributes:


    """

    @staticmethod
    def _jsonify_value(value: Any) -> Any:
        """
        Make the provided-value JSON safe.

        :param value: Any, The value to jsonify.
        :return: Any

        """

        if value is not None:
            if isinstance(value, date):
                return Formatter.date_to_str(value=value)
            elif isinstance(value, datetime):
                return Formatter.datetime_to_str(value=value)
            elif isinstance(value, dict):
                return Formatter.jsonify(data=value)
            elif isinstance(value, list):
                for i in range(0, len(value)):
                    value[i] = Formatter._jsonify_value(value=value[i])

                return value
            elif hasattr(value, "to_json"):
                return Formatter.jsonify(data=value.to_json())
            else:
                return value

    @staticmethod
    def jsonify(data: Dict) -> Dict:
        """
        Convert the data dictionary into a JSON-compatible dictionary.

        :param data: Dict, The data dictionary to parse into a JSON string (e.g. convert
            objects/values into json representations, where possible).
        :return: Dict

        """

        for key, value in data.items():
            data[key] = Formatter._jsonify_value(value=value)

        return data

    @staticmethod
    def date_to_str(value: date) -> str:
        """
        Convert the date to the Transparent Classsroom string format.

        :param value: date, The date to convert.
        :return: str

        """

        if value is not None:
            if isinstance(value, date):
                return date.strftime(value, "%Y-%m-%d")
            elif isinstance(value, str):
                return value
            else:
                raise ValueError(f"The provided value {value} is not date-like.")

    @staticmethod
    def datetime_to_str(value: datetime) -> str:
        """
        Convert the datetime to the Transparent Classsroom string format.

        :param value: datetime, The datetime to convert.
        :return: str

        """

        if value is not None:
            if isinstance(value, datetime):
                return datetime.strftime(value, "%Y-%m-%d %H:%M:%S.%f-%z")
            elif isinstance(value, str):
                return value
            else:
                raise ValueError(f"The provided value {value} is not datetime-like.")

    @staticmethod
    def str_to_date(value: str) -> date:
        """
        Convert the string to a date object.

        :param value: str, The string to convert.
        :return: date

        """

        if value is not None:
            if isinstance(value, date):
                return value
            elif isinstance(value, str):
                return datetime.strptime(value, "%Y-%m-%d").date()
            else:
                raise ValueError(f"The provided value {value} is not date-like.")

    @staticmethod
    def str_to_datetime(value: str) -> datetime:
        """
        Convert the string to a datetime object.

        :param value: str, The string to convert.
        :return: datetime

        """

        if value is not None:
            if isinstance(value, datetime):
                return value
            elif isinstance(value, str):
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f-%z")
            else:
                raise ValueError(f"The provided value {value} is not datetime-like.")
