import hashlib
import pathlib
import subprocess
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
STAMP = "2026-09-12T20:00:00Z"


def write_yaml(root, name, value):
    (root / name).write_text(yaml.safe_dump(value, sort_keys=False))


def valid_project(root):
    write_yaml(root, "series-bible.yaml", {"schema_version": 1, "series": {"id": "NS", "title": "North Signal", "version": 1, "status": "approved", "updated_at": STAMP}})
    write_yaml(root, "episode-05.yaml", {"schema_version": 1, "episode": {"id": "EP-05", "title": "Return Pulse", "version": 1, "status": "approved", "setup_mode": "full", "updated_at": STAMP}, "beginning_state": "Mara enters", "ending_state": "The signal responds"})
    write_yaml(root, "continuity-ledger.yaml", {"schema_version": 1, "series_id": "NS", "episode_id": "EP-05", "updated_at": STAMP, "latest_approved_shot": "SH-01", "states": [{"shot_id": "SH-01", "status": "approved"}], "unresolved": []})
    write_yaml(root, "asset-index.yaml", {"schema_version": 1, "updated_at": STAMP, "assets": [{"id": "REF-01", "version": 1, "type": "image", "path_or_url": "ref.png", "source": "user", "status": "approved"}]})
    (root / "session-handoff.md").write_text("# Session handoff\n\nSETUP MODE: full\nUPDATED AT: 2026-09-12T20:00:00Z\nSERIES: NS\nEPISODE: EP-05\nSCRIPT VERSION: 1\nLAST APPROVED SHOT: SH-01\nCURRENT STORY STATE: The signal responds\nUNRESOLVED QUESTIONS: none\nNEXT RECOMMENDED SHOT: SH-02\n")


def validate(root):
    return subprocess.run(["python3", str(ROOT / "scripts/check_continuity_files.py"), str(root)], capture_output=True, text=True)


class ContinuityBehaviorTests(unittest.TestCase):
    def test_checked_in_fixture_project_passes(self):
        result = validate(ROOT / "tests/fixtures")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_valid_project_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            valid_project(pathlib.Path(directory))
            result = validate(directory)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("LATEST APPROVED SHOT: SH-01", result.stdout)

    def test_blank_templates_fail_closed(self):
        result = validate(ROOT / "templates")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISSING episode-*.yaml", result.stdout)
        self.assertIn("must be non-empty", result.stdout)

    def test_missing_records_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = validate(directory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISSING", result.stdout)

    def test_cross_record_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            valid_project(root)
            ledger = yaml.safe_load((root / "continuity-ledger.yaml").read_text())
            ledger["series_id"] = "OTHER"
            ledger["episode_id"] = "EP-99"
            write_yaml(root, "continuity-ledger.yaml", ledger)
            result = validate(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match series-bible", result.stdout)
        self.assertIn("does not resolve to an episode", result.stdout)

    def test_invalid_timestamp_and_unresolved_latest_shot_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            valid_project(root)
            ledger = yaml.safe_load((root / "continuity-ledger.yaml").read_text())
            ledger["updated_at"] = "yesterday"
            ledger["latest_approved_shot"] = "SH-MISSING"
            write_yaml(root, "continuity-ledger.yaml", ledger)
            result = validate(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ISO-8601", result.stdout)
        self.assertIn("must resolve to an approved state", result.stdout)

    def test_duplicate_asset_versions_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            valid_project(root)
            assets = yaml.safe_load((root / "asset-index.yaml").read_text())
            assets["assets"].append(dict(assets["assets"][0]))
            write_yaml(root, "asset-index.yaml", assets)
            result = validate(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate asset version", result.stdout)

    def test_reviewed_take_requires_review_evidence_and_resolved_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            valid_project(root)
            write_yaml(root, "video-take-01.yaml", {"schema_version": 1, "take": {"id": "TAKE-01", "episode_id": "EP-05", "shot_id": "SH-01", "image_prompt_version": "1", "source_image_id": "MISSING", "model_version": "1", "video_prompt_version": "1", "generation_settings": {}, "output_take_id": "OUT-01", "observed_continuity_failures": [], "approval_status": "approved", "reviewed_at": "", "reviewed_by": "", "review_notes": "", "created_at": STAMP}})
            result = validate(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not resolve to the asset index", result.stdout)
        self.assertIn("reviewed_at", result.stdout)

    def test_atomic_update_rejects_stale_writer_and_preserves_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "ledger.yaml"
            replacement = root / "new.yaml"
            target.write_text("version: 1\n")
            replacement.write_text("version: 2\n")
            result = subprocess.run(["python3", str(ROOT / "scripts/atomic_update.py"), str(target), str(replacement), "--expect-sha256", "bad"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(target.read_text(), "version: 1\n")

    def test_atomic_update_writes_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = root / "ledger.yaml"
            replacement = root / "new.yaml"
            target.write_text("version: 1\n")
            replacement.write_text("version: 2\n")
            expected = hashlib.sha256(target.read_bytes()).hexdigest()
            result = subprocess.run(["python3", str(ROOT / "scripts/atomic_update.py"), str(target), str(replacement), "--expect-sha256", expected], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(target.read_text(), "version: 2\n")
            self.assertEqual((root / "ledger.yaml.bak").read_text(), "version: 1\n")


if __name__ == "__main__":
    unittest.main()
