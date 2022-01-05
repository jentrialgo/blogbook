# Blog book

Blog book is a python scripts that converts Blogspot or Wordpress blogs into PDF
files to be printed like a book. It uses their RSS feed.

# Usage

```bash
python blogbook.py --base-url https://example.blogspot.com --platform Blogspot
```

See all options with:

```bash
python blogbook.py --help

Usage: blogbook.py [OPTIONS]

Options:
  --base-url TEXT                 Base URL of the blog. For instance:
                                  http://example.blogspot.com  [required]
  --output TEXT                   Output file name  [default: output.pdf]
  --platform [Blogspot|Wordpress]
                                  Platform used to host the blog  [required]
  --tag TEXT                      Only the posts with that tag (or tags if the
                                  option is repeated) will be included
  --help                          Show this message and exit.
```
