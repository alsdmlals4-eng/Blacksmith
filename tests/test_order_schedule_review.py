"""Offline planning model only; no Godot or save implementation evidence."""
import unittest
from tools.simulate_order_schedule_review import ScheduleReview


class OrderScheduleReviewTests(unittest.TestCase):
    def test_empty_days_do_not_create_wealth_or_reroll_offers(self):
        model = ScheduleReview()
        original = model.offers.copy()
        for _ in range(240):
            model.close(model.day)
        self.assertEqual(model.gold, 0)
        self.assertEqual(model.offers, original)
        self.assertEqual(model.day, 241)  # Reveals growth-skipping risk, not a fix.

    def test_completed_recovery_refills_only_next_day(self):
        model = ScheduleReview()
        order = model.offers[0]
        self.assertTrue(model.complete_recovery(order))
        self.assertFalse(model.complete_recovery(order))
        self.assertIsNone(model.offers[0])
        model.close(1)
        self.assertIsNotNone(model.offers[0])
        self.assertEqual(model.gold, 400)

    def test_duplicate_and_save_failure(self):
        model = ScheduleReview()
        self.assertFalse(model.close(1, save_ok=False))
        self.assertEqual(model.day, 1)
        self.assertTrue(model.close(1))
        self.assertFalse(model.close(1))
        self.assertEqual(model.day, 2)

    def test_reports_resolve_once_on_due_day(self):
        model = ScheduleReview()
        self.assertTrue(model.dispatch(model.offers[1], "ADVENTURE", "uid-1"))
        self.assertFalse(model.dispatch(model.offers[2], "DUEL", "uid-1"))
        model.close(1)
        self.assertEqual(len(model.resolved), 0)
        model.close(2)
        self.assertEqual(len(model.resolved), 1)
        model.close(3)
        self.assertEqual(len(model.resolved), 1)

    def test_two_world_orders_do_not_occupy_recovery(self):
        model = ScheduleReview()
        model.dispatch(model.offers[1], "ARMY", "uid-1")
        model.dispatch(model.offers[2], "ARMY", "uid-2")
        self.assertTrue(model.complete_recovery(model.offers[0]))

    def test_unknown_profile_is_rejected_without_mutation(self):
        model = ScheduleReview()
        before = model.offers.copy()
        self.assertFalse(model.dispatch(model.offers[1], "UNKNOWN", "uid-1"))
        self.assertEqual(model.offers, before)
        self.assertEqual(model.pending, {})

    def test_each_report_delay_uses_handoff_day(self):
        for kind, delay in [("DUEL", 1), ("ADVENTURE", 2), ("ARMY", 3)]:
            with self.subTest(kind=kind):
                model = ScheduleReview()
                for _ in range(4):
                    model.close(model.day)
                model.dispatch(model.offers[1], kind, "uid-1")
                for _ in range(delay - 1):
                    model.close(model.day)
                    self.assertEqual(len(model.resolved), 0)
                model.close(model.day)
                self.assertEqual(model.day, 5 + delay)
                self.assertEqual(len(model.resolved), 1)


if __name__ == "__main__":
    unittest.main()
