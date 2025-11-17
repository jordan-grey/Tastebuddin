import os   #accessing env varibles 
from flask import Flask, jsonify, request, render_template   #Flask for webapp, jsonify for return JSON response
from flask_cors import CORS
from recipe_service import RecipeService
from recipe_utility import RecipeUtility
from user import User
from dotenv import load_dotenv
from supabase import create_client, Client 
import uuid
from leaderboard_service import LeaderboardService


app = Flask(__name__)
CORS(app)  # allow frontend container to talk to backend
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


service = RecipeService(supabase)
utility = RecipeUtility(supabase)
leaderboard_service = LeaderboardService(supabase)
user = User(supabase)

@app.route('/')
def index():
    return {"message": "CookSwipe API running!"}

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

@app.errorhandler(403)
def error_403(e):
    return render_template('403.html')

@app.route("/user/<string:username>", methods=["GET"])
def get_user_data(username):
    result, status = user.get_user_with_username(username)
    return jsonify(result), status



@app.route("/signup", methods=["POST"])
def signup():
    # Retrieve form fields:
    profiledata = request.get_json()  
    user_instance = User(supabase)
    result, status = user_instance.create_profile(profiledata)
    return jsonify(result), status

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
    return jsonify(result), status

@app.route("/leaderboard/weekly", methods=["GET"])
def leaderboard_weekly():
    result, status = leaderboard_service.get_weekly_leaderboard(limit=10)
    return jsonify(result), status

@app.route("/leaderboard/authors", methods=["GET"])
def leaderboard_authors():
    result, status = leaderboard_service.get_author_leaderboard(limit=10)
    return jsonify(result), status

if __name__ == '__main__':
    app.run(debug=True)