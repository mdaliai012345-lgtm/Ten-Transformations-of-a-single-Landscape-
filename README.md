One Landscape, Ten Visual Transformations

* A visible study of pixels, arrays and modular image operations.

One source image. Independent edits. One labeled visual summary.

Overview

*This project loads a single landscape photograph, applies a set of independent transformations to it, and assembles the results into one labeled collage. The collage doubles as a visual test suite: each tile is a named operation, so unexpected output is easy to spot at a glance.

Pipeline

Each stage has one job, so the workflow can be inspected, reordered, or extended without rewriting the whole process.

*Load: read the source image into an RGB array.
*Resize: create a consistent base image for all tiles.
*Transform: apply one operation per function.
*Assemble: grid the outputs and save the collage.

 Transformations
Operation	How it works
Darker	Subtract a fixed amount, then clip to 0-255
Brighter	Add a fixed amount, then clip to 0-255
Grayscale	Weighted RGB channels combined into one luminance value
Negative	Each pixel inverted against 255
Flips	Horizontal and vertical flips via array slicing
Rotation	Array rotation without rebuilding the image
Channel isolation	Red, green and blue contributions shown separately
Center crop	Shared crop that keeps the visual field consistent across edits

Clipping after brightness changes prevents overflow and keeps the image displayable.

Why a collage?
*Named: every tile is labeled with its operation.
*Visible: mistakes show up immediately.
*Reusable: add more filters or swap in a new source image with the same structure.
