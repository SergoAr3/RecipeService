from fastapi import HTTPException
from starlette import status


HTTP_404_NOT_FOUND_recipe = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No recipe found")
HTTP_404_NOT_FOUND_ingredient = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ingredient found")
HTTP_404_NOT_FOUND_image = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No image for recipe")
HTTP_409_CONFLICT_created = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                          detail="Recipe with this name already exists")
