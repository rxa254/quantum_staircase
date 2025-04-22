import argparse
from pathlib import Path
from quantum_staircase import utils, patterns

def main():
    parser = argparse.ArgumentParser(description="Quantum Staircase panel exporter")
    parser.add_argument("--theme", required=True, choices=patterns.list_themes(), help="Pattern theme")
    parser.add_argument("--outfile", required=True, help="Output image (PNG/SVG)")
    parser.add_argument("--panel-size-m", type=float, default=3.0, help="Panel size in metres (square)")
    parser.add_argument("--resolution-mm", type=float, default=1.0, help="Pixel resolution in mm")
    args = parser.parse_args()

    pattern_func = patterns.get_theme(args.theme)
    arr = pattern_func(args.panel_size_m, args.resolution_mm)
    img_path = Path(args.outfile)
    utils.export.save_image(arr, img_path, args.panel_size_m, args.resolution_mm)
    print(f"Saved {img_path.resolve()}")
