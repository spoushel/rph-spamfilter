import os

class Corpus:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def emails(self):
        for filename in os.listdir(self.path_to_file):
            if filename.startswith("!"):
                continue
            file_path = os.path.join(self.path_to_file, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                body = file.read()
            
            yield filename, body
