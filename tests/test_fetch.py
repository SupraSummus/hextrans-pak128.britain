"""Tests for `pak._fetch` — the lock-file parser/emitter and the
validate-or-record predicate.  Network and filesystem are not
exercised here; live fetches are covered by the bake CI jobs.

Run from the repo root:

    python3 -m pytest tests/

or, without pytest installed:

    python3 -m unittest tests.test_fetch
"""

from __future__ import annotations

import unittest

from pak._fetch import emit_lock, parse_lock, validate_or_record

SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64


class TestLockRoundTrip(unittest.TestCase):

    def test_empty_manifest(self):
        text = emit_lock("deadbeef", {})
        self.assertEqual(parse_lock(text), ("deadbeef", {}))

    def test_populated_manifest_round_trips(self):
        files = {"a/file": SHA_A, "b/file": SHA_B, "c/file": SHA_C}
        text = emit_lock("deadbeef", files)
        self.assertEqual(parse_lock(text), ("deadbeef", files))

    def test_emit_sorts_by_path(self):
        text = emit_lock("d", {"z": SHA_A, "a": SHA_B, "m": SHA_C})
        body = [l for l in text.splitlines() if "  " in l]
        paths = [l.split("  ", 1)[1] for l in body]
        self.assertEqual(paths, ["a", "m", "z"])

    def test_emit_is_idempotent(self):
        files = {"a/file": SHA_A, "b/file": SHA_B}
        once = emit_lock("d", files)
        twice = emit_lock(*parse_lock(once))
        self.assertEqual(once, twice)


class TestLockParse(unittest.TestCase):

    def test_comments_and_blanks_ignored(self):
        text = (
            "# leading comment\n"
            "\n"
            "commit deadbeef\n"
            "\n"
            "# section comment\n"
            f"{SHA_A}  a/file\n"
        )
        commit, files = parse_lock(text)
        self.assertEqual(commit, "deadbeef")
        self.assertEqual(files, {"a/file": SHA_A})

    def test_missing_separator_raises(self):
        text = f"commit d\n{SHA_A} a/file\n"  # single space, not the two-space sha256sum separator
        with self.assertRaises(RuntimeError) as cm:
            parse_lock(text, source="x.lock")
        self.assertIn("x.lock", str(cm.exception))

    def test_paths_with_spaces_kept_intact(self):
        # Two-space separator means paths with single spaces survive.
        text = f"commit d\n{SHA_A}  path with spaces/file\n"
        _, files = parse_lock(text)
        self.assertEqual(files, {"path with spaces/file": SHA_A})

    def test_no_commit_header_yields_empty_commit(self):
        text = f"{SHA_A}  a/file\n"
        commit, files = parse_lock(text)
        self.assertEqual(commit, "")
        self.assertEqual(files, {"a/file": SHA_A})


class TestValidateOrRecord(unittest.TestCase):

    def test_unknown_path_records_and_returns_true(self):
        files: dict[str, str] = {}
        self.assertTrue(validate_or_record(files, "x", SHA_A))
        self.assertEqual(files, {"x": SHA_A})

    def test_match_returns_false_and_does_not_mutate(self):
        files = {"x": SHA_A}
        self.assertFalse(validate_or_record(files, "x", SHA_A))
        self.assertEqual(files, {"x": SHA_A})

    def test_mismatch_raises_and_does_not_mutate(self):
        files = {"x": SHA_A}
        with self.assertRaises(SystemExit) as cm:
            validate_or_record(files, "x", SHA_B)
        msg = str(cm.exception)
        self.assertIn("x", msg)
        self.assertIn(SHA_A, msg)
        self.assertIn(SHA_B, msg)
        self.assertEqual(files, {"x": SHA_A})


if __name__ == "__main__":
    unittest.main()
