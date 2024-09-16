from fastapi import APIRouter, status
from app.apps.generator.services import GeneratorService
from app.apps.generator.schema import InGenerator, GeneratorSchema


generator_controller = APIRouter()


@generator_controller.post("", response_model=GeneratorSchema, status_code=status.HTTP_200_OK)
async def generate(query: InGenerator):
    return await GeneratorService().run(query)
