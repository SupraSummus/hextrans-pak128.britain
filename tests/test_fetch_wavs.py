"""Smoke test for `pak.fetch_wavs.collect`.

Reads the actual ported bake units (no network — `fetch_pak` is not
called).  Anchors the contract that the source of truth is `.py`,
not `.dat`.
"""

from __future__ import annotations

import unittest

from pak.fetch_wavs import collect


class TestCollect(unittest.TestCase):

    def test_results_are_wav_filenames(self):
        for name in collect():
            with self.subTest(name=name):
                self.assertTrue(name.endswith(".wav"))
                self.assertNotIn("/", name)


if __name__ == "__main__":
    unittest.main()
