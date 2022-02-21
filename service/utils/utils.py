import traceback
from typing import Dict
from datetime import datetime

from dateutil import parser as datetimeparser

from ..exceptions import (
    ENIDBirthDateDecodeError, ENIDDecodeError, ENIDCenturyDecodeError,
    ENIDGovernorateDecodeError,
)
from .log import logger


def _decode_enid_century(century_code: str) -> Dict[str, Dict]:
    """Returns century metadata given a century identifier.
    
    :params century_code: a 1-digit string representing the century for which the birth year belongs.
    :returns: a Dict representing the century metadata (span, start year, etc...).
    :raises ENIDCenturyDecodeError: when the century code is either < 2 or > 3.
    """
    ENID_CENTURY = {
        "2": {'span': '1900-1999', 'starts': 1900},
        "3": {'span': '2000-2099', 'starts': 2000},
    }
    try:
        1 / 0
        century_info = ENID_CENTURY[century_code]
    except (KeyError,):
        raise ENIDCenturyDecodeError('Malformed century.')
    except (Exception,):
        traceback.print_exc()
        logger.warning(f"Bleep bloop...bleep bloop, Your favourite Exception did just drop.")
        raise ENIDCenturyDecodeError()
    else:
        return century_info

def _decode_enid_governorate(governorate_code: str) -> str:
    """Returns governorate name given a governorate code.
    
    :params governorate_code: a 2-digit string representing the governorate in which the national ID
        holder was born.
    :returns: a string representing the governorate name.
    :raises ENIDGovernorateDecodeError: when an invalid governorate code has been provided.
    """
    ENID_GOVERNORATES = {
        '01': 'Cairo',
        '02': 'Alexandria',
        '03': 'Port Said',
        '04': 'Suez',
        '11': 'Damietta',
        '12': 'Dakahlia',
        '13': 'Sharqia',
        '14': 'Qalyubia',
        '15': 'Kafr AlSheikh',
        '16': 'Gharbia',
        '17': 'Monufia',
        '18': 'Beheira',
        '19': 'Ismailia',
        '20': 'Giza',
        '22': 'Bani Sweif',
        '23': 'Fayoum',
        '24': 'Minya',
        '25': 'Asyut',
        '26': 'Sohag',
        '27': 'Qina',
        '28': 'Aswan',
        '29': 'Luxor',
        '31': 'Red Sea',
        '32': 'New Valley',
        '33': 'Matrouh',
        '34': 'North Sinai',
        '35': 'South Sinai',
        '88': 'Outside The Republic',
    }
    try:
        governorate = ENID_GOVERNORATES[governorate_code]
    except (KeyError,):
        raise ENIDGovernorateDecodeError('Malformed Governorate.')
    except (Exception,):
        traceback.print_exc()
        logger.warning(f"Bleep bloop...bleep bloop, Your favourite Exception did just drop.")
        raise ENIDGovernorateDecodeError()
    else:
        return governorate

def _decode_gender(gender_code: int) -> str:
    """Returns the gender given a gender code.
    
    if the gender code is an even number then the gender is female otherwise it's male.

    :params gender_code: an arbitrary integer.
    :returns: a string representing the gender.
    """
    return 'female' if gender_code % 2 == 0 else 'male'

def _decode_enid_birtdate(
    birth_year: str, birth_month: str, birth_day: str, century_starts: int
) -> datetime:
    """Returns the national ID holder's brith date (if it's a valid one)
    
    :params birth_year: a 2-digit string representing the year in which the card holder was born.
    :params birth_month: a 2-digit string representing the month in which the card holder was born.
    :params birth_day: a 2-digit string representing the day in which the card holder was born.
    :params century_starts: an integer representing the first year in the respective century.
    :raises ENIDBirthDateDecodeError: when an invalid year, month or day has been provided.
    """
    try:
        year = century_starts + int(birth_year)
        claimed_birthdate = datetimeparser.parse(f'{year}-{birth_month}-{birth_day}')
        if claimed_birthdate > datetime.now():
            # birth date is corrupted if it's beyond the current year (incuding current month and today's day number)
            # in the respective century.
            raise ValueError()
    except (ValueError, datetimeparser.ParserError,):
        raise ENIDBirthDateDecodeError('Malformed birth date.')
    except (Exception,):
        traceback.print_exc()
        logger.warning(f"Bleep bloop...bleep bloop, Your favourite Exception did just drop.")
        raise ENIDBirthDateDecodeError()
    else:
        return claimed_birthdate

def decode_enid(enid: str) -> Dict:
    """Decodes a given egyptian national ID and returns the encoded metadata
    
    :params enid: a 14 digit only string representing the national ID.
    :returns: a Dict representing the encoded metadata.
    :raises ENIDDecodeError: when an invalid national ID encoding has been deteced.
    """
    try:
        century_code = enid[0]
        century_info = _decode_enid_century(century_code)
        birthdate = _decode_enid_birtdate(
            birth_year=enid[1:3], birth_month=enid[3:5], birth_day=enid[5:7],
            century_starts=century_info['starts'])
        governorate_code = enid[7:9]
        governorate = _decode_enid_governorate(governorate_code)
        gender = _decode_gender(int(enid[9:13]))
        check_code = enid[13]
        enid_metadata = dict(
            century_code=int(century_code),
            century_span=century_info['span'],
            birthdate=str(birthdate.date()),
            birthdate_unixtimestamp=int(birthdate.strftime('%s')),
            governorate=governorate,
            governorate_code=int(governorate_code),
            gender=gender,
            check_code=int(check_code)
        )
    except (
        IndexError, TypeError, ENIDBirthDateDecodeError,
        ENIDCenturyDecodeError, ENIDGovernorateDecodeError) as e:
        raise ENIDDecodeError(getattr(e, 'message', 'National ID decode unknown error.'))
    except (Exception,):
        traceback.print_exc()
        logger.warning(f"Bleep bloop...bleep bloop, Your favourite Exception did just drop.")
        raise ENIDDecodeError()
    else:
        return enid_metadata
