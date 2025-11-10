'''from typing import List, Dict, Any
import json, ast

class RecipeUtility:
    def __init__(self, supabase=None):
        """
        Utility for building and filtering user feeds.
        If `supabase` is None, operates in offline/test mode.
        """
        self.supabase = supabase
        self.table_name = "recipes_public"

    # -------------------------------
    #  Core filtering logic (works in both modes)
    # -------------------------------

    def filter_recipes_by_allergens(self, recipes, user_allergens):
        """
        NOT USING THIS ONE 
        Remove any recipe whose dietary restrictions contain an allergen.
        Comparison is case-insensitive and handles stringified lists from Supabase.
        """
        allergens = [a.strip().lower() for a in (user_allergens or [])]
        filtered = []

        for recipe in recipes:
            restrictions = self._parse_list_field(recipe.get("dietaryrestrictions"))
            # A recipe passes if it does NOT contain any allergen
            if not any(a in restrictions for a in allergens):
                filtered.append(recipe)
        return filtered


    
    def filter_recipes_by_allergens(self, recipes, user_allergens):
        """
        USING THIS ONE 
        Remove recipes containing allergens that match user's restrictions.
        Matching is case-insensitive but titles remain in their original casing.
        """
        # Normalize allergen comparison (case-insensitive)
        user_allergens_lower = [a.lower() for a in user_allergens]

        filtered = []
        for recipe in recipes:
            recipe_allergens = [
                a.lower()
                for a in self._parse_list_field(recipe.get("dietaryrestrictions", []))
            ]
            # Skip recipes that contain any allergen
            if any(a in recipe_allergens for a in user_allergens_lower):
                continue
            filtered.append(recipe)
        return filtered


    def filter_unseen_recipes(self, recipes: List[Dict[str, Any]], unseen_ids: List[int]):
        """Only keep recipes the user hasn't seen yet."""
        if not unseen_ids:
            return recipes
        return [r for r in recipes if r.get("recipeid") in unseen_ids]

    # -------------------------------
    #  Feed generation logic
    # -------------------------------
    def generate_user_feed(self, recipes=None, user_data=None):
        """
        Generates a personalized recipe feed for a given user.
        Works in two modes:
        1. Offline (unit test): self.utility.generate_user_feed(recipes, user)
        2. Online  (app route): utility.generate_user_feed(user)
        """

        # --- auto-fix argument order ---
        if isinstance(recipes, dict) and isinstance(user_data, list):
            # args were flipped (test order)
            recipes, user_data = user_data, recipes

        # --- fetch from Supabase in live mode ---
        if recipes is None and self.supabase:
            try:
                response = self.supabase.table(self.table_name).select("*").execute()
                recipes = response.data or []
            except Exception as e:
                return {"error": f"Failed to fetch recipes: {e}"}

        if not recipes:
            return []

        # --- normalize user fields ---
        if isinstance(user_data, list) and user_data:
            user_data = user_data[0]
        elif not isinstance(user_data, dict):
            user_data = {}

        allergens = self._parse_list_field(user_data.get("allergens"))
        unseen = self._parse_list_field(user_data.get("unseen_recipes"))

        # --- apply filters ---
        safe_recipes = self.filter_recipes_by_allergens(recipes, allergens)
        feed = self.filter_unseen_recipes(safe_recipes, unseen)

        return feed

    # -------------------------------
    #  Helper: normalize field inputs
    # -------------------------------

    def _parse_list_field(self, field_value):
        """
        USING THIS ONE 
        Safely parse a list-like field (string, list, or None) into a Python list.
        Works for both Supabase (stringified JSON) and test data (list objects).
        """
        if field_value is None:
            return []
        if isinstance(field_value, list):
            return field_value
        if isinstance(field_value, str):
            try:
                # Remove quotes/brackets if manually stringified like "['Peanuts', 'Gluten']"
                return json.loads(field_value.replace("'", '"'))
            except Exception:
                # Fallback split for comma-separated or space-separated
                return [v.strip() for v in field_value.strip("[]").replace("'", "").split(",") if v.strip()]
        return []

    def _parse_list_field(self, field):
        NOT USING THIS ONE 
        """Ensure all list-like fields (JSON, text, or actual list) return a list of lowercase strings."""
        if not field:
            return []
        if isinstance(field, str):
            try:
                # Convert stringified list to Python list
                import ast
                parsed = ast.literal_eval(field)
                if isinstance(parsed, list):
                    return [str(x).strip().lower() for x in parsed]
            except Exception:
                # Fallback: treat as comma-separated string
                return [x.strip().lower() for x in field.split(",")]
        if isinstance(field, list):
            return [str(x).strip().lower() for x in field]
        return []

'''

from typing import Iterable, List, Dict, Any, Optional
import ast
import re


class RecipeUtility:
    """
    Works in two modes:
      - Offline (tests): pass `recipes` explicitly to generate_user_feed(...)
      - Online (runtime): construct with a supabase client and call generate_user_feed(None, user_data)
    """

    def __init__(self, supabase=None):
        self.supabase = supabase

    # ---------- helpers ----------

    def _as_list(self, value: Any) -> List[Any]:
        """Return a list from value; supports real lists or serialized Python list strings."""
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, (tuple, set)):
            return list(value)
        if isinstance(value, str):
            s = value.strip()
            # Try to parse "['a','b']" safely
            if s.startswith("[") and s.endswith("]"):
                try:
                    parsed = ast.literal_eval(s)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
            # fallback: comma-separated
            if "," in s:
                return [x.strip() for x in s.split(",") if x.strip()]
            if s:
                return [s]
        return []

    _CANON = {
        "peanut": "peanut",
        "peanuts": "peanut",
        "tree nut": "treenuts",
        "tree nuts": "treenuts",
        "treenut": "treenuts",
        "treenuts": "treenuts",
        "shellfish": "shellfish",
        "fish": "fish",
        "gluten": "gluten",
        "dairy": "dairy"
    }

    def _norm_token(self, s: str) -> str:
        """Lowercase, strip non-letters/spaces/underscores, collapse spaces, map to canonical."""
        t = (s or "").lower()
        # keep letters, spaces, underscores
        t = re.sub(r"[^a-z _]", "", t)
        t = t.replace("_", " ").strip()
        # collapse spaces
        t = re.sub(r"\s+", " ", t)
        # canonical map (tries full, then singular-ish)
        if t in self._CANON:
            return self._CANON[t]
        # quick singular-ish pass for simple plurals
        if t.endswith("s") and t[:-1] in self._CANON:
            return self._CANON[t[:-1]]
        return t

    def _norm_set(self, items: Iterable[Any]) -> set:
        return {self._norm_token(str(x)) for x in self._as_list(items) if str(x).strip()}

    def _recipe_id(self, recipe: Dict[str, Any]) -> Optional[int]:
        """Support either recipeid or id."""
        if "recipeid" in recipe:
            return recipe["recipeid"]
        if "id" in recipe:
            return recipe["id"]
        return None

    # ---------- core filters ----------

    def filter_recipes_by_allergens(
        self,
        recipes: List[Dict[str, Any]],
        user_allergens: Iterable[Any],
    ) -> List[Dict[str, Any]]:
        """Remove any recipe that contains a user allergen in either dietaryrestrictions or ingredients."""
        user_allergen_set = self._norm_set(user_allergens)

        filtered: List[Dict[str, Any]] = []
        for r in recipes:
            # collect tokens from both typical fields
            recipe_tokens = set()

            # dietaryrestrictions can be list or serialized string list
            recipe_tokens |= self._norm_set(r.get("dietaryrestrictions"))

            # ingredients can also contain allergen-y words
            recipe_tokens |= self._norm_set(r.get("ingredients"))

            # If *any* overlap with user allergens, drop it
            if recipe_tokens & user_allergen_set:
                continue

            filtered.append(r)

        return filtered

    def filter_unseen_recipes(
        self,
        recipes: List[Dict[str, Any]],
        unseen_ids: Iterable[Any],
    ) -> List[Dict[str, Any]]:
        """Keep only recipes whose id/recipeid is in 'unseen' (if unseen list provided); otherwise return recipes."""
        unseen_set = set(self._as_list(unseen_ids))
        if not unseen_set:
            # If no unseen list provided, don’t remove anything
            return list(recipes)

        kept: List[Dict[str, Any]] = []
        for r in recipes:
            rid = self._recipe_id(r)
            if rid in unseen_set:
                kept.append(r)
        return kept

    # ---------- feed ----------

    def _fetch_all_recipes(self) -> List[Dict[str, Any]]:
        if not self.supabase:
            return []
        resp = (
            self.supabase.table("recipes_public")
            .select("*")
            .order("datecreated", desc=True)
            .execute()
        )
        return resp.data or []

    def generate_user_feed(
        self,
        recipes_or_none: Optional[List[Dict[str, Any]]],
        user_data: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        If recipes_or_none is provided (tests), use it.
        If it’s None and supabase is set (runtime), we fetch from DB.
        """
        # 1) Gather recipes
        recipes = recipes_or_none if recipes_or_none is not None else self._fetch_all_recipes()

        # 2) Pull user fields flexibly
        allergens = self._as_list(user_data.get("allergens"))
        unseen = self._as_list(user_data.get("unseen_recipes"))

        # 3) Apply filters
        safe = self.filter_recipes_by_allergens(recipes, allergens)
        feed = self.filter_unseen_recipes(safe, unseen)

        return feed
