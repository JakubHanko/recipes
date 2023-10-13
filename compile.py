import glob
import os
from dataclasses import dataclass
from typing import List

import marko
import marko.block as mb
from jinja2 import Environment, PackageLoader, select_autoescape
from marko.block import Heading, List

NAME_HEADING_LEVEL = 1
INGREDIENTS_STR = "Ingrediencie"
INSTRUCTIONS_STR = "Postup"
NOTES_STR = "Poznámky"


def get_recipe_name(document):
    for node in document.children:
        if type(node) is mb.Heading and node.level == NAME_HEADING_LEVEL:
            return node.children[0].children


def get_recipe_ingredients(document):
    return get_list_from_section(document, INGREDIENTS_STR)


def get_list_from_section(document, section):
    section_found = False
    for node in document.children:
        if type(node) is Heading:
            section_found = node.children[0].children == section

        if type(node) is mb.List and section_found:
            return [item.children[0].children[0].children for item in node.children]


def get_recipe_instructions(document):
    return get_list_from_section(document, INSTRUCTIONS_STR)


def get_recipe_notes(document):
    return get_list_from_section(document, NOTES_STR)


def get_recipe_slug(recipe_filename):
    recipe_filename = recipe_filename.split(os.sep)[-1]
    recipe_filename = recipe_filename.split(".")[0]

    return recipe_filename.replace("_", "-")


def parse_recipe_file(recipe_filename):
    with open(recipe_filename) as f:
        recipe_doc = marko.parse(f.read())

    return Recipe(
        name=get_recipe_name(recipe_doc),
        ingredients=get_recipe_ingredients(recipe_doc),
        instructions=get_recipe_instructions(recipe_doc),
        notes=get_recipe_notes(recipe_doc),
        slug=get_recipe_slug(recipe_filename),
    )


@dataclass
class Recipe:
    name: str
    ingredients: List[str]
    instructions: List[str]
    notes: List[str]
    slug: str


if __name__ == "__main__":
    recipe_filenames = glob.glob("recipes/*.md")

    recipes = [parse_recipe_file(c) for c in recipe_filenames]

    env = Environment(loader=PackageLoader("compile"), autoescape=select_autoescape())

    template = env.get_template("recipe.html")

    for recipe in recipes:
        template.stream(
            recipe_name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            notes=recipe.notes,
        ).dump(f"docs/{recipe.slug}.html")

    index_template = env.get_template("index.html")
    index_template.stream(recipes=recipes).dump("docs/index.html")
