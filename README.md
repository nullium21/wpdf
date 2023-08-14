# `wpdf`, a Wattpad downloader

[Wattpad](https://wattpad.com) is a, let's call it commercialized, solution.
Like, why does it want me to create an account *so bad*?
That's why this project was created -- on GitHub there seemed to be literally *zero* recently-updated tools for working with it.

## What does this support?

I'll be honest. I do *not* know all the specifics of how writers can structure their work on Wattpad.
The tool was only tested on [this story](https://www.wattpad.com/story/264410416), which only has text, and was recommended to me by a friend, and was the main reason this tool even exists.

From what it *looks like*, though, it should be fine, as the server seems to just give you the HTML for the text...

Anyway, here's a link to the [Issues](https://github.com/nullium21/wpdf/issues) tab on `wpdf`'s GitHub if you see something that's not working.

## Usage
```bash
# Display help with all supported options, autogenerated by argparse.
$ wpdf -h

# Download a full story (wattpad.com/stories/{StoryId}) into a file.
$ wpdf -o MyStory.pdf -s StoryId

# Download a full story into a file, but with a bigger-than-default Table of Contents.
$ wpdf -o MyStory.pdf -s StoryId --toc-length 5  # 5 pages

# Download a full story into a file, but with a custom font.
$ wpdf -o MyStory.pdf -s StoryId -f font-{variation}.ttf  # assumes there's `font-Regular.ttf`, `font-Bold.ttf` and `font-Italic.ttf` in the current working directory
$ wpdf -o MyStory.pdf -s StoryId -R font-Regular.ttf -B font-Bold.ttf -I font-Italic.ttf  # the same thing, but specified manually

# Download only certain chapters (of a single story, else it will crash!)
$ wpdf -o MyStory.pdf -c ChapterId ChapterId...
```
