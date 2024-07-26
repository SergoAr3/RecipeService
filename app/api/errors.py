from fastapi import HTTPException
from starlette import status


HTTP_404_NOT_FOUND_RECIPE = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No recipe found")
HTTP_404_NOT_FOUND_RECIPE_OR_STEP = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                  detail="No recipe or step found")
HTTP_404_NOT_FOUND_RECIPE_OR_INGREDIENT = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                        detail="No recipe or ingredient found")
HTTP_404_NOT_FOUND_IMAGE = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No image for recipe")
HTTP_409_CONFLICT_CREATED = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                          detail="Recipe with this name already exists")
HTTP_409_CONFLICT_USER_EXISTS = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                              detail='User with this username already exists!')
HTTP_500_INTERNAL_ERROR = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        detail="Internal Server Error")
