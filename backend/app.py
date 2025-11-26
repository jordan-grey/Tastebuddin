import os   #accessing env varibles 
from flask import Flask, jsonify, request, render_template   #Flask for webapp, jsonify for return JSON response
from recipe_service import RecipeService
from recipe_utility import RecipeUtility
from supabase import create_client, Client 
import uuid
from leaderboard_service import LeaderboardService
from user_service import UserService

from flask_cors import CORS



app = Flask(__name__)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

CORS(app)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


service = RecipeService(supabase)
utility = RecipeUtility(supabase)
leaderboard_service = LeaderboardService(supabase)
user_service = UserService(supabase)


@app.route('/')
def index():
    return {"message": "CookSwipe API running!"}

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

@app.errorhandler(403)
def error_403(e):
    return render_template('403.html')

@app.route("/recipes", methods=["GET"])
def get_all_recipes():
    result = service.get_all_recipes()
    return jsonify(result), 200 if "error" not in result else 500

@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    result, status = service.get_recipe(recipe_id)
    return jsonify(result), status

@app.route("/recipes", methods=["POST"])
def create_recipe():
    data = dict(request.form) if request.form else request.json()
    image_file = request.files.get("image")
    result = service.create_recipe(data, image_file)
    return jsonify(result), 201 if "error" not in result else 400

@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    data = dict(request.form) if request.form else request.json()
    image_file = request.files.get("image")
    result = service.update_recipe(recipe_id, data, image_file)
    return jsonify(result), 200 if "error" not in result else 400

@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    result = service.delete_recipe(recipe_id)
    return jsonify(result), 200 if "error" not in result else 400

@app.route("/feed/<identifier>", methods=["GET"])
def get_user_feed(identifier):
    """
    Returns a personalized recipe feed for a given user.
    The identifier can be either a UUID (id) or a username (string).
    """
    try:
        print(f"[DEBUG] Feed request for identifier: {identifier}")

        # Detect whether identifier is a UUID or username
        query_col = "id" if is_valid_uuid(identifier) else "username"
        print(f"Querying users_public.{query_col} for {identifier}")

        # Fetch user info
        user_response = (
            supabase.table("users_public")
            .select("*")
            .eq(query_col, identifier)
            .execute()
        )

        if not user_response.data:
            print("⚠️ No user found for that identifier")
            return jsonify({"error": "User not found"}), 404

        user = user_response.data[0]
        print(f"Loaded user info: {user}")

        # Fetch all recipes
        recipe_response = supabase.table("recipes_public").select("*").execute()
        recipes = recipe_response.data or []

        print(f"📚 Retrieved {len(recipes)} total recipes")

        # Pass both datasets to your RecipeUtility class
        feed = utility.generate_user_feed(recipes, user)

        return jsonify({"data": feed}), 200

    except Exception as e:
        import traceback
        print("[ERROR TRACEBACK]")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



def is_valid_uuid(value):
    """Helper: Check if a string looks like a valid UUID."""
    import uuid
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False
    

@app.route("/leaderboard/daily", methods=["GET"])
def get_daily_leaderboard():
    result, status = leaderboard_service.get_daily_leaderboard(limit=10)
    return jsonify({"data": result}), status

@app.route("/leaderboard/weekly", methods=["GET"])
def leaderboard_weekly():
    result, status = leaderboard_service.get_weekly_leaderboard(limit=10)
    return jsonify({"data": result}), status

@app.route("/leaderboard/authors", methods=["GET"])
def leaderboard_authors():
    result, status = leaderboard_service.get_author_leaderboard(limit=10)
    return jsonify({"data": result}), status

@app.route("/user/exists/<username>", methods=["GET"])
def check_username_exists(username):
    """
    Returns {exists: true/false} depending on whether
    the username already exists in users_public.
    """
    try:
        # IMPORTANT: match your real table name
        result = (
            supabase
            .table("users_public")
            .select("username")
            .eq("username", username)
            .execute()
        )

        exists = len(result.data) > 0
        return jsonify({"exists": exists}), 200

    except Exception as e:
        print("ERROR in /user/exists:", e)
        return jsonify({"exists": False, "error": str(e)}), 500




@app.route("/user/create", methods=["POST"])
def create_user_route():
    data = request.json
    user_id = data.get("user_id")
    username = data.get("username")
    allergens = data.get("allergens", [])

    if not user_id or not username:
        return jsonify({"error": "Missing required fields"}), 400

    # 1) Validate username format (ALWAYS enforce this server-side)
    import re
    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        return jsonify({"error": "Invalid username format"}), 400

    # 2) Ensure username is unique
    exists_check = (
        supabase
        .table("users_public")
        .select("username")
        .eq("username", username)
        .execute()
    )

    if exists_check.data:
        return jsonify({"error": "Username already taken"}), 409

    # 3) Create the user using your user_service

    recipes_response = (
        supabase.table("recipes_public")
        .select("recipeid, dietaryrestrictions")
        .execute()
    )

    all_recipes = recipes_response.data or []

    # 2. Filter with simplified function
    unseen_ids = utility.filter_unseen_by_allergens(
        all_recipes,
        allergens
    )

    # 2. Run the allergen filter (returns IDs only)
    filtered_unseen_ids = utility.filter_unseen_by_allergens(
        all_recipes, allergens
    )


    result, status = user_service.create_user(user_id, username, allergens, filtered_unseen_ids)

    if status != 200:
        return jsonify(result), status

    # 4) Add allergens, if provided
    if allergens:
        user_service.update_allergens(user_id, allergens)

    return jsonify({"message": "User created", "data": result}), 200


@app.route("/user/like", methods=["POST"])
def like_recipe_route():
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
    data = request.json

    user_id = data.get("user_id")
    recipe_id = data.get("recipe_id")

    if not user_id or recipe_id is None:
        return jsonify({"error": "Missing required fields"}), 400

    result, status = user_service.dislike_recipe(user_id, recipe_id)
    return jsonify(result), status


@app.route("/config")
def get_config():
    return jsonify({
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY")
    })

@app.route("/user/<user_id>/liked", methods=["GET"])
def get_liked_recipes(user_id):
    svc = RecipeService(supabase)
    data, status = svc.get_liked_recipes(user_id)
    return jsonify(data), status


# @app.route("/recipe/<int:recipe_id>", methods=["GET"])
# def get_recipe(recipe_id):
#     svc = RecipeService(supabase)
#     data, status = svc.get_recipe_by_id(recipe_id)
#     return jsonify(data), status


if __name__ == '__main__':
    app.run(debug=True)