
HN Scraper 
==========

A command-line tool that scrapes the Hacker News front page (first 3 pages by default), lets you filter the results, and exports them to CSV and/or Excel.

Features
--------
- Scrapes rank, title, URL, points and comment count for each post
- Follows the "More" link across multiple pages, with a polite delay between requests
- Optional filtering by title keyword, minimum points and minimum comments
- Exports to CSV, Excel (.xlsx) or both
- Excel output has a bold header row and auto-sized columns
- Prints the top 10 posts by points when finished

Requirements
------------
Python 3.10 or newer (the code uses the X | Y type syntax).

Install the dependencies:

    pip install requests beautifulsoup4 lxml openpyxl

Usage
-----
Run from the project folder:

    python main.py

You will be prompted for:

1. Filter results? (yes/no)
   If yes, you can enter a keyword, a minimum points value and a minimum comments value. Press Enter to skip any of them.
2. Export format? (csv/excel/both/skip)
   Files are written to the project folder.

Example output files: hn_posts.csv and hn_posts.xlsx

Output columns
--------------
rank, title, url, points, comments

Project structure
-----------------
    web_scraper_project/
        main.py          Entry point and interactive prompts
        config.py        Settings (URL, file names, timeout, user agent)
        exceptions.py    Custom errors: ScraperError, FetchError, ParseError, ExportError
        core/
            models.py    Post class (one scraped post)
            scraper.py   Session setup, page fetching, HTML parsing, multi-page scraping
            filters.py   Keyword / points / comments filters
            export.py    CSV and Excel writers

Configuration
-------------
Edit config.py to change:

    APP_NAME       Name shown in the banner
    BASE_URL       Page to start scraping from
    CSV_FILE       CSV output file name
    EXCEL_FILE     Excel output file name
    TIMEOUT        Request timeout in seconds
    USER_AGENT     Sent with every request

The number of pages and the delay between requests are arguments of scrape_multiple_pages() in core/scraper.py (defaults: max_pages=3, delay=2 seconds).

How it works
------------
1. create_session() builds a requests session with your User-Agent.
2. scrape_multiple_pages() fetches each page, parses it with BeautifulSoup (lxml), and follows the "More" link until it reaches the page limit.
3. apply_filters() narrows the list based on your answers.
4. export_posts() writes the chosen format(s).

Errors are handled with custom exceptions: a failed fetch stops scraping and keeps whatever was already collected, and export problems are reported without crashing the program.

Notes on responsible scraping
-----------------------------
- Keep the delay between requests so you don't hammer the site.
- Update USER_AGENT with your own contact details.
- Hacker News also offers an official API, which is the better choice for heavy or frequent use.

Limitations
-----------
- Depends on Hacker News's current HTML structure; a site redesign could break the parser.
- Ranks in the output are counted across pages by the scraper, so they may skip numbers if a post row is missing a link.
