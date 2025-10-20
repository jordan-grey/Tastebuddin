import os   #accessing env varibles 
from flask import Flask, jsonify, request   #Flask for webapp, jsonify for return JSON response
from dotenv import load_dotenv      # to load env variables from .env file
from supabase import create_client, Client   # Client to act with datbase 


#load env varibles from .env file
load_dotenv()   


#create flask instance 
app = Flask(__name__)

#Fetch creditenals for database 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

#Initialize the Supabase Client 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#Root route just to test if server is running
@app.route('/')
def index():
    return "Flask & Supabase connected!"

#route to fetch all users fro the "users" table in Supabase 
@app.route('/users')
def get_users():
    #featch all rows from the 'users' table 
    response = supabase.table("users").select("*").execute()

    #retrun the fetch data as JSON 
    return jsonify(response.data)

@app.route("/recipes", methods=["GET", "POST"])
def handle_recipes():
    if request.method == "POST":
        data = request.json
        print("Received:", data)
        response = supabase.table("recipes").insert(data).execute()
        print("Supabase response:", response)
        return jsonify(response.data), 201

    elif request.method == "GET":
        response = supabase.table("recipes").select("*").execute()
        return jsonify(response.data), 200

# GET one recipe, UPDATE, or DELETE
@app.route("/recipes/<id>", methods=["GET", "PUT", "DELETE"])
def handle_single_recipe(id):
    if request.method == "GET":
        response = supabase.table("recipes").select("*").eq("recipe_id", id).execute()
        return jsonify(response.data[0] if response.data else {}), 200

    elif request.method == "PUT":
        data = request.json
        response = supabase.table("recipes").update(data).eq("recipe_id", id).execute()
        return jsonify(response.data), 200

    elif request.method == "DELETE":
        response = supabase.table("recipes").delete().eq("recipe_id", id).execute()
        return jsonify(response.data), 200



if __name__ == '__main__':
    app.run(debug=True)
