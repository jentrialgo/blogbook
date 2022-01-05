from datetime import datetime
import feedparser
import weasyprint
import click
from rich.progress import Progress

import locale
locale.setlocale(locale.LC_ALL, '')

def get_blogspot_entries(base_url):

    feed_url = base_url + "/feeds/posts/default/"


    index = 1
    all_entries = []
    with Progress(transient=True) as progress:
        while True:
            url = f"{feed_url}?start-index={index}"
            feed = feedparser.parse(url)
            
            total_results = int(feed.feed.opensearch_totalresults)
            if index == 1:
                task = progress.add_task("Downloading feed", total=total_results)

            all_entries.extend(feed.entries)

            index += len(feed.entries)

            progress.advance(task, len(feed.entries))

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


def convert_to_pdf(entries, output_filename):
    entry_index = 1
    all_text = ""
    for entry in entries:
        tags = "[None]"
        if "tags" in entry.keys():
            tags = [tag.term for tag in entry.tags]
        print(f"[{entry_index}] ({entry.published[:10]}) {entry.title} {tags}")
        entry_index += 1

        date = datetime.fromisoformat(entry.published)
        date_str = date.strftime("%c").capitalize()
        headers = f"<h1>{entry.title}</h1>\n\n<h2>{date_str}</h2>"
        all_text += headers  + entry.content[0].value + "\n\n"

    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"

    weasyprint.HTML(string=all_text).write_pdf(output_filename)

@click.command()
@click.option('--base-url', type=str, required=True,
    help='Base URL of the blog. For instance: http://example.blogspot.com')
@click.option('--output', type=str, default="output.pdf", show_default=True,
    help='Output file name')
def main(base_url, output):
    entries = get_blogspot_entries(base_url)
    convert_to_pdf(entries, output)


if __name__ == "__main__":
    main()
