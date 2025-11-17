import os
from supabase import create_client, Client 
from flask import jsonify
import traceback



class User:
    def __init__(self, supabase, uuid=""): #uuid is for testing. 
        self.email = ""
        self.password = ""
        self.username = ""
        self.allergens= ""
        self.uuid = uuid
        self.table_name = "users_public"
        self.supabase = supabase

    def create_auth(self, authdata:dict):
        self.email = authdata["email"]
        self.password = authdata["password"]
        response = self.supabase.auth.sign_up(    
            {        
                "email": self.email,
                "password": self.password
        }
        )
        print(response.user.id)
        self.uuid = response.user.id

    def create_profile(self, profiledata:dict):
        self.username = profiledata["username"]
        self.allergens= profiledata["allergens"]
        try:
            print(self.uuid)
            data = {"id": self.uuid, 
                    "username": self.username,
                    "allergens": self.allergens
                    }
            response = (
                    self.supabase.table(self.table_name)
                    .insert(data)
                    .execute()
            )
            #print("Supabase insert response:", response)  # Debug line

            return {"message": "Profile created successfully", "data": response.data}
        except Exception as e:
            return {"error": str(e)}
        
    def get_user_with_id(self, uuid):
        response = (   
            self.supabase.table(self.table_name)    
            .select("*") 
            .eq("id", uuid)   
            .execute())
        return response
    
    def get_user_with_username(self, username):
        try:
            response = (
                self.supabase.table(self.table_name)    
                .select("*") 
                .eq("username", username)   
                .execute()
            )
            if not response.data:
                return {"error": "User not found"}, 404
            return {"data": response.data}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def delete_profile(self, uuid): 
        #primarly used for testing purposes, only deletes profile line not auth
        response = (   
            self.supabase.table(self.table_name)    
            .delete() 
            .eq("id", uuid)   
            .execute())
        return response


    
