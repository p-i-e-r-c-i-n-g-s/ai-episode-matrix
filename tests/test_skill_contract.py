import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def read(self, name):
        return (ROOT / name).read_text()

    def test_episode_mode_is_continuity_first(self):
        text = self.read("SKILL.md")
        self.assertIn("top-level operating mode", text)
        self.assertIn("continuity bible", text)
        self.assertIn("continuity checkpoint", text)

    def test_durable_records_and_acceptance_gate(self):
        text = self.read("references/episode-building.md")
        for filename in ("series-bible.yaml", "continuity-ledger.yaml", "asset-index.yaml", "session-handoff.md"):
            self.assertIn(filename, text)
        self.assertIn("Episode acceptance gate", text)

    def test_state_lifecycle_and_asset_versions(self):
        text = self.read("references/episode-building.md")
        self.assertIn("planned → generated → reviewed → approved", text)
        self.assertIn("CHAR-01_v03", text)

    def test_episode_example_carries_state_forward(self):
        text = self.read("examples/episode-5-continuation.md")
        self.assertIn("EP-05", text)
        self.assertIn("PROP-07_v02", text)
        self.assertIn("Post-test record", text)

    def test_no_stale_project_name(self):
        paths = [ROOT / name for name in ("SKILL.md", "README.md", "WORKFLOW.md")]
        for directory in ("references", "examples"):
            paths.extend((ROOT / directory).rglob("*.md"))
        for path in paths:
            self.assertNotIn("cinematic-video-prompt-builder", path.read_text(errors="ignore"))

    def test_primary_modes_are_documented_as_six(self):
        text = self.read("SKILL.md")
        self.assertIn("## Six operating modes", text)
        self.assertNotIn("## Five operating modes", text)
        for mode in ("Image-base mode", "Image-to-video mode", "Director mode", "Movie mode", "Episode mode", "Music-video mode"):
            self.assertIn(mode, text)

    def test_music_video_reference_is_routed(self):
        self.assertIn("music-video-mode.md", self.read("SKILL.md"))

    def test_cinematography_reference_is_routed(self):
        self.assertIn("cinematography-discipline.md", self.read("SKILL.md"))


if __name__ == "__main__":
    unittest.main()
