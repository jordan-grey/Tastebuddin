import os   #accessing env varibles 
from flask import Flask, jsonify, request, render_template   #Flask for webapp, jsonify for return JSON response
from flask_cors import CORS
from recipe_service import RecipeService
from dotenv import load_dotenv
import recipe_service  # Import your module f   # to load env variables from .env file
from supabase import create_client, Client 
import recipe_service   # Client to act with datbase 


app = Flask(__name__)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
#CORS(app)

service = RecipeService(supabase)

@app.route('/')
def index():
    return {"message": "CookSwipe API running!"}
'''
# ---------- Recipe Routes ----------
@app.route('/recipes', methods=['GET'])
def get_recipes():
    return recipe_service.get_all_recipes()

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    return recipe_service.get_recipe_by_id(recipe_id)

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    return recipe_service.create_recipe(data)

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def edit_recipe(recipe_id):
    data = request.get_json()
    return recipe_service.update_recipe(recipe_id, data)

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def remove_recipe(recipe_id):
    return recipe_service.delete_recipe(recipe_id)

@app.route("/recipes/unseen/<user_id>", methods=["GET"])
def get_filtered_unseen_recipes(user_id):
    from recipe_service import filter_recipes_by_restrictions
    filtered_recipes = filter_recipes_by_restrictions(user_id)
    return jsonify(filtered_recipes), 200


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

@app.errorhandler(403)
def error_403(e):
    return render_template('403.html')

'''

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
    data = request.get_json()
    result = service.create_recipe(data)
    return jsonify(result), 201 if "error" not in result else 400

@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    data = request.get_json()
    result = service.update_recipe(recipe_id, data)
    return jsonify(result), 200 if "error" not in result else 400

@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    result = service.delete_recipe(recipe_id)
    return jsonify(result), 200 if "error" not in result else 400
if __name__ == '__main__':
    app.run(debug=True)