import glob
import json
import os
import shutil
import sys

from jinja2 import Environment, PackageLoader, select_autoescape

from recipe_engine.model import Recipe, RecipeCategory, recipe_category_format
from recipe_engine.parser import parse_recipe_file
from recipe_engine.writer import write_index, write_recipes

if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    if not config.get("output_dir"):
        sys.exit("Missing 'output_dir' key in the configuration file.")

    output_dir = config["output_dir"]

    recipe_filenames = glob.glob("recipes/*.md")

    recipes = [parse_recipe_file(c) for c in recipe_filenames]

    recipes.sort(key=lambda x: x.name)

    env = Environment(loader=PackageLoader("compile"), autoescape=select_autoescape())
    env.filters["recipe_category_format"] = recipe_category_format

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    write_recipes(env, recipes, output_dir)

    recipes_dict: dict[RecipeCategory, list[Recipe]] = {}

    for recipe in recipes:
        if recipe.category not in recipes_dict:
            recipes_dict[recipe.category] = []

        recipes_dict[recipe.category].append(recipe)

    write_index(env, recipes_dict, output_dir)

    shutil.copyfile(
        os.path.join("templates", "styles.css"), os.path.join(output_dir, "styles.css")
    )

    if os.path.exists(os.path.join("recipes", "img")):
        shutil.copytree(
            os.path.join("recipes", "img"),
            os.path.join(output_dir, "img"),
            dirs_exist_ok=True,
        )
