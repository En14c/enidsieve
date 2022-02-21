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
    """
    return ENIDMetaData.from_enid(enid)