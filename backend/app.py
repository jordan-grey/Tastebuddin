import os   #accessing env varibles 
from flask import Flask, jsonify, request, render_template   #Flask for webapp, jsonify for return JSON response
from dotenv import load_dotenv      # to load env variables from .env file
from supabase import create_client, Client  # Client to act with datbase 


#load env varibles from .env file
load_dotenv()   


#create flask instance 
app = Flask(__name__)

#Fetch creditenals for database 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

#Initialize the Supabase Client 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

## -----------------------------
#   User Login Functions
# -----------------------------

@app.route('/login', methods=['POST'])
def register_auth(email, password):
    response = supabase.auth.sign_up({        
        "email": email,        
        "password": password})
    return response
def register_auth(email, password):
    response = supabase.auth.sign_in_with_password({        
        "email": email,        
        "password": password})
    return response
## -----------------------------
#   Recipe CRUD FUNCTIONS
# -----------------------------

@app.route('/recipes', methods=['POST'])
def create_recipe():
    """init(Dict Data) : RecipeID"""
    data = request.get_json()
    try:
        response = supabase.table("recipes").insert(data).execute()
        return jsonify({"message": "Recipe created successfully", "data": response.data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def edit_recipe(recipe_id):
    """edit(RecipeID, Dict Data) : Error code"""
    data = request.get_json()
    try:
        response = supabase.table("recipes").update(data).eq("recipe_id", recipe_id).execute()
        if response.data:
            return jsonify({"message": "Recipe updated", "data": response.data}), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """delete(RecipeID) : error code"""
    try:
        response = supabase.table("recipes").delete().eq("recipe_id", recipe_id).execute()
        if response.data:
            return jsonify({"message": "Recipe deleted"}), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """get(RecipeID) : Dict Data"""
    try:
        response = supabase.table("recipes").select("*").eq("recipe_id", recipe_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        else:
            return jsonify({"error": "Recipe not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    """Optional: view all recipes"""
    try:
        response = supabase.table("recipes").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

@app.errorhandler(403)
def error_403(e):
    return render_template('403.html')


@app.route('/')
def index():
    return jsonify({"message": "Tastebuddin API running!"})
if __name__ == '__main__':
    app.run(debug=True)
