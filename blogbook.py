from datetime import datetime
import feedparser
import weasyprint
import click
from rich.progress import Progress
from rich.console import Console

import locale
locale.setlocale(locale.LC_ALL, '')


def get_entries(base_url, platform):
    if platform.lower() == "blogspot":
        feed_url = base_url + "/feeds/posts/default/"
    else:
        feed_url = base_url + "/feed/atom/"

    index = 1
    page = 1
    all_entries = []
    with Progress(transient=True) as progress:
        while True:
            if platform.lower() == "blogspot":
                url = f"{feed_url}?start-index={index}"
            else:
                url = f"{feed_url}?paged={page}"

            feed = feedparser.parse(url)
            
            if platform.lower() == "blogspot":
                total_results = int(feed.feed.opensearch_totalresults)
                if index == 1:
                    task = progress.add_task("Downloading feed", total=total_results)

                progress.advance(task, len(feed.entries))
            else:  # For wordpress
                print(f"Downloading page {page}")

            all_entries.extend(feed.entries)

            index += len(feed.entries)
            page += 1

            if len(feed.entries) == 0:
                break

    all_entries.reverse()

    return all_entries


def print_entry_summary(entries):
    entry_index = 1
    for entry in entries:
        tags = "[None]"
        if "tags" in entry.keys():
            tags = [tag.term for tag in entry.tags]
        print(f"[{entry_index}] ({entry.published[:10]}) {entry.title} {tags}")
        entry_index += 1


def convert_to_pdf(entries, platform, output_filename,):
    entry_index = 1
    all_text = ""
    for entry in entries:
        tags = "[None]"
        if "tags" in entry.keys():
            tags = [tag.term for tag in entry.tags]
        print(f"[{entry_index}] ({entry.published[:10]}) {entry.title} {tags}")
        entry_index += 1

        if platform.lower() == 'blogspot':
            date = datetime.fromisoformat(entry.published)
            date_str = date.strftime("%c").capitalize()
        else:  # Wordpress
            date_str = entry.published
        headers = f"<h1>{entry.title}</h1>\n\n<h2>{date_str}</h2>"
        all_text += headers  + entry.content[0].value + "\n\n"

    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"

    console = Console()
    with console.status("Generating PDF...") as status:
        weasyprint.HTML(string=all_text).write_pdf(output_filename)


@click.command()
@click.option('--base-url', type=str, required=True,
    help='Base URL of the blog. For instance: http://example.blogspot.com')
@click.option('--output', type=str, default="output.pdf", show_default=True,
    help='Output file name')
@click.option('--platform', type=click.Choice(['Blogspot', "Wordpress"],
    case_sensitive=False), required=True,
    help='Platform used to host the blog')
def main(base_url, output, platform):
    entries = get_entries(base_url, platform)
    convert_to_pdf(entries, platform, output)


if __name__ == "__main__":
    main()
