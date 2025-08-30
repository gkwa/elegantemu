import typing

import elegantemu.commands


class ConfigDict(typing.TypedDict):
    """Type definition for configuration dictionary."""

    output_folder: str
    template_url: str
    template_base: str
    template_url_base: str
    output_dir: str
    project_name: str


def generate_boilerplate_commands(folder_name: str, **config: str) -> str:
    """Generate boilerplate commands and return as string."""
    # Create command
    create_cmd = elegantemu.commands.create_boilerplate_command(
        folder_name=folder_name,
        output_folder=config["output_folder"],
        template_url=config["template_url"],
    )
    # Generate command using local template path
    generate_local_cmd = elegantemu.commands.create_generate_command(
        folder_name=folder_name,
        template_path=f"{config['template_base']}/$FOLDER_NAME",
        output_dir=config["output_dir"],
        project_name=config["project_name"],
    )
    # Generate command using URL template path
    generate_url_cmd = elegantemu.commands.create_generate_command(
        folder_name=folder_name,
        template_path=f"{config['template_url_base']}/$FOLDER_NAME",
        output_dir=config["output_dir"],
        project_name=config["project_name"],
    )

    output_lines = [
        "# Create new boilerplate item",
        create_cmd,
        "",
        "# Generate and view template output (local)",
        generate_local_cmd,
        "",
        "# Generate and view template output (URL)",
        generate_url_cmd,
    ]

    return "\n".join(output_lines)
