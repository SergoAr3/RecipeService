from app.repositories.ingredient import IngredientRepository
from app.schemas.ingredient import IngredientCreate, IngredientRead


class IngredientService:
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository

    async def get_by_ingredient_id(self, ingredient_id: int) -> IngredientRead:
        ingredient = await self.ingredient_repository.get(ingredient_id)
        ingredient = IngredientRead.from_orm(ingredient)
        return ingredient

    async def get_by_recipe_id(self, recipe_id: int) -> IngredientRead:
        ingredient = await self.ingredient_repository.get(recipe_id, by_recipe_id=True)
        ingredient = IngredientRead.from_orm(ingredient)
        return ingredient

    async def get_by_name(self, name: str) -> IngredientRead:
        ingredient = await self.ingredient_repository.get(name, by_name=True)
        ingredient = IngredientRead.from_orm(ingredient)
        return ingredient

    async def create_ingredient(self, ingredient: IngredientCreate, recipe_id: int) -> None:
        db_ingredient = await self.ingredient_repository.create(ingredient, recipe_id)

