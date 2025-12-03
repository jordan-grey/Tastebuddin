# Installation and Execution Instructions

## Requirements
In order to run the program, you must have Docker installed and running.

## How to Run
1. Download the **Tastebuddin.zip** file. Extract into its own folder.
2. Open a terminal. In the terminal, navigate to the root of the Tastebuddin project. This is the same location as this **README.md** and the **docker-compose.yml**.
3. Run ```docker compose build```. This will create the docker container to run the project in.
4. Run ```docker compose up```. This will run the container that was just created in the previous step, and will begin hosting the frontend and backend of the website. This will also combine their functionalities so that the full website is accessible.
5. Open a browser. Any old one will do; the writer of this guide used Google Chrome.
6. Navigate to ```localhost:3000```. This should automatically  open up the ```index.html``` page, where you can navigate to Sign-in and Registration.
7. Create an account and log in. Once you are logged in, you should have access to all of the features Tastebuddin has to offer!

Supabase is always active, so there should not be anymore steps to running the web application. Should you encounter any issues attempting to run Tastebuddin, feel free to reach out to Tastebuddin's team members for more information.