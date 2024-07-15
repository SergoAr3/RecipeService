from fastapi import HTTPException
from starlette import status

HTTP_404_NOT_FOUND_recipe = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No recipe found")
HTTP_404_NOT_FOUND_ingredient = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ingredient found")
HTTP_404_NOT_FOUND_image = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No image for recipe")
HTTP_409_CONFLICT_created = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                          detail="Recipe with this name already exists")
HTTP_204_NO_CONTENT = HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No recipes found")
HTTP_200_OK_deleted = HTTPException(status_code=status.HTTP_200_OK, detail="Recipe has been deleted")
HTTP_200_OK_created = HTTPException(status_code=status.HTTP_200_OK, detail="Recipe has been created")
HTTP_200_OK_updated = HTTPException(status_code=status.HTTP_200_OK, detail="Recipe has been updated")
HTTP_200_OK_register = HTTPException(status_code=status.HTTP_200_OK, detail="User successfully registered")
HTTP_200_OK_rating = HTTPException(status_code=status.HTTP_200_OK, detail="Recipe has been successfully evaluated")
