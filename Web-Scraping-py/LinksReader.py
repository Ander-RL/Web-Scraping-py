class LinksReader:

    def __init__(self):
        self.link_list = list()
        self.file_path = ".\\Links.txt"
        self.fill_list(self.file_path)

    def get_link_list(self):
        return self.link_list

    def set_link_list(self, link_list):
        self.link_list = link_list

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path

    def fill_list(self, file_path):
        with open(file_path, "r") as handler:
            for line in handler:
                self.link_list.append(line)

    def print_list(self, file_path):
        print(self.link_list)