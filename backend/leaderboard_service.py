# leaderboard_service.py
from datetime import datetime, timedelta

class LeaderboardService:
    def __init__(self, supabase):
        self.supabase = supabase
        self.table_name = "recipes_public"

    def get_daily_leaderboard(self, limit=10):
        """Top recipes from the last 24 hours."""
        return self._get_leaderboard(days=1, limit=limit)

    def get_weekly_leaderboard(self, limit=10):
        """Top recipes from the last 7 days."""
        return self._get_leaderboard(days=7, limit=limit)

    def _get_leaderboard(self, days, limit=10):
        """Generic helper for daily/weekly leaderboards."""
        try:
            since = datetime.utcnow() - timedelta(days=days)
            response = (
                self.supabase.table(self.table_name)
                .select("recipeid, title, authorname, likes, datecreated")
                .gte("datecreated", since.isoformat())
                .order("likes", desc=True)
                .limit(limit)
                .execute()
            )

            if not response.data:
                return {"message": f"No recipes found in the last {days} day(s)"}, 200

            leaderboard = [
                {
                    "rank": idx + 1,
                    "recipeid": r["recipeid"], 
                    "author": r["authorname"],
                    "title": r["title"],
                    "likes": r.get("likes", 0),
                    "datecreated": r.get("datecreated")
                }
                for idx, r in enumerate(response.data)
            ]
            return {"leaderboard": leaderboard}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    def get_author_leaderboard(self, limit=10):
        """Ranks authors by total likes across all their recipes."""
        try:
            # Step 1: fetch all recipes
            response = (
                self.supabase.table(self.table_name)
                .select("authorname, likes")
                .execute()
            )
            if not response.data:
                return {"message": "No author data found"}, 200

            # Step 2: aggregate total likes per author
            totals = {}
            for row in response.data:
                author = row.get("authorname", "Unknown")
                totals[author] = totals.get(author, 0) + (row.get("likes", 0) or 0)

            # Step 3: rank by total likes
            ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:limit]
            leaderboard = [
                {"rank": idx + 1, "author": author, "total_likes": likes}
                for idx, (author, likes) in enumerate(ranked)
            ]
            return {"leaderboard": leaderboard}, 200

        except Exception as e:
            return {"error": str(e)}, 500
