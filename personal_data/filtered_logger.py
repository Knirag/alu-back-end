#!/usr/bin/env python3
"""
Module for filtering log data.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate specified fields in the log message using redaction string.

    :param fields: List of strings representing fields to obfuscate.
    :param redaction: String representing the redaction value.
    :param message: String representing the log line.
    :param separator: String representing the character separating fields in the log line.
    :return: String with specified fields obfuscated.
    """
    pattern = re.compile(
            r'(?<=(' + '|'.join(fields) + r')=)[^' + re.escape(separator) + r']*'
            )
    return re.sub(pattern, redaction, message)

# Additional functions or classes as needed
