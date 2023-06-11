def get_matching_module(modules: list[str], snippet: str) -> str | None:
    """
    Finds the correct module to a snippet

    :param modules: A list of known modules.
    :param snippet: A snippet of a module string.
    :return: The matching module string or `None`.
    """
    for module in modules:
        if snippet == module.split('.')[-1]:
            return module
    return None
