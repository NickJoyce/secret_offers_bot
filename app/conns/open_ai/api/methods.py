class Methods():
    def __init__(self, base_url):
        self.base_url = base_url

    @property
    def responses(self):
        return f"{self.base_url}/responses"

