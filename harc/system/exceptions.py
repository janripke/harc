class CommandError(Exception):
    """Thrown when the execution of Command fails"""
    pass


class DatabricksTokenNotFoundError(Exception):
    """Thrown when the databricks token is not found in the configuration."""
    pass


class PluginException(Exception):
    pass