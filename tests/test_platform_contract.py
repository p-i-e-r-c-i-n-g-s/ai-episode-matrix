import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class PlatformContractTests(unittest.TestCase):
    """Offline integration contracts; live generation is intentionally opt-in."""

    def test_adapter_requires_reference_preservation_and_unverified_controls(self):
        text = (ROOT / "references/platform-adapters.md").read_text()
        for field in ("ENGINE:", "INPUT:", "REFERENCE INSTRUCTION:", "MOTION INSTRUCTION:", "CONTROLS:", "UNVERIFIED:"):
            self.assertIn(field, text)
        self.assertIn("Never invent a parameter", text)

    def test_image_to_video_example_obeys_preserve_animate_contract(self):
        text = (ROOT / "examples/image-to-video.md").read_text()
        normalized = text.lower()
        for field in ("preserve", "animate", "no scene change", "success criteria"):
            self.assertIn(field, normalized)


if __name__ == "__main__":
    unittest.main()
