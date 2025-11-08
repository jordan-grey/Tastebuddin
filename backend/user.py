import os
from supabase import create_client, Client


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)
def get_user_data_with_id(uuid):
    response = (   
        supabase.table("users_public")    
        .select("*") 
        .eq("id", uuid)   
        .execute())
    return response

class user:
    def __init__(self, userdata:dict):
        self.email = userdata.email
        self.password = userdata.password
        self.username = userdata.username
        self.allergens= userdata.allergens
        self.uuid = "unset"

    def create_auth(self):
        response = supabase.auth.sign_up(    
            {        
                "email": self.email,
                "password": self.password
        }
        )
        self.uuid = response.user.id

    def create_profile(self):
        response = (
                supabase.table("users_public")
                .insert({"id": self.uuid, 
                         "username": self.username,
                         "allergens": self.allergens
                         })
                .execute()
        )


    
