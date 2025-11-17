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
        "dairy": "dairy",
        "vegetarian": "vegetarian",
        "pork": "prok",
        "egg": "egg",
        "eggs": "egg",
        "halal": "halal"
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
