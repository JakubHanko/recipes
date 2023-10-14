def write_recipes(environment, recipes):
    template = environment.get_template("recipe.html")

    for recipe in recipes:
        template.stream(
            recipe_name=recipe.name,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            notes=recipe.notes,
            image=recipe.img_path,
        ).dump(f"docs/{recipe.slug}.html")


def write_index(environment, recipes):
    template = environment.get_template("index.html")

    template.stream(recipes=recipes).dump("docs/index.html")
