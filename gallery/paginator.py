class Paginator:
    def __init__(self, page: str, limit: str, url: str) -> None:
        self.page = self.validate(page, "page")
        self.limit = self.validate(limit, "limit")
        self.url = url

    @property
    def next_num(self):
        return self.page + 1

    @property
    def prev_num(self):
        return 0 if self.page == 0 else self.page - 1

    @property
    def next_page(self):
        return f"{self.url}?page={self.next_num}&limit={self.limit}"

    @property
    def previous_page(self):
        return f"{self.url}?page={self.prev_num}&limit={self.limit}"

    def validate(self, value, name):
        try:
            value = int(value)
            value = 0 if value < 0 else value
            return value
        except ValueError:
            raise Exception(message=f"Url Arg: {name}, must be integer")
