from fastapi import APIRouter


router = APIRouter()


# Test
@router.get('/')
async def test():
    return {'status': 'Successful'}
