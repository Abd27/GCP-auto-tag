import re

def get_resource_name(path: str):
    regex = ".*\/(.*)"
    name = re.search(regex, path).group(1)
    return name