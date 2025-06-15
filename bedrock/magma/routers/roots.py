from fastapi import APIRouter


# ########    ROUTER:  root    ########


router = APIRouter(tags=["root"])


@router.get("/")
async def root():
    return {"message": "This is the root/default handler in the Bedrock 'Magma' FastAPI application."}

