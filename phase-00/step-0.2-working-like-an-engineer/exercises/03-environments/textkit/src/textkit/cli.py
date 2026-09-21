"""The console entry point. Argument parsing and printing live here only."""

import click

from textkit.core import word_count


@click.command()
@click.argument("text")
def main(text: str) -> None:
    """Print each word in TEXT and how often it appears."""
    for word, count in word_count(text).items():
        click.echo(f"{word} {count}")


if __name__ == "__main__":
    main()
