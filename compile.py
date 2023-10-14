import glob
import os
from dataclasses import dataclass
from enum import Enum
from typing import List

import frontmatter
import marko
import marko.block as mb
from jinja2 import Environment, PackageLoader, select_autoescape

NAME_HEADING_LEVEL = 1


def get_recipe_name(document):
    for node in document.children:
        if type(node) is mb.Heading and node.level == NAME_HEADING_LEVEL:
            return node.children[0].children


def get_recipe_ingredients(document):
    return get_list_from_section(document, "Ingredients")


def get_list_from_section(document, section):
    section_found = False
    for node in document.children:
        if type(node) is mb.Heading:
            section_found = node.children[0].children == section

        if type(node) is mb.List and section_found:
            return [item.children[0].children[0].children for item in node.children]


def get_recipe_instructions(document):
    return get_list_from_section(document, "Instructions")


def get_recipe_notes(document):
    return get_list_from_section(document, "Notes")


def get_recipe_slug(recipe_filename):
    recipe_filename = recipe_filename.split(os.sep)[-1]
    recipe_filename = recipe_filename.split(".")[0]

    return recipe_filename.replace("_", "-")


def get_recipe_image_path(document):
    for node in document.children:
        if type(node) is mb.Paragraph:
            return f"{os.path.join('recipes', node.children[0].dest)}"


def get_recipe_category(post):
    cat = post["category"] if post.get("category") else "Other"
    cat = cat.replace(" ", "_").upper()
    try:
        return RecipeCategory[cat]
    except KeyError:
        return RecipeCategory.OTHER


def parse_recipe_file(recipe_filename):
    with open(recipe_filename) as f:
        content = f.read()
        recipe_doc = marko.parse(content)
        post = frontmatter.loads(content)

    return Recipe(
        name=get_recipe_name(recipe_doc),
        ingredients=get_recipe_ingredients(recipe_doc),
        instructions=get_recipe_instructions(recipe_doc),
        notes=get_recipe_notes(recipe_doc),
        slug=get_recipe_slug(recipe_filename),
        img_path=get_recipe_image_path(recipe_doc),
        category=get_recipe_category(post.metadata),
    )


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


def recipe_category_format(category):
    out = str(category)
    out = out.split(".")[-1]
    out = out.lower().capitalize()
    out = out.replace("_", " ")

    if category not in [RecipeCategory.BREAKFAST, RecipeCategory.OTHER]:
        out += "s"

    return out


if __name__ == "__main__":
    recipe_filenames = glob.glob("recipes/*.md")

    recipes = [parse_recipe_file(c) for c in recipe_filenames]

    recipes.sort(key=lambda x: x.name)

    env = Environment(loader=PackageLoader("compile"), autoescape=select_autoescape())
    env.filters["recipe_category_format"] = recipe_category_format

    template = env.get_template("recipe.html")

    for recipe in recipes:
        template.stream(
            recipe_name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            notes=recipe.notes,
            image=recipe.img_path,
        ).dump(f"{recipe.slug}.html")

    index_template = env.get_template("index.html")

    recipes_dict = {}

    for recipe in recipes:
        if recipe.category not in recipes_dict:
            recipes_dict[recipe.category] = []

        recipes_dict[recipe.category].append(recipe)
    index_template.stream(recipes=recipes_dict).dump("index.html")
