import unittest
from unittest.mock import MagicMock
from leaderboard_service import LeaderboardService
from datetime import datetime

class LeaderboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mock_supabase = MagicMock()
        cls.service = LeaderboardService(mock_supabase)

    def test_daily_leaderboard(self):
        mock_data = [
            {"recipeid": 1, "title": "A", "authorname": "u1", "likes": 15, "datecreated": datetime.utcnow().isoformat()},
            {"recipeid": 2, "title": "B", "authorname": "u2", "likes": 10, "datecreated": datetime.utcnow().isoformat()}
        ]
        self.service.supabase.table().select().gte().order().limit().execute.return_value.data = mock_data
        result, status = self.service.get_daily_leaderboard()
        self.assertEqual(status, 200)
        self.assertEqual(result["leaderboard"][0]["rank"], 1)

    def test_author_leaderboard(self):
        mock_data = [
            {"authorname": "u1", "likes": 5},
            {"authorname": "u1", "likes": 10},
            {"authorname": "u2", "likes": 7}
        ]
        self.service.supabase.table().select().execute.return_value.data = mock_data
        result, status = self.service.get_author_leaderboard()
        self.assertEqual(status, 200)
        self.assertEqual(result["leaderboard"][0]["author"], "u1")

if __name__ == "__main__":
    unittest.main()
