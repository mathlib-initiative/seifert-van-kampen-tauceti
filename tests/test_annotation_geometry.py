"""Keep the nested underbrace link inside its displayed equation."""
import json
from pathlib import Path
import unittest


class PublishedGeometry(unittest.TestCase):
    def test_middle_underbrace_highlight_stays_inside_equation(self):
        root = Path(__file__).resolve().parents[1]
        bundle = json.loads((root / "pdf-overlay/annotations.bundle.json").read_text())
        records = {row["annotation"]["id"]: row["annotation"] for row in bundle["annotations"]}
        equation = records["proof-3.1-s04-factorization"]["subject"][0]["location"]
        x, y, width, height = equation["rect"]
        for subject in records["proof-3.1-s05-middle"]["subject"]:
            label = subject["location"]
            lx, ly, lw, lh = label["rect"]
            self.assertEqual(label["page"], equation["page"])
            self.assertGreaterEqual(lx + 1e-6, x)
            self.assertGreaterEqual(ly + 1e-6, y)
            self.assertLessEqual(lx + lw, x + width + 1e-6)
            self.assertLessEqual(ly + lh, y + height + 1e-6)
