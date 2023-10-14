import os

import frontmatter  # type: ignore
import marko
from marko.block import Document, Heading, List, ListItem, Paragraph
from marko.inline import Image, RawText

from recipe_model import Recipe, RecipeCategory

NAME_HEADING_LEVEL = 1


def get_recipe_name(document: Document) -> str:
    for node in document.children:
        if type(node) is Heading and node.level == NAME_HEADING_LEVEL:
            rawtext = node.children[0]
            assert type(rawtext) is RawText

            return rawtext.children

    assert False


def get_recipe_ingredients(document: Document) -> list[str]:
    ret = get_list_from_section(document, "Ingredients")
    assert ret is not None
    return ret


def get_list_items(node: List) -> list[str]:
    out: list[str] = []

    for item in node.children:
        assert type(item) is ListItem

        par = item.children[0]
        assert type(par) is Paragraph

        rawtext = par.children[0]
        assert type(rawtext) is RawText

        out.append(rawtext.children)

    return out


def get_list_from_section(document: Document, section: str) -> list[str] | None:
    section_found = False
    for node in document.children:
        if type(node) is Heading:
            rawtext = node.children[0]
            assert type(rawtext) is RawText

            section_found = rawtext.children == section

        if type(node) is List and section_found:
            return get_list_items(node)

    return None


def get_recipe_instructions(document: Document) -> list[str]:
    ret = get_list_from_section(document, "Instructions")
    assert ret is not None
    return ret


def get_recipe_notes(document: Document) -> list[str] | None:
    return get_list_from_section(document, "Notes")


def get_recipe_slug(recipe_filename: str) -> str:
    recipe_filename = recipe_filename.split(os.sep)[-1]
    recipe_filename = recipe_filename.split(".")[0]

    return recipe_filename.replace("_", "-")


def get_recipe_image_path(document: Document) -> str | None:
    for node in document.children:
        if type(node) is Paragraph:
            img = node.children[0]
            assert type(img) is Image

            # The resulting templates get rendered to docs/ -- hence the '..'
            return f"{os.path.join('..', 'recipes', img.dest)}"

    return None


def get_recipe_category(post: dict[str, str]) -> RecipeCategory:
    cat = post["category"] if post.get("category") else "Other"
    cat = cat.replace(" ", "_").upper()
    try:
        return RecipeCategory[cat]
    except KeyError:
        return RecipeCategory.OTHER


def parse_recipe_file(recipe_filename: str) -> Recipe:
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
