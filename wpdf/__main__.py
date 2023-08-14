from argparse import ArgumentParser

import wpdf.wattpad as wp
from wpdf.document import Document, FontSet


def main():
    args = ArgumentParser('wpdf')

    story_or_chapters = args.add_mutually_exclusive_group(required=True)
    story_or_chapters.add_argument('-s', '--story', help='Wattpad story ID to fetch all chapters from')
    story_or_chapters.add_argument('-c', '--chapters', nargs='+', help='Wattpad chapter IDs to fetch')

    default_fonts = '/usr/share/fonts/noto/NotoSans-{variation}.ttf'

    font_settings = args.add_mutually_exclusive_group()
    font_settings.add_argument('-f', '--font-template', help=f'Font filename template to use (default: {default_fonts})',
                               default=default_fonts)
    manual_fonts = font_settings.add_argument_group()
    manual_fonts.add_argument('-R', '--font-regular', help='Filename for the Regular font variation to use')
    manual_fonts.add_argument('-B', '--font-bold', help='Filename for the Bold font variation to use')
    manual_fonts.add_argument('-I', '--font-italic', help='Filename for the Italic font variation to use')

    args.add_argument('-o', '--output', required=True, help='Output filename')
    args.add_argument('--toc-length', type=int, default=2, help='Table of Contents length in pages')
    args = args.parse_args()

    if args.story:
        story = wp.story_by_id(args.story)
        parts = story.parts
    else:
        parts = [wp.part_by_id(part) for part in args.chapters]
        stories = {part.groupId for part in parts}

        assert len(stories) == 1
        story = wp.story_by_id(stories.pop())

    if args.font_template:
        fonts = FontSet(
            regular=args.font_template.format(variation='Regular'),
            bold=args.font_template.format(variation='Bold'),
            italic=args.font_template.format(variation='Italic')
        )
    else:
        fonts = FontSet(regular=args.font_regular, bold=args.font_bold, italic=args.font_italic)

    doc = Document(fonts)

    if story.cover:
        doc.add_cover(story.cover)
    doc.add_toc_page(story.title, args.toc_length)

    for part in parts:
        html = wp.story_part_text(part)
        doc.add_chapter(part.title, html)

    doc.output(args.output)


main()
