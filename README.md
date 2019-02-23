# YumBot

## Description
A web application providing customized recipes created by the YumBot

## How to run
First ensure that you have Python version 2.6+ installed on your machine. To confirm,
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
   
## Making Changes

### Add new endpoints
Create new endpoints for your application or API in the file **app/views.py**

### Edit HTML Templates
Currently there is a **layout.html** file in **app/templates** which contains basic headers and links to the basic css and js files in **app/static/css/index.css** and **app/static/js/index.js**.
Create new templates which extend **layout.html** following the format of **app/templates/index.html**

### Change the host and port
By default, this application runs on **127.0.0.1:8095**. Change the default host and port in **run.py** or run it on a different host and port using the --host and --port flags. For example,

    ./run.py --host <your-host> --port <your-port>
