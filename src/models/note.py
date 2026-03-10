from .fields import Tag


class Note:
    def __init__(self, title, content=""):
        self.title = title
        self.content = content
        self.tags = []

    def edit(self, new_content):
        pass

    def add_tag(self, tag):
        pass

    def remove_tag(self, tag):
        pass

    def __str__(self):
        pass
