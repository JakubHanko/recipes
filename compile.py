import glob
import os

from jinja2 import Environment, PackageLoader, select_autoescape

from recipe_model import recipe_category_format
from recipe_parser import parse_recipe_file

if __name__ == "__main__":
    recipe_filenames = glob.glob("recipes/*.md")

    recipes = [parse_recipe_file(c) for c in recipe_filenames]

    recipes.sort(key=lambda x: x.name)

    env = Environment(loader=PackageLoader("compile"), autoescape=select_autoescape())
    env.filters["recipe_category_format"] = recipe_category_format

    template = env.get_template("recipe.html")

    if not os.path.exists('docs/'):
        os.makedirs('docs')

    for recipe in recipes:
        template.stream(
            recipe_name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            notes=recipe.notes,
            image=recipe.img_path,
        ).dump(f"docs/{recipe.slug}.html")

    index_template = env.get_template("index.html")

    recipes_dict = {}

    for recipe in recipes:
        if recipe.category not in recipes_dict:
            recipes_dict[recipe.category] = []

        recipes_dict[recipe.category].append(recipe)
    index_template.stream(recipes=recipes_dict).dump("docs/index.html")
