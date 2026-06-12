"""Fetch latest YouTube videos from RSS and update README.md."""
import xml.etree.ElementTree as ET
import urllib.request
import re
import sys

CHANNEL_ID = "UCSm3rF8rQ7ftp8hZ7tvqiaw"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
README = "README.md"

try:
    feed = urllib.request.urlopen(FEED_URL, timeout=15).read()
except Exception as e:
    print(f"❌ Failed to fetch RSS feed: {e}")
    sys.exit(0)  # soft fail — don't break the workflow

root = ET.fromstring(feed)
ns = {"atom": "http://www.w3.org/2005/Atom"}
entries = root.findall("atom:entry", ns)[:3]

videos_html = ""
for entry in entries:
    title = entry.find("atom:title", ns).text
    link = entry.find("atom:link", ns).attrib["href"]
    video_id = link.split("v=")[-1]
    escaped_title = title.replace("'", "").replace('"', "")
    videos_html += (
        f"<a href='{link}'>"
        f"<img width='250' src='https://img.youtube.com/vi/{video_id}/mqdefault.jpg' "
        f"alt='{escaped_title}' title='{escaped_title}'>"
        f"</a>\n"
    )

new_section = (
    "<!-- YOUTUBE:START -->\n"
    '<p align="center">\n'
    f"{videos_html}"
    "</p>\n"
    "<!-- YOUTUBE:END -->"
)

with open(README, "r") as f:
    content = f.read()

content = re.sub(
    r"<!-- YOUTUBE:START -->.*?<!-- YOUTUBE:END -->",
    new_section,
    content,
    flags=re.DOTALL,
)

with open(README, "w") as f:
    f.write(content)

print("✅ README updated with latest YouTube videos")
