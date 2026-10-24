# Figure assets

Only referenced SVG figures are retained.

Run `python redesign.py` to regenerate the H/E diagrams. The generator only outputs SVG names referenced by the parent Markdown slides.

`fig-i-circle.svg` and `fig-f-cuts.svg` are independently maintained assets.

Publish the SVG files alongside the HTML, retaining this folder structure.

`matching_overview.py`: regenerate the DFS overview and sparse/dense graph comparison.

`hopcroft_karp.py`: regenerate the Hopcroft–Karp BFS layers and simultaneous augmentation diagrams.

`hk_walkthrough.py`: current simplified two-stage Hopcroft–Karp figures.
