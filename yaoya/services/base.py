from yaoya.exceptions import YaoyaError


class NotFoundError(YaoyaError):
    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
