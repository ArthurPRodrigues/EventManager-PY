import os
from string import Template


class HtmlTemplateEngine:
    def __init__(self, templates_dir: str):
        self.templates_dir = templates_dir

    def render(self, template_name: str, context: dict) -> str:
        template_path = os.path.join(self.templates_dir, template_name)
        with open(template_path, encoding="utf-8") as f:
            template_content = f.read()

        html_template = Template(template_content)

        return html_template.substitute(context)
