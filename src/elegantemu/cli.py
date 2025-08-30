import argparse
import sys

import elegantemu.config
import elegantemu.generator
import elegantemu.logging_config
import elegantemu.utils


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate boilerplate commands for project templates"
    )
    parser.add_argument(
        "folder",
        nargs="+",
        help="Words to create folder name from (e.g., 'my test dir')",
    )
    parser.add_argument(
        "--no-slugify",
        action="store_true",
        help="Don't convert folder name to slug format, use as-is",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v for INFO, -vv for DEBUG)",
    )
    parser.add_argument(
        "--output-folder",
        help="Output folder for boilerplate "
        "(overrides ELEGANTEMU_OUTPUT_FOLDER env var)",
    )
    parser.add_argument(
        "--template-url",
        help="Template URL (overrides ELEGANTEMU_TEMPLATE_URL env var)",
    )
    parser.add_argument(
        "--template-base",
        help="Base path for templates (overrides ELEGANTEMU_TEMPLATE_BASE env var)",
    )
    parser.add_argument(
        "--template-url-base",
        help="Base URL for template URLs "
        "(overrides ELEGANTEMU_TEMPLATE_URL_BASE env var)",
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for generated files "
        "(overrides ELEGANTEMU_OUTPUT_DIR env var)",
    )
    parser.add_argument(
        "--project-name",
        help="Project name variable (overrides ELEGANTEMU_PROJECT_NAME env var)",
    )
    return parser.parse_args()


def process_folder_name(folder_args: list[str], *, no_slugify: bool) -> str:
    """Process folder arguments into final folder name."""
    logger = elegantemu.logging_config.get_logger(__name__)

    folder_text = " ".join(folder_args)
    logger.debug("Original folder text: '%s'", folder_text)

    if no_slugify:
        logger.info("Using folder name as-is: '%s'", folder_text)
        return folder_text
    slugified = elegantemu.utils.slugify(folder_text)
    logger.info("Slugified folder name: '%s' -> '%s'", folder_text, slugified)
    return slugified


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()

    # Set up logging based on verbosity
    elegantemu.logging_config.setup_logging(args.verbose)
    logger = elegantemu.logging_config.get_logger(__name__)

    logger.debug("Arguments: %s", vars(args))

    # Check for missing environment variables and exit early if needed
    missing_vars = elegantemu.config.get_missing_env_vars(args)
    if missing_vars:
        logger.debug("Missing environment variables: %s", missing_vars)
        suggestion = elegantemu.config.suggest_env_vars(missing_vars, sys.argv)
        sys.stdout.write(f"{suggestion}\n")
        sys.exit(1)

    # Process folder name
    folder_name = process_folder_name(args.folder, no_slugify=args.no_slugify)
    logger.debug("Final folder name: '%s'", folder_name)

    # Get all configuration values
    config = elegantemu.config.get_config_values(args)
    logger.debug("Configuration: %s", config)

    # Generate and print output
    output = elegantemu.generator.generate_boilerplate_commands(
        folder_name=folder_name, **config
    )

    sys.stdout.write(f"{output}\n")


if __name__ == "__main__":
    main()
