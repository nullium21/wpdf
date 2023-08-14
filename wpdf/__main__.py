from argparse import ArgumentParser

import wpdf.wattpad as wp
from wpdf.document import Document, FontSet


def main():
    args = ArgumentParser('wpdf')

    story_or_chapters = args.add_mutually_exclusive_group(required=True)
    story_or_chapters.add_argument('-s', '--story', help='Wattpad story ID to fetch all chapters from')
    story_or_chapters.add_argument('-c', '--chapters', nargs='+', help='Wattpad chapter IDs to fetch')

    args.add_argument('-o', '--output', required=True, help='Output filename')
    args = args.parse_args()

    if args.story:
        story = wp.story_by_id(args.story)
        parts = story.parts
    else:
        parts = [wp.part_by_id(part) for part in args.chapters]
        stories = {part.groupId for part in parts}

        assert len(stories) == 1
        story = wp.story_by_id(stories.pop())

    doc = Document(FontSet(
        regular='/usr/share/fonts/noto/NotoSans-Regular.ttf',
        bold='/usr/share/fonts/noto/NotoSans-Bold.ttf',
        italic='/usr/share/fonts/noto/NotoSans-Italic.ttf'
    ))

    if story.cover:
        doc.add_cover(story.cover)
    doc.add_toc_page(story.title)

    for part in parts:  # for testing, only use first 20
        html = wp.story_part_text(part)
        doc.add_chapter(part.title, html)

    doc.output(args.output)


main()
