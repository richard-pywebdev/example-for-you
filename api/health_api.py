from fastapi import APIRouter, status, Response


router = APIRouter()


@router.get('/health', status_code=status.HTTP_200_OK)
async def health_check_api(response: Response):
    response.headers["X-Health-Check"] = "ok"
    return {
        'health': "ok"
    }