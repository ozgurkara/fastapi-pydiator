from fastapi import status, APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("",
            status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: {
                    "model": str,
                    "content": {
                        "text/plain": {
                            "example": "OK"
                        }
                    }
                }
            },
            response_class=PlainTextResponse)
async def get():
    return "OK"
