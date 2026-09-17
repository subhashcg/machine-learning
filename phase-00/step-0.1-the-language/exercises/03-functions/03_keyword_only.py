"""3. resize(image, width, height, *, keep_ratio=True, upscale=False)

It need not resize anything — return a description string. The point is the
signature.

Show that resize("img", 800, 600, True, False) raises, and say in a comment why
refusing that call is a feature.
"""


def resize(image, width, height, *, keep_ratio=True, upscale=False):
    return f"{image} {width}*{height} (keep_ratio: {keep_ratio}, upscale: {upscale})"


if __name__ == "__main__":
    print(resize("photo.jpg", 800, 600))
    print(resize("photo.jpg", 800, 600, keep_ratio=False, upscale=True))

    try:
        # This will raise as keep_ration and upscale are expected to keyword argments. Sicne these are booleans its better to be explicit about their purpose.
        # Keyword arguments also gives the flexibility to change the functiona signature without impacting all consumers the function
        print(resize("photo.jpg", 800, 600, True, False))
    except TypeError as e:
        print(f"Keyword arguments are being passed as positional argments {e}")
