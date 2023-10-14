import os

import frontmatter
import marko
from marko.block import Heading, List, Paragraph

from recipe_model import Recipe, RecipeCategory

NAME_HEADING_LEVEL = 1


def get_recipe_name(document):
    for node in document.children:
        if type(node) is Heading and node.level == NAME_HEADING_LEVEL:
            return node.children[0].children


def get_recipe_ingredients(document):
    return get_list_from_section(document, "Ingredients")


def get_list_from_section(document, section):
    section_found = False
    for node in document.children:
        if type(node) is Heading:
            section_found = node.children[0].children == section

        if type(node) is List and section_found:
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
        if type(node) is Paragraph:
            # The resulting templates get rendered to docs/ -- hende the '..'
            return f"{os.path.join('..', 'recipes', node.children[0].dest)}"


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
