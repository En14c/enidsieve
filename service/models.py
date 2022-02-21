from __future__ import annotations
from typing import Dict

from pydantic import BaseModel, constr, validator

from .utils import decode_enid
from .exceptions import ENIDDecodeError


class ENID(BaseModel):
    """Represents the Egyptian National ID and used to validate it."""
    enid: constr(regex='[0-9]{14}') # we expect the ID to contain only digits and len(enid) == 14

    @validator('enid')
    def validate_enid(cls, v):
        """Validates the incoming national ID.
        
        NOTE: the parsing and decoding logic is delegated to a utility function, to allow
        reuseability, and to reduce code repetition as much as we can.

        :params v: the national ID which needs to be validated, at this point we know that the
            incoming enid, has been validated to be a string of digits w/ length 14, and we
            should delegate further decoding and parsing process to decode_enid().
        :returns: the enid value after validation.
        :raises ValueError: when a malformed national ID has been provided, with a descriptive error message
        """
        try:
            decode_enid(v)
        except (ENIDDecodeError,) as e:
            raise ValueError(getattr(e, 'message', 'Malformed National ID.'))
        else:
            return v
    
    @property
    def metadata(self) -> Dict:
        """Provides access to the information encoded in the national ID.
        
        :returns: as the decoded metadata as a Dict.
        """
        return decode_enid(self.enid)

class ENIDMetaData(BaseModel):
    """Represents the metadata which would be incoded in the national ID."""
    century_code: int
    century_span: str
    birthdate_unixtimestamp: int
    birthdate: str
    governorate: str
    governorate_code: int
    gender: str
    check_code: int

    @classmethod
    def from_enid(cls, enid: ENID) -> ENIDMetaData:
        """Retrieves the metadata from a given national ID.
        
        :params enid: a *validated* ENID instance
        :returns: a *validated* ENIDMetaData instance.
        """
        return cls(**enid.metadata)