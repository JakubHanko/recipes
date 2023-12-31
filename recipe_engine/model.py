from dataclasses import dataclass
from enum import Enum, auto


class RecipeCategory(Enum):
    APPETIZER = auto()
    MAIN_COURSE = auto()
    DESSERT = auto()
    SALAD = auto()
    SOUP = auto()
    BREAKFAST = auto()
    OTHER = auto()


@dataclass
class Recipe:
    name: str
    ingredients: list[str]
    instructions: list[str]
    notes: list[str] | None
    slug: str
    img_path: str | None
    category: RecipeCategory


def recipe_category_format(category: RecipeCategory) -> str:
    out = str(category)
    out = out.split(".")[-1]
    out = out.lower().capitalize()
    out = out.replace("_", " ")

    if category not in [RecipeCategory.BREAKFAST, RecipeCategory.OTHER]:
        out += "s"

    return out
