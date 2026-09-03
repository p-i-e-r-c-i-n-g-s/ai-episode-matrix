import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ContinuityBehaviorTests(unittest.TestCase):
    def test_templates_define_durable_records(self):
        templates = ROOT / "templates"
        for name in ("series-bible.yaml", "episode.yaml", "continuity-ledger.yaml", "asset-index.yaml", "session-handoff.md"):
            self.assertTrue((templates / name).exists())
        self.assertTrue((templates / "video-take.yaml").exists())

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

    def test_scanner_fails_closed_for_missing_records(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(["python3", str(ROOT / "scripts/check_continuity_files.py"), directory], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISSING", result.stdout)

    def test_scanner_accepts_complete_fixture_records(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory)
            shutil.copy(ROOT / "templates/series-bible.yaml", target / "series-bible.yaml")
            shutil.copy(ROOT / "templates/continuity-ledger.yaml", target / "continuity-ledger.yaml")
            shutil.copy(ROOT / "templates/asset-index.yaml", target / "asset-index.yaml")
            shutil.copy(ROOT / "templates/session-handoff.md", target / "session-handoff.md")
            shutil.copy(ROOT / "tests/fixtures/episode-05.yaml", target / "episode-05.yaml")
            shutil.copy(ROOT / "templates/video-take.yaml", target / "video-take-01.yaml")
            result = subprocess.run(["python3", str(ROOT / "scripts/check_continuity_files.py"), directory], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NEXT ACTION", result.stdout)

    def test_scanner_rejects_empty_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory)
            for name in ("series-bible.yaml", "continuity-ledger.yaml", "asset-index.yaml"):
                shutil.copy(ROOT / "templates" / name, target / name)
            shutil.copy(ROOT / "tests/fixtures/episode-05.yaml", target / "episode-05.yaml")
            (target / "session-handoff.md").write_text("\n")
            result = subprocess.run(["python3", str(ROOT / "scripts/check_continuity_files.py"), directory], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("session-handoff.md", result.stdout)

    def test_scanner_reports_malformed_nested_records(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory)
            for name in ("series-bible.yaml", "continuity-ledger.yaml", "asset-index.yaml"):
                shutil.copy(ROOT / "templates" / name, target / name)
            shutil.copy(ROOT / "templates/session-handoff.md", target / "session-handoff.md")
            (target / "episode-05.yaml").write_text("episode: []\n")
            (target / "asset-index.yaml").write_text("assets: [bad-record]\n")
            result = subprocess.run(["python3", str(ROOT / "scripts/check_continuity_files.py"), directory], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("episode-05.yaml", result.stdout)
        self.assertIn("asset-index.yaml", result.stdout)


if __name__ == "__main__":
    unittest.main()
