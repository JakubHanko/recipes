import argparse
import glob
import os
import shutil

from jinja2 import Environment, PackageLoader, select_autoescape

from recipe_model import Recipe, RecipeCategory, recipe_category_format
from recipe_parser import parse_recipe_file
from recipe_writer import write_index, write_recipes

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", required=False, action="store_true")
    deploy_on = parser.parse_args().deploy

    recipe_filenames = glob.glob("recipes/*.md")

    recipes = [parse_recipe_file(c) for c in recipe_filenames]

    recipes.sort(key=lambda x: x.name)

    env = Environment(loader=PackageLoader("compile"), autoescape=select_autoescape())
    env.filters["recipe_category_format"] = recipe_category_format
    env.globals["path_base"] = "" if deploy_on else "../templates/"

    if not os.path.exists("docs/"):
        os.makedirs("docs")

    write_recipes(env, recipes)

    recipes_dict: dict[RecipeCategory, list[Recipe]] = {}

    for recipe in recipes:
        if recipe.category not in recipes_dict:
            recipes_dict[recipe.category] = []

        recipes_dict[recipe.category].append(recipe)

    write_index(env, recipes_dict)

    shutil.copyfile("templates/styles.css", "docs/styles.css")
