#!/usr/bin/env python3
"""从本地 Markdown 检索帖子，返回可核对的原帖链接和行号。"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
SOURCE_URL = re.compile(r"https://www\.xiaohongshu\.com/explore/([0-9a-f]{24})")
IMAGE_ONLY = "（正文仅为图片，无文字内容）"
DIRECTORY_MARKER = "<!-- 查帖.py 生成下方目录 -->\n"


@dataclass(frozen=True)
class Post:
    note_id: str
    number: str
    title: str
    published_at: str
    topics: str
    path: str
    url: str
    image_count: int
    source_status: str | None
    body_line: int
    body: str

    @property
    def image_only(self):
        return self.body == IMAGE_ONLY


def read_post(path):
    number, dash, _ = path.stem.partition("-")
    header, divider, text = path.read_text(encoding="utf-8-sig").partition("\n---\n")
    heading = header.split("\n", 1)[0]
    fields = dict(re.findall(r"(?m)^- ([^：\n]+)：([^\n]*)$", header))
    url = fields.get("链接", "")
    source = SOURCE_URL.fullmatch(url)
    images = re.fullmatch(r"图文（(\d+) 张图片）", fields.get("类型", ""))
    text_after_blanks = text.lstrip("\n")
    body = text_after_blanks.rstrip("\n")
    topics = fields.get("话题", "")
    if not (dash and number.isdecimal() and heading.startswith("# ") and heading[2:].strip()):
        raise ValueError(f"{path.name} 的序号或标题格式有误")
    if not (source and images and fields.get("发布时间") and divider and body.strip()):
        raise ValueError(f"{path.name} 缺少有效的链接、类型、发布时间或正文")

    return Post(
        note_id=source[1],
        number=number,
        title=heading[2:],
        published_at=fields["发布时间"],
        topics="" if topics == "（无）" else topics,
        path=path.relative_to(ROOT).as_posix(),
        url=url,
        image_count=int(images[1]),
        source_status=fields.get("来源状态"),
        body_line=header.count("\n") + 3 + len(text) - len(text_after_blanks),
        body=body,
    )


def read_posts():
    paths = sorted((ROOT / "帖子").glob("*.md"))
    if not paths:
        raise ValueError("帖子目录里没有 Markdown 文件")
    posts = [read_post(path) for path in paths]
    if len({post.note_id for post in posts}) != len(posts):
        raise ValueError("帖子目录里有重复的原帖 ID")
    if len({post.number for post in posts}) != len(posts):
        raise ValueError("帖子目录里有重复的本地序号")
    return sorted(posts, key=lambda post: post.published_at, reverse=True)


def normalize(text):
    folded = unicodedata.normalize("NFKC", text).casefold().replace("\u200b", "")
    return " ".join(folded.split())


def score(post, terms):
    fields = (
        (normalize(post.title), 5),
        (normalize(post.topics), 3),
        (normalize(post.body) if not post.image_only else "", 1),
    )
    ranking = 0
    for term in terms:
        weight = sum(weight for field, weight in fields if term in field)
        if not weight:
            return 0
        ranking += weight
    return ranking


def result(post, terms):
    line_number = 1
    excerpt = None
    if not post.image_only:
        lines = ((line, text.strip()) for line, text in enumerate(post.body.split("\n"), post.body_line))
        line_number, content = max(lines, key=lambda pair: sum(term in normalize(pair[1]) for term in terms))
        positions = [match.start() for term in terms if (match := re.search(re.escape(term), content, re.IGNORECASE))]
        start = max(0, min(positions, default=0) - 35)
        end = start + 120
        excerpt = ("…" if start else "") + content[start:end] + ("…" if len(content) > end else "")

    return {
        "note_id": post.note_id,
        "number": post.number,
        "title": post.title,
        "published_at": post.published_at,
        "path": post.path,
        "line": line_number,
        "source_url": post.url,
        "source_status": post.source_status,
        "body_status": "仅图片" if post.image_only else "有文字",
        "image_count": post.image_count,
        "excerpt": excerpt,
    }


def refresh_index(posts):
    path = ROOT / "索引.md"
    intro, marker, _ = path.read_text(encoding="utf-8").partition(DIRECTORY_MARKER)
    if not marker:
        raise ValueError("索引.md 缺少目录标记")
    rows = ["| 序号 | 发布时间 | 本地帖子 | 原帖 | 状态 |", "| --- | --- | --- | --- | --- |"]
    for post in posts:
        title = post.title.replace("|", r"\|").replace("[", r"\[").replace("]", r"\]")
        target = quote(post.path)
        status = ["仅图片"] if post.image_only else []
        if post.source_status:
            status.append(post.source_status.replace("|", r"\|"))
        rows.append(
            f"| {post.number} | {post.published_at} | [{title}]({target}) | "
            f"[原帖]({post.url}) | {'、'.join(status)} |"
        )
    with TemporaryDirectory(dir=ROOT, prefix=".目录-") as temp:
        updated = Path(temp) / path.name
        updated.write_text(intro + marker + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
        updated.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--id", metavar="ID", help="用原帖 ID、原帖链接或本地序号直查")
    mode.add_argument("--refresh-index", action="store_true", help="刷新索引.md 中的帖子目录")
    parser.add_argument("keywords", nargs="*", help="同时匹配标题、话题或正文中的关键词")
    parser.add_argument("--limit", type=int, default=5, help="最多显示的结果数，默认 5")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    terms = tuple(dict.fromkeys(filter(None, map(normalize, args.keywords))))
    if (terms and (args.id or args.refresh_index)) or not (terms or args.id or args.refresh_index):
        parser.error("请使用关键词、--id 或 --refresh-index 中的一种")
    if args.limit < 1:
        parser.error("--limit 必须大于 0")

    try:
        posts = read_posts()
        if args.refresh_index:
            refresh_index(posts)
            print(f"已更新索引.md，共 {len(posts)} 篇。")
            return
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")

    if args.id:
        ref = args.id.strip().split("?", 1)[0].split("#", 1)[0].rstrip("/").casefold()
        matches = [post for post in posts if ref in (post.note_id, post.number, post.url)]
    else:
        ranked = [(score(post, terms), post) for post in posts]
        ranked.sort(key=lambda item: item[0], reverse=True)
        matches = [post for weight, post in ranked if weight]

    results = [result(post, terms) for post in matches[: args.limit]]
    if args.json:
        print(json.dumps({"total": len(matches), "posts": results}, ensure_ascii=False))
        return
    print(f"匹配 {len(matches)} 篇，显示 {len(results)} 篇。")
    for item in results:
        print(f"\n{item['number']} 《{item['title']}》 · {item['published_at']}")
        print(f"{item['path']}:{item['line']}")
        print(item["source_url"])
        if item["source_status"]:
            print(item["source_status"])
        print(item["excerpt"] if item["excerpt"] else f"仅图片（{item['image_count']} 张），本地未存图片。")


if __name__ == "__main__":
    main()
