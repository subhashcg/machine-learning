"""3. resize(image, width, height, *, keep_ratio=True, upscale=False)

It need not resize anything — return a description string. The point is the
signature.

Show that resize("img", 800, 600, True, False) raises, and say in a comment why
refusing that call is a feature.
"""


def resize(image, width, height, *, keep_ratio=True, upscale=False):
    # TODO — return a string describing what would happen
    pass


if __name__ == "__main__":
    print(resize("photo.jpg", 800, 600))
    print(resize("photo.jpg", 800, 600, keep_ratio=False, upscale=True))

    # TODO: show the positional call being refused, and why that is a feature
