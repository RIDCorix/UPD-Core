from typing import Dict, List
import time

def list_to_dict(l, key='key'):
    result = {}
    for item in l:
        result[item[key]] = item