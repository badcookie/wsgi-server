def parse_query_string(line: str) -> dict:
    pairs = line.split('&')
    params = (item.split('=') for item in pairs)
    return {param: value for param, value in params}
