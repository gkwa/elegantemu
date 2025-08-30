import pathlib
import shlex

import jinja2


def shell_quote_filter(value: str) -> str:
    """Custom Jinja2 filter to quote shell values with double quotes when needed."""
    # If the value contains variables (like $FOLDER_NAME), use double quotes
    if "$" in value:
        # Escape any existing double quotes and wrap in double quotes
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    # Otherwise use shlex.quote for safety
    return shlex.quote(value)


def get_templates_dir() -> pathlib.Path:
    """Get the path to the templates directory."""
    return pathlib.Path(__file__).parent / "templates"


def render_template(template_name: str, **kwargs) -> str:
    """Render a Jinja2 template with the given variables."""
    templates_dir = get_templates_dir()
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )
    env.filters["shell_quote"] = shell_quote_filter
    template = env.get_template(template_name)
    return template.render(**kwargs).strip()


def create_boilerplate_command(
    folder_name: str, output_folder: str, template_url: str
) -> str:
    """Create the boilerplate creation command."""
    return render_template(
        "create_boilerplate.j2",
        folder_name=folder_name,
        output_folder=output_folder,
        template_url=template_url,
    )


def create_generate_command(
    folder_name: str, template_path: str, output_dir: str, project_name: str
) -> str:
    """Create the boilerplate generation command."""
    return render_template(
        "generate_boilerplate.j2",
        folder_name=folder_name,
        template_path=template_path,
        output_dir=output_dir,
        project_name=project_name,
    )
