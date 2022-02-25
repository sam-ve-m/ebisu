def pipe_to_list(data: str):
    list_data = None
    if data:
        data = data.upper()
        list_data = data.split('|')
    return list_data
