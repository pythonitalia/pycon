from jinja2 import Environment, Undefined


class DefaultingUndefined(Undefined):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.variable_name = kwargs.get("name")

    def __str__(self):
        return "{{" + self.variable_name + "}}"


def render_template_from_string(
    template_string: str, context: dict, *, show_placeholders: bool = False
) -> str:
    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True,
    )

    if show_placeholders:
        env.undefined = DefaultingUndefined

    template = env.from_string(template_string)
    return template.render(context).strip()
