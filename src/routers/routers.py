from fastapi import APIRouter

from src.routers.products.router import router as product_router
from src.routers.recipes.router import router as recipe_router
from src.routers.audio.router import router as audio_router


router = APIRouter(prefix="/api/v1")

router.include_router(router=product_router)
router.include_router(router=recipe_router)
router.include_router(router=audio_router)