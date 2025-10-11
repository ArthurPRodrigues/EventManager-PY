import os
from string import Template


class HtmlTemplateEngine:
    def __init__(self, templates_dir: str):
        if not os.path.isdir(templates_dir):
            raise FileNotFoundError(
                f"The templates directory was not found: {templates_dir}"
            )
        self.templates_dir = templates_dir

    def render(self, template_name: str, context: dict) -> str:
        template_path = os.path.join(self.templates_dir, template_name)

        try:
            with open(template_path, encoding="utf-8") as f:
                template_content = f.read()

            html_template = Template(template_content)

            return html_template.substitute(context)

        except FileNotFoundError:
            # TODO: remove print after ticket redeeming implementation
            print(f"Error: Template file not found at {template_path}")
            raise
        except KeyError as e:
            # TODO: remove print after ticket redeeming implementation
            print(
                f"Error: The variable {e} is missing in the context for the template {template_name}"
            )
            raise
