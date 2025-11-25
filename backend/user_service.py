from supabase import Client
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv() 


class UserService:
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table = "users_public"

    # -------------------------------------------------
    # CREATE USER
    # -------------------------------------------------
    def create_user(self, user_id: str, username: str, aller, unseen):

        profile_data = {
            "id": user_id,
            "username": username,
            "allergens": aller,
            "liked_recipes": [],
            "unseen_recipes": unseen,
            "disliked_recipes": [],
            "total_likes": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        try:
            result = self.supabase.table(self.table).insert(profile_data).execute()
            return {"data": result.data}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    # -------------------------------------------------
    def get_user(self, user_id: str):
        try:
            res = (
                self.supabase.table(self.table)
                .select("*")
                .eq("id", user_id)
                .execute()
            )

            if not res.data:
                return {"error": "User not found"}, 404

            return {"data": res.data}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    # -------------------------------------------------
    # UPDATE ALLERGENS
    # -------------------------------------------------
    def update_allergens(self, user_id: str, allergens: list):
        try:
            resp = (
                self.supabase.table(self.table)
                .update({"allergens": allergens})
                .eq("id", user_id)
                .execute()
            )
            return {"data": resp.data}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    # -------------------------------------------------
    # LIKE/DISLIKE RECIPE
    # -------------------------------------------------
    def like_recipe(self, user_id: str, recipe_id: int, author_id: str):
        try:
            user, _ = self.get_user(user_id)
            profile = user["data"][0]

            likes = profile.get("liked_recipes", [])
            if recipe_id not in likes:
                likes.append(recipe_id)

            unseen = profile.get("unseen_recipes", [])
            if recipe_id in unseen:
                unseen.remove(recipe_id)

            self.supabase.table(self.table).update(
                {
                    "liked_recipes": likes,
                    "unseen_recipes": unseen
                }
            ).eq("id", user_id).execute()

            author, _ = self.get_user(author_id)
            total = author["data"][0].get("total_likes", 0) + 1

            self.supabase.table(self.table).update(
                {"total_likes": total}
            ).eq("id", author_id).execute()

            return {"data": "Recipe liked"}, 200

        except Exception as e:
            return {"error": str(e)}, 500
        
    def dislike_recipe(self, user_id: str, recipe_id: int):
        try:
            user, _ = self.get_user(user_id)
            profile = user["data"][0]

            disliked = profile.get("disliked_recipes", [])
            if recipe_id not in disliked:
                disliked.append(recipe_id)

            # Remove from unseen_recipes
            unseen = profile.get("unseen_recipes", [])
            if recipe_id in unseen:
                unseen.remove(recipe_id)

            # Update user record
            res = (
                self.supabase.table(self.table)
                .update({
                    "disliked_recipes": disliked,
                    "unseen_recipes": unseen
                })
                .eq("id", user_id)
                .execute()
            )
            return {"data": res.data}, 200

        except Exception as e:
            return {"error": str(e)}, 500


    def get_liked_recipes(self, user_id: str):
            """
            Returns all recipe rows whose IDs appear in user's liked_recipes list.
            """

            # 1) Fetch the user profile
            user_res = self.supabase.table(self.user_table).select("*").eq("id", user_id).execute()

            if not user_res.data:
                return {"error": "User not found"}, 404

            liked_ids = user_res.data[0].get("liked_recipes", [])

            # If empty, return empty list
            if not liked_ids:
                return {"data": []}, 200

            # 2) Fetch recipes matching these IDs
            recipes_res = (
                self.supabase.table(self.recipe_table)
                .select("*")
                .in_("id", liked_ids)
                .execute()
            )

            return {"data": recipes_res.data}, 200

    # -------------------------------------------------
    def unlike_recipe(self, user_id: str, recipe_id: int, author_id: str):
        try:
            user, _ = self.get_user(user_id)
            profile = user["data"][0]

            likes = profile.get("liked_recipes", [])
            if recipe_id in likes:
                likes.remove(recipe_id)

            self.supabase.table(self.table).update(
                {"liked_recipes": likes}
            ).eq("id", user_id).execute()

            author, _ = self.get_user(author_id)
            total = max(0, author["data"][0].get("total_likes", 0) - 1)

            self.supabase.table(self.table).update(
                {"total_likes": total}
            ).eq("id", author_id).execute()

            return {"data": "Recipe unliked"}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    # -------------------------------------------------
    def add_unseen(self, user_id: str, recipe_id: int):
        try:
            user, _ = self.get_user(user_id)
            profile = user["data"][0]

            unseen = profile.get("unseen_recipes", [])
            if recipe_id not in unseen:
                unseen.append(recipe_id)

            res = (
                self.supabase.table(self.table)
                .update({"unseen_recipes": unseen})
                .eq("id", user_id)
                .execute()
            )

            return {"data": res.data}, 200

        except Exception as e:
            return {"error": str(e)}, 500