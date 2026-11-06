import os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")  # remove this line if you want plt.show() windows
import matplotlib.pyplot as plt

IMAGE_PATH = "imagesss/sample.jpg"
TILE_W, TILE_H = 400, 300      # every tile is resized to this
COLS = 4
BORDER = 6                     # white gap between tiles


# ---------- load ----------
def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    return np.array(Image.open(path).convert("RGB"))


def resize(arr, w=TILE_W, h=TILE_H):
    return np.array(Image.fromarray(arr).resize((w, h)))


def info(arr):
    print("------------INFORMATION--ABOUT-IMAGES------------")
    print("Shape", arr.shape)
    print("Dimension", arr.ndim)
    print("Total Elements", arr.size)
    print("Datatype", arr.dtype)
    print("Height", arr.shape[0])
    print("Width", arr.shape[1])
    print("Channels", arr.shape[2])
    print()


# ---------- edits (your code, fixed) ----------
def darker(a, amount=50):
    return np.clip(a.astype(np.int16) - amount, 0, 255).astype(np.uint8)


def brighter(a, amount=60):
    return np.clip(a.astype(np.int16) + amount, 0, 255).astype(np.uint8)


def grayscale(a):
    g = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    return np.stack([g, g, g], axis=2).astype(np.uint8)  # 3 channels so it stacks


def negative(a):
    return 255 - a


def flip_vertical(a):
    return a[::-1, :, :]          # your [::1] did nothing; -1 actually flips


def flip_horizontal(a):
    return a[:, ::-1, :]


def rotate_90(a):
    return np.rot90(a, 1)         # your k=4 was a full turn (no change)


def crop_center(a):
    h, w = a.shape[:2]
    return a[h // 4: 3 * h // 4, w // 4: 3 * w // 4]


def keep_channel(a, ch):
    out = np.zeros_like(a)
    out[:, :, ch] = a[:, :, ch]   # your version zeroed R and G, which leaves BLUE
    return out


# ---------- collage ----------
def make_collage(tiles, cols=COLS, border=BORDER):
    rows = []
    for i in range(0, len(tiles), cols):
        row = tiles[i:i + cols]
        while len(row) < cols:    # pad last row with white
            row.append(np.full((TILE_H, TILE_W, 3), 255, np.uint8))
        padded = []
        for t in row:
            t = np.pad(t, ((border, border), (border, border), (0, 0)),
                       constant_values=255)
            padded.append(t)
        rows.append(np.hstack(padded))
    return np.vstack(rows)


def main():
    img = load_image(IMAGE_PATH)
    info(img)

    base = resize(img)
    edits = [
        ("Original", base),
        ("Darker", darker(base)),
        ("Brighter", brighter(base)),
        ("Grayscale", grayscale(base)),
        ("Negative", negative(base)),
        ("Flip Vertical", flip_vertical(base)),
        ("Flip Horizontal", flip_horizontal(base)),
        ("Rotate 90", resize(rotate_90(base))),
        ("Cropped Center", resize(crop_center(base))),
        ("Red Only", keep_channel(base, 0)),
        ("Green Only", keep_channel(base, 1)),
        ("Blue Only", keep_channel(base, 2)),
    ]

    # 1) plain collage saved as an image
    collage = make_collage([t for _, t in edits])
    Image.fromarray(collage).save("collage.png")
    print("Saved collage.png", collage.shape)

    # 2) labeled collage with matplotlib
    rows = int(np.ceil(len(edits) / COLS))
    fig, axes = plt.subplots(rows, COLS, figsize=(4 * COLS, 3.2 * rows))
    for ax, (title, tile) in zip(axes.ravel(), edits):
        ax.imshow(tile)
        ax.set_title(title)
        ax.axis("off")
    for ax in axes.ravel()[len(edits):]:
        ax.axis("off")
    plt.tight_layout()
    plt.savefig("collage_labeled.png", dpi=120)
    print("Saved collage_labeled.png")
    # plt.show()


if __name__ == "__main__":
    main()
