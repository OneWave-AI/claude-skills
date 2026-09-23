"""Offline unit tests for the period, derivation and restatement logic.

Run:  python3 -m unittest discover -s tests -v     (from the skill folder; no network, no User-Agent needed)
"""
import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import sec_pull as sp  # noqa: E402

SYN = json.loads((HERE / "fixtures" / "synthetic_restatement.json").read_text())
AAPL = json.loads((HERE / "fixtures" / "aapl_companyfacts_subset.json").read_text())


def row(df, metric, period):
    r = df[(df["metric"] == metric) & (df["period"] == period)]
    assert len(r) == 1, f"expected one row for {metric} {period}, got {len(r)}"
    return r.iloc[0]


class TestPeriods(unittest.TestCase):
    def test_duration_classes(self):
        self.assertEqual(sp.duration_class("2025-01-01", "2025-03-31"), "3M")
        self.assertEqual(sp.duration_class("2025-01-01", "2025-06-30"), "6M")
        self.assertEqual(sp.duration_class("2025-01-01", "2025-09-30"), "9M")
        self.assertEqual(sp.duration_class("2024-09-29", "2025-09-27"), "FY")   # 52-week year
        self.assertEqual(sp.duration_class("2022-09-25", "2023-09-30"), "FY")   # 53-week year
        self.assertEqual(sp.duration_class(None, "2025-09-27"), "I")

    def test_labels_use_filing_calendar_not_fact_fy(self):
        # FY2023 comparatives inside the FY2025 10-K carry fy=2025; the label must still say FY2023/FY2024.
        cal = sp.fiscal_calendar(AAPL)
        self.assertEqual(sp.period_label("2024-09-29", "2025-09-27", cal)[0], "FY2025")
        self.assertEqual(sp.period_label("2023-10-01", "2024-09-28", cal)[0], "FY2024")
        self.assertEqual(sp.period_label("2025-06-29", "2025-09-27", cal)[0], "FY2025 Q4")
        self.assertEqual(sp.period_label("2025-09-28", "2026-06-27", cal)[0], "FY2026 9M YTD")
        self.assertEqual(sp.period_label(None, "2026-06-27", cal)[0], "FY2026 Q3 end")


class TestQ4Derivation(unittest.TestCase):
    def test_q4_is_fy_minus_9m_and_labelled_derived(self):
        df = sp.build_table(SYN, metrics=["revenue"], years=1, quarters=1)
        q4 = row(df, "revenue", "FY2025 Q4")
        self.assertEqual(q4["value"], 1050 - 770)
        self.assertEqual(q4["basis"], "derived")
        self.assertIn("FY - 9M YTD", q4["formula"])
        self.assertIn("0000000001-26-000002", q4["accn"])   # FY 10-K
        self.assertIn("0000000001-25-000020", q4["accn"])   # Q3 10-Q (9M YTD)
        self.assertEqual((q4["start"], q4["end"]), ("2025-10-01", "2025-12-31"))

    def test_q4_fallback_fy_minus_three_quarters(self):
        facts = copy.deepcopy(SYN)
        usd = facts["facts"]["us-gaap"]["Revenues"]["units"]["USD"]
        facts["facts"]["us-gaap"]["Revenues"]["units"]["USD"] = [
            f for f in usd if not (f.get("start") == "2025-01-01" and f["end"] == "2025-09-30")]
        df = sp.build_table(facts, metrics=["revenue"], years=1, quarters=1)
        q4 = row(df, "revenue", "FY2025 Q4")
        self.assertEqual(q4["value"], 1050 - 240 - 260 - 270)
        self.assertIn("FY - Q1 - Q2 - Q3", q4["formula"])

    def test_ytd_only_cash_flow_quarters(self):
        df = sp.build_table(SYN, metrics=["operating_cash_flow"], years=1, quarters=4)
        self.assertEqual(row(df, "operating_cash_flow", "FY2025 Q1")["value"], 50)
        self.assertEqual(row(df, "operating_cash_flow", "FY2025 Q2")["value"], 110 - 50)
        self.assertEqual(row(df, "operating_cash_flow", "FY2025 Q3")["value"], 180 - 110)
        self.assertEqual(row(df, "operating_cash_flow", "FY2025 Q4")["value"], 250 - 180)
        self.assertEqual(row(df, "operating_cash_flow", "TTM")["value"], 250)

    def test_eps_not_derived(self):
        df = sp.build_table(SYN, metrics=["eps_diluted"], years=1, quarters=1)
        q4 = row(df, "eps_diluted", "FY2025 Q4")
        self.assertTrue(q4["value"] != q4["value"] or q4["value"] is None)  # NaN
        self.assertIn("not additive", q4["notes"])

    def test_real_aapl_q4_and_ttm(self):
        df = sp.build_table(AAPL, metrics=["revenue", "capex"], years=1, quarters=4)
        self.assertEqual(row(df, "revenue", "FY2025 Q4")["value"], 102_466_000_000)  # 416,161 - 313,695 ($M)
        self.assertEqual(row(df, "revenue", "TTM")["value"], 466_823_000_000)
        self.assertEqual(row(df, "capex", "FY2026 Q3")["value"], 6_799_000_000 - 4_344_000_000)


class TestRestatement(unittest.TestCase):
    def test_latest_filed_value_wins_and_original_kept(self):
        df = sp.build_table(SYN, metrics=["revenue", "net_income"], years=2, quarters=0)
        fy24 = row(df, "revenue", "FY2024")
        self.assertEqual(fy24["value"], 950)
        self.assertEqual(fy24["original_value"], 1000)
        self.assertEqual(fy24["original_accn"], "0000000001-25-000001")
        self.assertTrue(fy24["revised"])
        # cite the FIRST filing that carried the restated number (the 10-K/A), not the later 10-K comparative
        self.assertEqual(fy24["accn"], "0000000001-25-000009")
        self.assertEqual(fy24["form"], "10-K/A")
        self.assertIn("originally reported 1,000", fy24["notes"])
        self.assertIn("amended", fy24["notes"])

    def test_as_reported_mode(self):
        df = sp.build_table(SYN, metrics=["revenue"], years=2, quarters=0, as_reported=True)
        fy24 = row(df, "revenue", "FY2024")
        self.assertEqual(fy24["value"], 1000)
        self.assertEqual(fy24["accn"], "0000000001-25-000001")

    def test_unrevised_period_cites_original_filing(self):
        df = sp.build_table(AAPL, metrics=["cash"], years=2, quarters=0)
        r = row(df, "cash", "FY2025 end")
        self.assertEqual(r["value"], 35_934_000_000)
        self.assertEqual(r["accn"], "0000320193-25-000079")  # the FY2025 10-K, not a later 10-Q comparative
        self.assertFalse(r["revised"])

    def test_max_strategy_picks_total_revenue_and_reports_alternative(self):
        df = sp.build_table(SYN, metrics=["revenue"], years=1, quarters=0)
        fy25 = row(df, "revenue", "FY2025")
        self.assertEqual(fy25["tag"], "us-gaap:Revenues")
        self.assertEqual(fy25["value"], 1050)
        self.assertIn("RevenueFromContractWithCustomerExcludingAssessedTax = 1,000", fy25["notes"])


class TestFormatting(unittest.TestCase):
    def test_fmt(self):
        self.assertEqual(sp.fmt_value(416_161_000_000, "USD"), "$416,161M")
        self.assertEqual(sp.fmt_value(-5_000_000, "USD"), "-$5M")
        self.assertEqual(sp.fmt_value(7.46, "USD/shares"), "$7.46")
        self.assertEqual(sp.fmt_value(14_773_260_000, "shares"), "14,773.3M sh")

    def test_markdown_has_citation_links(self):
        df = sp.build_table(SYN, metrics=["revenue"], years=1, quarters=0)
        md = sp.to_markdown(df)
        self.assertIn("https://www.sec.gov/Archives/edgar/data/1/000000000126000002/0000000001-26-000002-index.htm", md)

    def test_missing_user_agent_is_an_error(self):
        import os
        old = os.environ.pop("SEC_USER_AGENT", None)
        try:
            with self.assertRaises(sp.SecError):
                sp.user_agent()
        finally:
            if old is not None:
                os.environ["SEC_USER_AGENT"] = old


if __name__ == "__main__":
    unittest.main()
