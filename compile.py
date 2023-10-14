import glob
import os

from jinja2 import Environment, PackageLoader, select_autoescape

from recipe_model import recipe_category_format
from recipe_parser import parse_recipe_file
from recipe_writer import write_index, write_recipes

if __name__ == "__main__":
    recipe_filenames = glob.glob("recipes/*.md")

    recipes = [parse_recipe_file(c) for c in recipe_filenames]

    recipes.sort(key=lambda x: x.name)

    env = Environment(loader=PackageLoader("compile"), autoescape=select_autoescape())
    env.filters["recipe_category_format"] = recipe_category_format

    if not os.path.exists("docs/"):
        os.makedirs("docs")

    write_recipes(env, recipes)

    recipes_dict = {}

    for recipe in recipes:
        if recipe.category not in recipes_dict:
            recipes_dict[recipe.category] = []

        recipes_dict[recipe.category].append(recipe)

    write_index(env, recipes_dict)
