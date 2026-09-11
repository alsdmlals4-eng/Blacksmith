"""Non-runtime scheduling probe. Never reads/writes game saves or runtime assets."""
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "docs/planning/BLACKSMITH_MODAK_CALENDAR_REVIEW_20260912.json"


class ScheduleReview:
    def __init__(self):
        self.policy = json.loads(SOURCE.read_text(encoding="utf-8"))["order_schedule_trial"]
        self.day = 1
        self.gold = 0
        self.material = 0
        self.sequence = 0
        self.offers = [self._next_id() for _ in range(self.policy["total_slots"])]
        self.pending = {}
        self.resolved = set()
        self.closed = set()

    def _next_id(self):
        self.sequence += 1
        return f"trial-order-{self.sequence}"

    def complete_recovery(self, order_id):
        # Assumes valid dedicated-material crafting/consumption happened elsewhere.
        if order_id is None or self.offers[0] != order_id:
            return False
        self.offers[0] = None
        self.gold += self.policy["recovery_gold"]
        self.material += self.policy["recovery_material"]
        return True

    def dispatch(self, order_id, kind, uid):
        if kind not in self.policy["report_delay_days"] or not uid:
            return False
        if order_id is None or order_id not in self.offers[1:] or order_id in self.pending:
            return False
        if any(record["uid"] == uid for record in self.pending.values()):
            return False
        self.pending[order_id] = {"uid": uid, "due": self.day + self.policy["report_delay_days"][kind]}
        return True

    def close(self, source_day, save_ok=True):
        # save_ok is injected outcome, NOT filesystem atomic-save verification.
        if source_day != self.day or source_day in self.closed or not save_ok:
            return False
        self.closed.add(source_day)
        self.day += 1
        for order_id, record in list(self.pending.items()):
            if record["due"] <= self.day:
                self.resolved.add(order_id)
                self.offers[self.offers.index(order_id)] = None
                del self.pending[order_id]
        self.offers = [offer if offer is not None else self._next_id() for offer in self.offers]
        return True


def probe():
    idle = ScheduleReview()
    initial_offers = idle.offers.copy()
    for _ in range(240):
        idle.close(idle.day)
    recovery = ScheduleReview()
    for _ in range(30):
        recovery.complete_recovery(recovery.offers[0])
        recovery.close(recovery.day)
    return {
        "evidence": "ABSTRACT_SCHEDULING_ONLY_NOT_RUNTIME_OR_BALANCE_PASS",
        "empty_240_closes": {"day": idle.day, "gold": idle.gold, "offers_unchanged": idle.offers == initial_offers,
                            "finding": "UNRESOLVED: pure calendar growth can be rushed without work"},
        "recovery_30_completed_orders": {"gold": recovery.gold, "material": recovery.material,
                                         "finding": "Intended labor reward assuming valid crafting; effort and item consumption not simulated"}
    }


if __name__ == "__main__":
    print(json.dumps(probe(), ensure_ascii=False, indent=2))
