"""
===============================================================================
File: app.py
Project: TasteBuddin Social Recipe Discovery Platform
Creation Date: Dec 4, 2025
Authors: Kadee Wheeler, ChatGPT Assistant

Description:
    This backend file defines the Flask web server for the TasteBuddin system.
    TasteBuddin is a recipe-sharing platform where users can:
      • Create, edit, and delete their own recipes
      • Browse an algorithmically generated swipe-style feed
      • Like/dislike recipes and collect favorites
      • View personal leaderboards and community rankings
      • Maintain user profiles & preferences (e.g., allergens)

    This file wires together:
      - Flask routing layer
      - Supabase database client
      - Recipe, User, and Leaderboard service classes
      - CORS handling for frontend communication
===============================================================================
"""

# =============================================================================
# IMPORTS — System, Libraries, and Application Services
# =============================================================================

import os                                   # Reads environment variables for configuration
from flask import Flask, jsonify, request   # Web framework utilities for JSON APIs
from flask import render_template           # Optional: HTML rendering
from flask_cors import CORS                 # Enables CORS for frontend communication
from supabase import create_client, Client  # Supabase DB + Storage client
import uuid                                 # Used for unique identifiers

# Internal service classes encapsulating business logic
from recipe_service import RecipeService
from recipe_utility import RecipeUtility
from leaderboard_service import LeaderboardService
from user_service import UserService


# =============================================================================
# FLASK APP INITIALIZATION & CONFIGURATION
# =============================================================================

app = Flask(__name__)

# Load Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Enable CORS for all routes (frontend ↔ backend communication)
CORS(app, supports_credentials=True, origins="*")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize services
service = RecipeService(supabase)
utility = RecipeUtility(supabase)
leaderboard_service = LeaderboardService(supabase)
user_service = UserService(supabase)


# =============================================================================
# ROUTE: ROOT / STATIC PAGES
# =============================================================================
@app.route("/")
def home():
    """
    Purpose:
        Serve main homepage (index.html).

    Returns:
        Static HTML file.
    """
    return app.send_static_file("index.html")


@app.errorhandler(404)
def error_404(e):
    """Serve custom 404 page."""
    return app.send_static_file('404.html')


@app.errorhandler(403)
def error_403(e):
    """Serve custom 403 page."""
    return app.send_static_file('403.html')


# =============================================================================
# ROUTES: RECIPE CRUD (Create, Read, Update, Delete)
# =============================================================================

@app.route("/recipes", methods=["GET"])
def get_recipes():
    """
    Purpose:
        Fetch recipes. If `authorid` is provided, fetch only that user's recipes.

    Query Params:
        authorid (str) — Optional user ID to filter recipes.

    Returns:
        JSON list of recipe objects.
    """
    authorid = request.args.get("authorid")

    if authorid:
        result = service.get_recipes_by_author(authorid)
        return jsonify(result), 200

    result = service.get_all_recipes()
    return jsonify(result), 200


@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    """
    Purpose:
        Retrieve details for a single recipe.

    Args:
        recipe_id (int): Recipe identifier.

    Returns:
        (JSON, status_code): Recipe details or error.
    """
    result, status = service.get_recipe(recipe_id)
    return jsonify(result), status


@app.route("/recipes", methods=["POST"])
def create_recipe():
    """
    Purpose:
        Create a new recipe.

    Body:
        form-data including:
            - title, description, category, ingredients, directions, etc.
            - image (optional)

    Returns:
        Newly created recipe or error.
    """
    data = dict(request.form) if request.form else request.json()
    image_file = request.files.get("image")
    result = service.create_recipe(data, image_file)
    return jsonify(result), 201 if "error" not in result else 400


@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    """
    Purpose:
        Update a recipe with new values.

    Args:
        recipe_id (int): Target recipe.

    Returns:
        Success or failure JSON payload.
    """
    data = dict(request.form) if request.form else request.json()
    image_file = request.files.get("image")
    result = service.update_recipe(recipe_id, data, image_file)
    return jsonify(result), 200 if "error" not in result else 400


@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    """
    Purpose:
        Delete a recipe permanently.

    Args:
        recipe_id (int)

    Returns:
        Confirmation JSON.
    """
    result = service.delete_recipe(recipe_id)
    return jsonify(result), 200 if "error" not in result else 400


# =============================================================================
# FEED GENERATION — Personalized Swipe Feed
# =============================================================================

@app.route("/feed/<identifier>", methods=["GET"])
def get_user_feed(identifier):
    """
    Purpose:
        Generate a personalized recipe feed for a given user.

    Args:
        identifier (str):
            - UUID user ID OR
            - Username

    Logic:
        1. Determine whether identifier is UUID or username.
        2. Load that user from DB.
        3. Load all recipes.
        4. Send both into RecipeUtility to compute feed ordering.

    Returns:
        {"data": feed_list} or error.
    """
    try:
        query_col = "id" if is_valid_uuid(identifier) else "username"

        user_response = (
            supabase.table("users_public")
            .select("*")
            .eq(query_col, identifier)
            .execute()
        )

        if not user_response.data:
            return jsonify({"error": "User not found"}), 404

        user = user_response.data[0]

        # Load all recipes
        recipe_response = supabase.table("recipes_public").select("*").execute()
        recipes = recipe_response.data or []

        feed = utility.generate_user_feed(recipes, user)

        return jsonify({"data": feed}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def is_valid_uuid(value):
    """
    Purpose:
        Utility to check if a string is a valid UUID.

    Args:
        value (str)

    Returns:
        bool — True if valid UUID.
    """
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


# =============================================================================
# LEADERBOARD ROUTES — Daily, Weekly, Authors
# =============================================================================

@app.route("/leaderboard/daily", methods=["GET"])
def get_daily_leaderboard():
    """Return top recipes of the day."""
    result, status = leaderboard_service.get_daily_leaderboard(limit=10)
    return jsonify({"data": result}), status


@app.route("/leaderboard/weekly", methods=["GET"])
def leaderboard_weekly():
    """Return top recipes of the week."""
    result, status = leaderboard_service.get_weekly_leaderboard(limit=10)
    return jsonify({"data": result}), status


@app.route("/leaderboard/authors", methods=["GET"])
def leaderboard_authors():
    """Return top-ranked recipe authors."""
    result, status = leaderboard_service.get_author_leaderboard(limit=10)
    return jsonify({"data": result}), status


# =============================================================================
# USER MANAGEMENT — Create, Update, Likes, Collections
# =============================================================================

@app.route("/user/exists/<username>", methods=["GET"])
def check_username_exists(username):
    """
    Purpose:
        Check if username is already taken.

    Returns:
        {"exists": bool}
    """
    try:
        result = (
            supabase.table("users_public")
            .select("username")
            .eq("username", username)
            .execute()
        )

        exists = len(result.data) > 0
        return jsonify({"exists": exists}), 200

    except Exception as e:
        return jsonify({"exists": False, "error": str(e)}), 500


@app.route("/user/create", methods=["POST"])
def create_user_route():
    """
    Purpose:
        Create a new user account + initialize allergen filtering.

    Body:
        { user_id, username, allergens }

    Returns:
        Newly created user.
    """
    data = request.json
    user_id = data.get("user_id")
    username = data.get("username")
    allergens = data.get("allergens", [])

    # Validation
    if not user_id or not username:
        return jsonify({"error": "Missing required fields"}), 400

    import re
    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        return jsonify({"error": "Invalid username format"}), 400

    exists_check = (
        supabase.table("users_public")
        .select("username")
        .eq("username", username)
        .execute()
    )
    if exists_check.data:
        return jsonify({"error": "Username already taken"}), 409

    # Load all recipes for unseen filtering
    recipes_response = supabase.table("recipes_public").select("recipeid,dietaryrestrictions").execute()
    all_recipes = recipes_response.data or []

    filtered_ids = utility.filter_unseen_by_allergens(all_recipes, allergens)

    result, status = user_service.create_user(user_id, username, allergens, filtered_ids)

    if status != 200:
        return jsonify(result), status

    # Save allergens if given
    if allergens:
        user_service.update_allergens(user_id, allergens)

    return jsonify({"message": "User created", "data": result}), 200


@app.route("/user/like", methods=["POST"])
def like_recipe_route():
    """
    Purpose:
        Like a recipe ("swipe right").

    Body:
        { user_id, recipeid, author_id }

    Returns:
        Updated user record or error.
    """
    data = request.json
    user_id = data.get("user_id")
    recipe_id = data.get("recipeid")
    author_id = data.get("author_id")

    if not user_id or recipe_id is None or not author_id:
        return jsonify({"error": "Missing required fields"}), 400

    result, status = user_service.like_recipe(user_id, recipe_id, author_id)
    return jsonify(result), status


@app.route("/user/dislike", methods=["POST"])
def dislike_recipe_route():
    """
    Purpose:
        Dislike/remove a recipe from collection.

    Body:
        { user_id, recipe_id }

    Returns:
        Updated user record or error.
    """
    data = request.json
    user_id = data.get("user_id")
    recipe_id = data.get("recipe_id")

    if not user_id or recipe_id is None:
        return jsonify({"error": "Missing required fields"}), 400

    result, status = user_service.dislike_recipe(user_id, recipe_id)
    return jsonify(result), status


@app.route("/user/<user_id>/liked", methods=["GET"])
def get_liked_recipes(user_id):
    """
    Purpose:
        Fetch all recipes the user has liked/saved.

    Args:
        user_id (str)

    Returns:
        {"data": [recipe, ...]}
    """
    data, status = user_service.get_liked_recipes(user_id)
    return jsonify(data), status


# =============================================================================
# USER PROFILE — Retrieve & Update Public Data
# =============================================================================

@app.route("/api/user_public/<username>", methods=["GET"])
def get_user(username):
    """
    Purpose:
        Fetch a user's public profile information.

    Args:
        username (str)

    Returns:
        JSON profile or error.
    """
    try:
        user = user_service.get_user_by_username(username)
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/user_public/<username>", methods=["PUT"])
def update_user(username):
    """
    Purpose:
        Update a user's public profile fields.

    Body:
        JSON containing fields to update.

    Returns:
        Updated user object.
    """
    try:
        data = request.json
        updated = user_service.update_user_by_username(username, data)
        return jsonify(updated)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================================================================
# SERVER ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    """
    Launch the Flask development server.
    Debug=True enables hot reload and full error traces.
    """
    app.run(debug=True)
