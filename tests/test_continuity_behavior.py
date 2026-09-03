import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ContinuityBehaviorTests(unittest.TestCase):
    def test_templates_define_durable_records(self):
        templates = ROOT / "templates"
        for name in ("series-bible.yaml", "episode.yaml", "continuity-ledger.yaml", "asset-index.yaml", "session-handoff.md"):
            self.assertTrue((templates / name).exists())

    def test_quick_and_full_setup_are_distinct(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertIn("quick setup", text)
        self.assertIn("full setup", text)
        self.assertIn("defers", text.lower())

    def test_approved_state_is_the_only_canon(self):
        text = (ROOT / "references/episode-building.md").read_text()
        self.assertIn("Only `approved` state propagates as canon", text)
        self.assertIn("latest approved shot state", text)

    def test_platform_prompt_contract_preserves_continuity(self):
        text = (ROOT / "references/platform-adapters.md").read_text()
        self.assertIn("identity and asset references", text)
        self.assertIn("composition and geography", text)


if __name__ == "__main__":
    unittest.main()
