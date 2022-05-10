from yaoya.sesseion import StreamlitSessionManager


class BasePage:
    def __init__(self, page_id: str, title: str, ssm: StreamlitSessionManager) -> None:
        self.page_id = page_id
        self.title = title
        self.ssm = ssm

    def render(self) -> None:
        pass
