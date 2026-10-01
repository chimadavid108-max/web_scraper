class ScraperError(Exception):
    pass


class ParseError(ScraperError):
    pass


class FetchError(ScraperError):
    pass


class ExportError(ScraperError):
    pass
