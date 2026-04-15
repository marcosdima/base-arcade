from ..helper import Helper


class Tags(Helper):
    def setup(self):
        super().setup()

        self.tags: set[str] = set()


    def add(self, tag: str):
        self.tags.add(tag)


    def remove(self, tag: str):
        self.tags.discard(tag)


    def has(self, tag: str) -> bool:
        return tag in self.tags