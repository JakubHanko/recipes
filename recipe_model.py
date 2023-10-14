from dataclasses import dataclass
from enum import Enum
from typing import List


class RecipeCategory(Enum):
    APPETIZER = 1
    MAIN_COURSE = 2
    DESSERT = 3
    SALAD = 4
    SOUP = 5
    BREAKFAST = 6
    OTHER = 7


@dataclass
class Recipe:
    name: str
    ingredients: List[str]
    instructions: List[str]
    notes: List[str]
    slug: str
    img_path: str
    category: RecipeCategory
