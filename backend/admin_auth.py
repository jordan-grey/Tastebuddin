"""
SUPABASE AUTH ADMIN
Sarah temple - Nov 2 2025

This is needed to manage test cases where deletion of accounts in auth is necessary. 

We also need this for 
"""


import os
from supabase import create_client
from supabase.lib.client_options import ClientOptions
from flask import Flask, jsonify, request, render_template   #Flask for webapp, jsonify for return JSON response
from dotenv import load_dotenv      # to load env variables from .env file

#load env varibles from .env file
load_dotenv()   


#create flask instance 
app = Flask(__name__)

#Fetch creditenals for database 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_S_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(    
    SUPABASE_URL,    
    SUPABASE_S_KEY,    
    options=ClientOptions(        
        auto_refresh_token=False,        
        persist_session=False,    
    )
)
def delete_account(account_id):
    results = supabase.auth.admin.delete_user(account_id)
    return results
#Access auth admin api

admin_auth_client = supabase.auth.admin