# YumBot

## Description
A web application providing customized recipes created by the YumBot

## How to run

First, get a Spoonacular API key by visiting [this](https://rapidapi.com/spoonacular/api/recipe-food-nutrition/pricing) site. Select the basic plan. Then, in the Rapid API dashboard, click "Add New App" on the left navigation bar. Name the application "YumBot".  YumBot should not show up in your "My Apps" section on the left navigation bar. Then, select YumBot and in the dropdown menu, click on "Security". You should be able to see your API key. Copy this key and set it as an environment variable on your machine by typing this command in a terminal window

    export SPOONACULAR_API_KEY=<your-key>

Then, ensure that you have Python version 2.6+ installed on your machine. To confirm,
open a terminal and run the following command to ensure that python is installed and it is the correct version.

    python --version
Then,
#### 1. Clone this repository


        git clone https://github.com/SrutiG/YumBot.git
#### 2. Navigate to the flask_boilerplate folder

        cd YumBot
#### 3. Install the necessary requirements
    
        pip install --user -r requirements.txt
#### 4. Make sure that the run.py file has executable permissions

        chmod +x run.py
#### 5. Run this command

        ./run.py
#### 6. Navigate to the URL *127.0.0.1:8095* in your browser
   A page should appear saying *Hello World*.
   
## Create the Database

This application currently uses a SQLite database generated in the **app** folder. In order to create the database, run the following commands.

#### 1. Give executable permissions to the db_create.py and db_migrate.py files
        chmod +x db_create.py && chmod +x db_migrate.py
        
#### 2. Run db_create.py to create the database
        ./db_create.py
        
#### 3. Run db_migrate.py to create the migrations based on the current schema
        ./db_migrate.py
        
## Populate the database

The file **modify_db.py** can be used to add/remove recipes from the database and run algorithms. Make sure it has executable permissions by running the following command
            
    chmod +x modify_db.py
    
Then, run it with your chosen arguments.

    ./modify_db.py [args]
    
These are the available arguments

| argument name | type   | default value | possible values                                                    | description                                                                                                                                                                                                                                                                                                                                |
|---------------|--------|---------------|--------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| action        | string | add           | add, remove, matrix, pca, kmeans, add_calc, remove_calc | **add**: add recipes to the database. Use numrecipes arg to set number of recipes to add. Default is 10  **remove**: remove recipes from the database. Use numrecipes flag to set number of recipes to remove.  **matrix**: recreate the co-occurrence matrix based on current recipes in the database. This is done automatically after adding recipes.  **pca**: calculate pca coordinates based on current co-occurrence matrix. **kmeans**: calculate kmeans clusters based on pca coordinates.  **add_calc**: add recipes to database, calculate pca coordinates and kmeans coordinates. Use numrecipes to set number of recipes to add.  **remove_calc**: remove recipes from database. calculate pca coordinates and kmeans coordinates. Use numrecipes to set number of recipes to remove.|
| numrecipes    | int    | 10            | any integer >= 0                                                   | number of recipes to add or remove from the database                                                                                                                                                                                                                                                                                       |
| components    | int    | 24            | any integer between 0 and 24                                       | number of PCA components                                                                                                                                                                                                                                                                                                                   |
| clusters      | int    | 35            | any positive integer                                               | number of k-means clusters 
   
## Other files

### Add new endpoints
Create new endpoints for the application in the file **app/views.py**

### Edit HTML Templates
Currently there is a **layout.html** file in **app/templates** which contains the topbar, headers, and links to the css and js files in **app/static/css/index.css** and **app/static/js/index.js**.
Create new templates which extend **layout.html**.

### Change the host and port
By default, this application runs on **127.0.0.1:8095**. Change the default host and port in **run.py** or run it on a different host and port using the --host and --port flags. For example,

    ./run.py --host <your-host> --port <your-port>
