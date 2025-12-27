def read_classification_from_file(file_path):
    # Create dict {filename: OK/SPAM}
    final_dict = {}
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.read().split("\n")

    for line in lines:
        elements = line.split()
        if len(elements) == 2:
            filename, status = elements
            final_dict[filename] = status

    return final_dict