import feedparser
import click
from rich.progress import Progress

def get_blogspot_entries(base_url):

    feed_url = base_url + "/feeds/posts/default/"


    index = 1
    all_entries = []
    with Progress(transient=True) as progress:
        while True:
            url = f"{feed_url}?start-index={index}"
            feed = feedparser.parse(url)
            
            total_results = int(feed.feed.opensearch_totalresults)
            # task = progress.add_task("Downloading feed...", start=False)
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

    print(entries[0].keys())  # TODO: remove


@click.command()
@click.option('--base-url', type=str, required=True,
    help='Base URL of the blog. For instance: http://example.blogspot.com')
def main(base_url):
    entries = get_blogspot_entries(base_url)
    print_entry_summary(entries)


if __name__ == "__main__":
    main()
