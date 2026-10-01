class Post:

    def __init__(
        self, rank: int, title: str, url: str, points: int = 0, comments: int = 0
    ) -> None:
        self.rank: int = rank
        self.title: str = title
        self.url: str = url
        self.points: int = points
        self.comments: int = comments

    def to_dict(self) -> dict[str, str | int]:
        return {
            "rank": self.rank,
            "title": self.title,
            "url": self.url,
            "points": self.points,
            "comments": self.comments,
        }

    def __str__(self) -> str:
        return f"#{self.rank} [{self.points} pts] {self.title.title()} ({self.comments} comments)"
