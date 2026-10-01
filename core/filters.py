def filter_by_keyword(posts: list[object] | list[None], keyword: str) -> list[object] | list[None]:
    return [post for post in posts if keyword.lower() in post.title.lower()]


def filter_by_min_points(posts: list[object] | list[None], min_points: int) -> list[object] | list[None]:
    return [post for post in posts if post.points >= min_points]


def filter_by_min_comments(posts: list[object] | list[None], min_comments:  int) -> list[object] | list[None]:
    return [post for post in posts if post.comments >= min_comments]


def apply_filters(posts: list[object] | list[None], keyword: str | None = None, min_points: int | None = None, min_comments: int | None= None) -> list[object] | list[None]:
    result = posts

    if keyword is not None:
        result = filter_by_keyword(result, keyword)
    if min_points is not None:
        result = filter_by_min_points(result, min_points)
    if min_comments is not None:
        result = filter_by_min_comments(result, min_comments)
        
    return result
