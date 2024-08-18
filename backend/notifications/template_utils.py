from jinja2 import Environment


def render_template_from_string(template_string: str, context: dict) -> str:
    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.from_string(template_string)
    return template.render(context).strip()
