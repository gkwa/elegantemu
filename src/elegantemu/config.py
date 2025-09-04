import importlib.metadata
import os
import shlex
import sys
import tempfile

import elegantemu.logging_config

# Configuration schema with defaults and descriptions
CONFIG_SCHEMA = {
    "ELEGANTEMU_OUTPUT_FOLDER": {
        "arg_name": "output_folder",
        "prompt": "Output folder for boilerplate",
        "example": "/path/to/output/folder",
        "default": None,
    },
    "ELEGANTEMU_TEMPLATE_URL": {
        "arg_name": "template_url",
        "prompt": "Template URL",
        "example": "github.com/user/repo/template",
        "default": None,
    },
    "ELEGANTEMU_TEMPLATE_BASE": {
        "arg_name": "template_base",
        "prompt": "Base path for templates",
        "example": "/path/to/templates",
        "default": None,
    },
    "ELEGANTEMU_TEMPLATE_URL_BASE": {
        "arg_name": "template_url_base",
        "prompt": "Base URL for template URLs",
        "example": "github.com/user/repo",
        "default": None,
    },
    "ELEGANTEMU_OUTPUT_DIR": {
        "arg_name": "output_dir",
        "prompt": "Output directory for generated files",
        "example": tempfile.gettempdir(),
        "default": tempfile.gettempdir(),
    },
    "ELEGANTEMU_PROJECT_NAME": {
        "arg_name": "project_name",
        "prompt": "Project name variable",
        "example": "stuff",
        "default": "stuff",
    },
}


def get_missing_env_vars(args) -> list[str]:
    """Return list of missing environment variables."""
    logger = elegantemu.logging_config.get_logger(__name__)
    missing = []

    for env_var, config in CONFIG_SCHEMA.items():
        arg_value = getattr(args, config["arg_name"])
        env_value = os.environ.get(env_var)

        logger.debug("Checking %s: arg=%s, env=%s", env_var, arg_value, env_value)

        if not arg_value and not env_value:
            missing.append(env_var)

    return missing


def suggest_env_vars(missing_vars: list[str], original_args: list[str]) -> str:
    """Generate suggestion string for setting environment variables."""
    logger = elegantemu.logging_config.get_logger(__name__)

    suggestions = []
    for var in missing_vars:
        example = CONFIG_SCHEMA[var]["example"]
        quoted_example = shlex.quote(example)
        suggestions.append(f"{var}={quoted_example}")
        logger.debug("Suggesting %s=%s", var, quoted_example)

    env_vars = " ".join(suggestions)
    app_name = get_app_name()
    # Skip the first argument (which is the script path) and use the rest
    user_args = " ".join(shlex.quote(arg) for arg in original_args[1:])
    command = f"{app_name} {user_args}"

    return (
        f"Missing environment variables. Try setting them like this:\n"
        f"{env_vars} {command}"
    )


def get_env_or_prompt(env_var: str, prompt_msg: str, default: str = "") -> str:
    """Get value from environment variable or prompt user if not present."""
    logger = elegantemu.logging_config.get_logger(__name__)

    value = os.environ.get(env_var)
    if value:
        logger.debug("Got %s from environment: '%s'", env_var, value)
        return value

    logger.info("Prompting for %s", env_var)

    try:
        if default:
            user_input = input(f"{prompt_msg} (default: {default}): ").strip()
            result = user_input if user_input else default
            logger.debug("User provided value for %s: '%s'", env_var, result)
            return result
        while True:
            user_input = input(f"{prompt_msg}: ").strip()
            if user_input:
                logger.debug("User provided value for %s: '%s'", env_var, user_input)
                return user_input
            logger.warning("This value is required.")
    except KeyboardInterrupt:
        logger.info("Cancelled by user (KeyboardInterrupt)")
        sys.exit(0)
    except EOFError:
        logger.info("Cancelled by user (EOF)")
        sys.exit(0)


def get_config_values(args) -> dict[str, str]:
    """Get all configuration values from args, env vars, or prompts."""
    logger = elegantemu.logging_config.get_logger(__name__)
    logger.debug("Getting configuration values")

    config = {}
    for env_var, schema in CONFIG_SCHEMA.items():
        arg_value = getattr(args, schema["arg_name"])
        config[schema["arg_name"]] = arg_value or get_env_or_prompt(
            env_var, schema["prompt"], schema["default"] or ""
        )

    logger.debug("Final configuration: %s", config)
    return config


def get_app_name() -> str:
    """Get the application name from package metadata."""
    try:
        # Get the package name from importlib.metadata
        return importlib.metadata.metadata(__package__ or __name__.split(".")[0])[
            "Name"
        ]
    except (importlib.metadata.PackageNotFoundError, KeyError):
        # Fallback to the package name if metadata is not available
        package_name = __package__ or __name__.split(".")[0]
        return package_name
