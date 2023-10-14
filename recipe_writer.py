from jinja2 import Environment

from recipe_model import Recipe, RecipeCategory


def write_recipes(environment: Environment, recipes: list[Recipe]) -> None:
    template = environment.get_template("recipe.html")

    for recipe in recipes:
        template.stream(
            recipe_name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            notes=recipe.notes,
            image=recipe.img_path,
        ).dump(f"docs/{recipe.slug}.html")


def write_index(
    environment: Environment, recipes: dict[RecipeCategory, list[Recipe]]
) -> None:
    template = environment.get_template("index.html")

    template.stream(recipes=recipes).dump("docs/index.html")
