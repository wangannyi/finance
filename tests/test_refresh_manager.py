import threading
import time
import unittest

from finance_app.refresh_manager import RefreshManager


class RefreshManagerTests(unittest.TestCase):
    def test_start_returns_while_refresh_runs_in_background(self):
        release = threading.Event()
        calls = []

        def runner(db_path):
            calls.append(db_path)
            release.wait(timeout=1)
            return [{"market": "ch"}]

        manager = RefreshManager("test.sqlite3", runner=runner)

        started = manager.start()
        duplicate = manager.start()

        self.assertEqual(started["status"], "running")
        self.assertEqual(duplicate["status"], "running")
        self.assertEqual(duplicate["message"], "刷新已在运行")
        self.assertEqual(calls, ["test.sqlite3"])

        release.set()
        for _ in range(20):
            status = manager.status()
            if status["status"] == "complete":
                break
            time.sleep(0.01)

        self.assertEqual(manager.status()["status"], "complete")
        self.assertEqual(manager.status()["saved_count"], 1)


if __name__ == "__main__":
    unittest.main()
