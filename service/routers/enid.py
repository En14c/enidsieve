from fastapi import APIRouter

from ..models import ENID, ENIDMetaData


router = APIRouter(
    prefix='/enids',
    tags=['enids'],
    responses={422: {'description': 'Not a valid Egyptian national ID.'}}
)

@router.post('/sieve', response_model=ENIDMetaData)
async def enid_seive(enid: ENID):
    """Handles the validation of the egyptian national ID and the extraction
    of the encoded metadata to a human/computer readable metadata.

    NOTE: with "from_enid()" i tried to provide as much abstraction as i can (metadata are
        encoded in the national ID) and to separate eny decoding or parsing logic from the
        view.
    """
    return ENIDMetaData.from_enid(enid)