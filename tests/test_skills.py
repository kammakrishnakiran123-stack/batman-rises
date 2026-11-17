#!/usr/bin/env python3
"""Verify the Batman Rises library. Standard library only.

Run from the repo root:  python3 tests/test_skills.py

Checks:
  1. Every skill folder has valid frontmatter (name matches folder, description present).
  2. Every skill script runs and gives the expected result on synthetic data.
"""
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def script(rel: str):
    return str(ROOT / rel)


def run(*args, expect_ok=True):
    proc = subprocess.run([PY, *args], capture_output=True, text=True)
    if expect_ok and proc.returncode != 0:
        raise AssertionError(f"exit {proc.returncode}\n{proc.stdout}\n{proc.stderr}")
    return proc


class Frontmatter(unittest.TestCase):
    def test_every_skill_has_valid_frontmatter(self):
        folders = [p.parent for p in ROOT.glob("*/SKILL.md")]
        self.assertGreaterEqual(len(folders), 24, "expected at least 24 skill folders")
        for folder in folders:
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), f"{folder.name}: no frontmatter")
            name = re.search(r"^name: (.+)$", text, re.MULTILINE)
            desc = re.search(r"^description: (.+)$", text, re.MULTILINE)
            self.assertIsNotNone(name, f"{folder.name}: missing name")
            self.assertEqual(name.group(1).strip(), folder.name, f"{folder.name}: name does not match folder")
            self.assertIsNotNone(desc, f"{folder.name}: missing description")

    def test_deepcrawl_is_in_its_own_folder(self):
        self.assertTrue((ROOT / "deepcrawl-website-reader" / "SKILL.md").exists())
        self.assertFalse((ROOT / "deepcrawl-website-reader.md").exists())


class PhotoOrganizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PIL import Image
        cls.tmp = Path(tempfile.mkdtemp())
        src = cls.tmp / "photos"
        src.mkdir()
        im = Image.new("RGB", (8, 8), (255, 0, 0))
        ex = im.getexif()
        ex.get_ifd(0x8769)[36867] = "2024:06:01 10:00:00"
        im.save(src / "a.jpg", exif=ex)
        shutil.copy(src / "a.jpg", src / "a_copy.jpg")
        Image.new("RGB", (8, 8), (0, 255, 0)).save(src / "noexif.png")
        (src / "a.xmp").write_text("<x/>")
        cls.src, cls.tmp_root = src, cls.tmp

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp_root)

    def test_dry_run_writes_only_the_plan(self):
        lib, plan = self.tmp / "lib1", self.tmp / "plan1.csv"
        run(script("photo-library-organizer/scripts/organize_photos.py"), str(self.src), str(lib),
            "--plan", str(plan))
        self.assertFalse(lib.exists())
        with plan.open(newline="") as fh:
            rows = list(csv.DictReader(fh))
        statuses = sorted(r["status"] for r in rows)
        self.assertEqual(statuses, ["dated", "dated", "duplicate", "undated"])

    def test_execute_routes_and_keeps_originals(self):
        lib, plan = self.tmp / "lib2", self.tmp / "plan2.csv"
        run(script("photo-library-organizer/scripts/organize_photos.py"), str(self.src), str(lib),
            "--plan", str(plan), "--execute")
        self.assertTrue((lib / "2024" / "2024-06-01" / "a.jpg").exists())
        self.assertTrue((lib / "2024" / "2024-06-01" / "a.xmp").exists())
        self.assertTrue((lib / "_duplicates" / "a_copy.jpg").exists())
        self.assertTrue((lib / "_undated" / "noexif.png").exists())
        self.assertTrue((self.src / "a.jpg").exists())

    def test_refuses_destination_inside_source(self):
        proc = run(script("photo-library-organizer/scripts/organize_photos.py"), str(self.src),
                   str(self.src / "inside"), "--plan", str(self.tmp / "p3.csv"), expect_ok=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse((self.src / "inside").exists())


class Sm2(unittest.TestCase):
    def test_formula_and_scheduling(self):
        sys.path.insert(0, str(ROOT / "fluent-language-tutor" / "scripts"))
        from datetime import date
        from sm2 import sm2_update
        t = date(2026, 1, 1)
        item = {"ease_factor": 2.5, "repetitions": 0, "interval_days": 0}
        a = sm2_update(item, 5, t)
        self.assertEqual((a["repetitions"], a["interval_days"], a["ease_factor"]), (1, 1, 2.6))
        b = sm2_update(a, 5, t)
        self.assertEqual((b["repetitions"], b["interval_days"]), (2, 6))
        c = sm2_update(b, 4, t)
        self.assertEqual(c["interval_days"], round(6 * b["ease_factor"]))
        lapse = sm2_update(c, 1, t)
        self.assertEqual((lapse["repetitions"], lapse["interval_days"]), (0, 1))
        floor = sm2_update({"ease_factor": 1.31, "repetitions": 3, "interval_days": 10}, 0, t)
        self.assertEqual(floor["ease_factor"], 1.3)
        with self.assertRaises(ValueError):
            sm2_update(item, 6, t)


class Transcripts(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.srt = self.tmp / "ep.srt"
        self.srt.write_text(
            "1\n00:00:01,000 --> 00:00:04,000\nWelcome to the show.\n\n"
            "2\n00:00:10,000 --> 00:00:14,500\nThe biggest mistake is ignoring small expenses.\n\n"
            "3\n00:00:20,000 --> 00:00:25,000\nStart with a monthly review.\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_search(self):
        out = run(script("podcast-clipper-search/scripts/transcript_tools.py"), "search",
                  str(self.srt), "small expenses").stdout
        self.assertIn("00:00:10,000", out)
        self.assertIn("1 match(es)", out)

    def test_window_shifts_and_clips(self):
        out = self.tmp / "clip.srt"
        run(script("podcast-clipper-search/scripts/transcript_tools.py"), "window",
            str(self.srt), "00:00:09", "00:00:22", str(out), "--pad", "0.3")
        text = out.read_text()
        self.assertIn("00:00:01,300 --> 00:00:05,800", text)  # cue 2 shifted by 8.7 s
        self.assertIn("00:00:11,300 --> 00:00:13,600", text)  # cue 3 shifted and clipped at 22.3 s
        self.assertNotIn("Welcome", text)


class HealthSummary(unittest.TestCase):
    def test_no_double_counting_and_sleep_filter(self):
        import datetime as dt
        tmp = Path(tempfile.mkdtemp())
        try:
            xml = tmp / "export.xml"
            rows = ['<?xml version="1.0"?><HealthData>']
            start = dt.date(2026, 5, 1)
            for i in range(10):
                d = start + dt.timedelta(days=i)
                for src in ("Watch", "iPhone"):
                    rows.append(f'<Record type="HKQuantityTypeIdentifierStepCount" sourceName="{src}" '
                                f'startDate="{d} 09:00:00 +0530" endDate="{d} 09:10:00 +0530" value="{1000 * (i + 1)}"/>')
                rows.append(f'<Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Watch" '
                            f'value="HKCategoryValueSleepAnalysisInBed" startDate="{d} 23:00:00 +0530" '
                            f'endDate="{d + dt.timedelta(days=1)} 07:00:00 +0530"/>')
                rows.append(f'<Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Watch" '
                            f'value="HKCategoryValueSleepAnalysisAsleepCore" startDate="{d} 23:30:00 +0530" '
                            f'endDate="{d + dt.timedelta(days=1)} 06:30:00 +0530"/>')
            rows.append("</HealthData>")
            xml.write_text("\n".join(rows))
            out = tmp / "out"
            run(script("health-fitness-insights/scripts/health_summary.py"), str(xml), str(out))
            with (out / "daily.csv").open(newline="") as fh:
                data = list(csv.DictReader(fh))
            self.assertEqual(data[0]["steps"], "1000")       # not 2000
            self.assertEqual(data[-1]["steps"], "10000")
            self.assertEqual(float(data[0]["sleep_hours"]), 7.0)  # InBed excluded
            self.assertEqual(data[6]["steps_7d_avg"], "4000")
        finally:
            shutil.rmtree(tmp)


class ChatInsights(unittest.TestCase):
    def test_counts_turns_and_flags_empty_files(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            exp = tmp / "exports"
            exp.mkdir()
            (exp / "a.md").write_text("---\ntitle: \"Plan\"\ndate: 2026-03-02\n---\n"
                                      "## Human\nHow do I plan a trip?\n## Claude\nStart with dates.\n"
                                      "## Human\nWhich cities?\n## Claude\nTokyo.\n")
            (exp / "b.md").write_text("# nothing here\n")
            out = tmp / "out"
            proc = run(script("chat-insights-dashboard/scripts/chat_insights.py"), str(exp), str(out))
            stats = json.loads((out / "stats.json").read_text())
            self.assertEqual((stats["conversations"], stats["turns"]), (2, 4))
            self.assertIn("1 file(s) had no", proc.stdout)
            self.assertIn("<svg", (out / "dashboard.html").read_text())
        finally:
            shutil.rmtree(tmp)


class Wardrobe(unittest.TestCase):
    def test_validate_and_outfits(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            inv = tmp / "w.json"
            inv.write_text(json.dumps([
                {"id": "t1", "name": "Oxford", "category": "top", "color": "white", "pattern": "solid",
                 "fabric": "cotton", "formality": "smart-casual", "season": "all"},
                {"id": "b1", "name": "Chinos", "category": "bottom", "color": "navy", "pattern": "solid",
                 "fabric": "cotton", "formality": "smart-casual", "season": "all"},
                {"id": "f1", "name": "Loafers", "category": "footwear", "color": "brown", "pattern": "solid",
                 "fabric": "leather", "formality": "smart-casual", "season": "all"},
            ]))
            ok = run(script("wardrobe-outfit-planner/scripts/wardrobe.py"), "validate", str(inv))
            self.assertIn("Inventory OK", ok.stdout)
            out = run(script("wardrobe-outfit-planner/scripts/wardrobe.py"), "outfits", str(inv),
                      "--season", "warm", "--formality", "smart-casual").stdout
            self.assertIn("top: Oxford, bottom: Chinos, footwear: Loafers", out)
            bad = tmp / "bad.json"
            bad.write_text('[{"id":"x","name":"n","category":"hat","color":"c","pattern":"p",'
                           '"fabric":"f","formality":"gala","season":"summer"}]')
            proc = run(script("wardrobe-outfit-planner/scripts/wardrobe.py"), "validate", str(bad),
                       expect_ok=False)
            self.assertEqual(proc.returncode, 1)
        finally:
            shutil.rmtree(tmp)


class PipelineCheck(unittest.TestCase):
    def test_errors_fail_the_check(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / "p.csv"
            p.write_text(
                "account,contact_name,contact_role,trigger_event,source_url,stage,next_step,next_step_date,owner,priority\n"
                "Acme,Ravi,CFO,Series B,,discovery,Demo,2026-12-01,K,high\n"
                "Globex,Lee,VP,,,contacted,Follow up,2026-12-01,K,urgent\n")
            proc = run(script("sales-engine-workflow/scripts/pipeline_check.py"), str(p),
                       "--today", "2026-11-16", expect_ok=False)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("no source_url", proc.stdout)
            self.assertIn("priority must be", proc.stdout)
        finally:
            shutil.rmtree(tmp)


class DiskAudit(unittest.TestCase):
    def test_tiers_and_nothing_deleted(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            home = tmp / "u"
            (home / "Library" / "Caches" / "app").mkdir(parents=True)
            (home / "Library" / "Caches" / "app" / "c.bin").write_bytes(b"x" * 3000)
            (home / "Downloads").mkdir()
            (home / "Downloads" / "iso.bin").write_bytes(b"x" * 9000)
            out = run(script("disk-and-drive-cleaner/scripts/size_audit.py"), str(home)).stdout
            self.assertIn("SAFE_TO_CLEAR", out)
            self.assertIn("REVIEW_FIRST", out)
            self.assertTrue((home / "Downloads" / "iso.bin").exists())
        finally:
            shutil.rmtree(tmp)


class ContentLint(unittest.TestCase):
    def test_x_limit_and_placeholder(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            d = tmp / "d.md"
            d.write_text("Short post.\n---\n" + "x" * 300 + "\n---\nSecond.\n\n## LinkedIn\nHook.\n")
            proc = run(script("content-production-pipeline/scripts/channel_lint.py"), str(d), expect_ok=False)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("X post 2: 300 characters", proc.stdout)
        finally:
            shutil.rmtree(tmp)


class ClauseScan(unittest.TestCase):
    def test_flags_high_risk_clauses(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            c = tmp / "c.txt"
            c.write_text("Provider's liability is unlimited liability for data loss.\n"
                         "Customer hereby assigns to Provider all improvements.\n"
                         "Provider may modify these terms at any time without notice.\n"
                         "This Agreement renews automatically each year.\n")
            out = run(script("contract-risk-review/scripts/clause_scan.py"), str(c)).stdout
            for label in ("Uncapped or unlimited liability", "Assignment of IP",
                          "Unilateral right to change terms", "Automatic renewal"):
                self.assertIn(label, out)
            self.assertIn("No governing-law clause found", out)
        finally:
            shutil.rmtree(tmp)


class ProposalGaps(unittest.TestCase):
    def test_negated_budget_is_still_a_gap(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            n = tmp / "n.md"
            n.write_text("Client wants a website redesign. We will build it in 6 weeks. Budget not discussed.\n")
            out = run(script("meeting-to-proposal/scripts/proposal_gaps.py"), str(n)).stdout
            self.assertIn("- Pricing or budget", out)
            self.assertNotIn("- Timeline or phases", out)
        finally:
            shutil.rmtree(tmp)


class Preflight(unittest.TestCase):
    def test_refuses_same_device_and_missing_destination(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            src = tmp / "src.img"
            src.write_bytes(b"x" * 4096)
            same = run(script("data-recovery-triage/scripts/preflight.py"), "--source", str(src),
                       "--dest", str(tmp), expect_ok=False)
            self.assertEqual(same.returncode, 1)
            self.assertIn("same device", same.stdout)
            missing = tmp / "nope"
            proc = run(script("data-recovery-triage/scripts/preflight.py"), "--source", str(src),
                       "--dest", str(missing), expect_ok=False)
            self.assertEqual(proc.returncode, 1)
            self.assertFalse(missing.exists(), "preflight must never create the destination")
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
