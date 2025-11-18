import os
from supabase import create_client, Client 
from flask import jsonify
import traceback

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)


class user:
    def __init__(self, userdata:dict, uuid=""): #uuid is for testing. 
        self.email = userdata["email"]
        self.password = userdata["password"]
        self.username = userdata["username"]
        self.allergens= userdata["allergens"]
        self.uuid = uuid

    def create_auth(self):
        response = supabase.auth.sign_up(    
            {        
                "email": self.email,
                "password": self.password
        }
        )
        print(response.user.id)
        self.uuid = response.user.id

    def create_profile(self):
        try:
            print(self.uuid)
            data = {"id": self.uuid, 
                    "username": self.username,
                    "allergens": self.allergens
                    }
            response = (
                    supabase.table("users_public")
                    .insert(data)
                    .execute()
            )
            #print("Supabase insert response:", response)  # Debug line

            return {"message": "Profile created successfully", "data": response.data}
        except Exception as e:
            return {"error": str(e)}
        
    def get_user_with_id(uuid):
        response = (   
            supabase.table("users_public")    
            .select("*") 
            .eq("id", uuid)   
            .execute())
        return response
    
    def delete_profile(uuid): 
        #primarly used for testing purposes, only deletes profile line not auth
        response = (   
            supabase.table("users_public")    
            .delete() 
            .eq("id", uuid)   
            .execute())
        return response


    
