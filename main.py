from config import BASE_URL, CSV_FILE, DIVIDER_WIDTH, APP_NAME, EXCEL_FILE
from exceptions import FetchError, ParseError, ExportError
from core.scraper import create_session, scrape_multiple_pages
from core.export import export_posts
from core.filters import apply_filters


def parse_optional_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        print("  ⚠️  Not a valid number — skipping this filter.")
        return None


def run() -> None:
    print("=" * DIVIDER_WIDTH)
    print(f"  {APP_NAME.upper()}")
    print("=" * DIVIDER_WIDTH)

    session = create_session()

    try:
        posts   = scrape_multiple_pages(session, BASE_URL)
        print(f"  Scraped {len(posts)} posts")

        filter_choice = input("\n  Filter results? (yes/no): ").strip().lower()
        filtered_posts = posts

        if filter_choice in ("yes", "y"):
            keyword = input("  Keyword (or Enter to skip): ").strip().lower() 
            min_points = parse_optional_int("  Minimum points (or Enter to skip): ")
            min_comments = parse_optional_int("  Minimum comments (or Enter to skip): ")

            filtered_posts = apply_filters(posts, keyword=keyword, min_points=min_points, min_comments=min_comments)
        print(f"  Filtered to {len(filtered_posts)} posts (from {len(posts)})")

        if filter_choice in ("yes" "y") and not filtered_posts:
            proceed = input("\n  No matches. Continue with unfiltered result? (yes/no): ").strip().lower()
            if proceed in ("yes", "y"):
                filtered_posts = posts
            else:
                filtered_posts = []

        export_fmt = input("\n  Export format? (csv/excel/both/skip): ").strip().lower()
        if export_fmt != "skip":
            try:
                written = export_posts(filtered_posts, export_fmt, CSV_FILE, EXCEL_FILE)
                print(f"  ✅ Exported to: {', '.join(written)}")
            except ExportError as e:
                print(f"  ❌ Export failed: {e}")
            except ValueError as e:
                print(f"  ❌ {e}")

        print("\n  Top 10 posts")
        for post in sorted(filtered_posts, key=lambda x: x.points, reverse=True)[:10]:
            print(f"    {post}")

    except (FetchError, ParseError) as e:
        print(e)
    except KeyboardInterrupt:
        print("  Goodbye")


if __name__ == "__main__":
    run()
