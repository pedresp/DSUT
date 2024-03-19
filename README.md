# DRONE_SETUP_TOOL

## Index

 - [Description](#item_one)
    
    - [templates](#item_one_one)
    - [classes.py](#item_one_two)
    - [drone_setup.py](#item_one_three)
    - [utils.py](#item_one_four)
 - [Requirements](#item_two)
 - [How to use](#item_three)

<a id=item_one></a>
## Description

The proyect is divided into different sectiones according to their function, which is explained below.

<a id=item_one_one></a>
### templates

This folder contains the templates that the application will be using. It is divided into two folders: 
    
 - **files**: contains the templates of the configuration files for the ROS packages to run 
 - **webpages**: contains the template of the webpage

<a id=item_one_two></a>
### clases.py

This class defines the Drone class and adds a constractor for it.

<a id=item_one_three></a>
### drone_setup.py

This class contains the full functionality of the API and how the webpage reacts.

<a id=item_one_four></a>
### utils.py

This class contains helpful funtions for the drone_setup.py file

<a id=item_two></a>
## Requirements

To run this app you need to meet the following requirements:
   - python3.10 or greater
   - Flask (you can install it via *pip install Flask*)

<a id=item_three></a>
## How to use

In order to execute the app is **essential to specify** the **ROS2_WORKSPACE** that you are using.

To do that, you **need to change** in the value of the variable **ros_ws** in the [drone_setup.py](#item_one_three) file. Right now the value of the variable is defined in line 9.

**IMPORTANT**: this webapp assumes that the ROS2 workspace that is being used is located in the home directory of the user. 
So for the program to run as expected, the **ros_ws** variable should be a relative path to the ros2 workspace from the home directory of the user.

Once the **ros_ws** has been configured, you only have to execute the following command:
   
      python3 drone_setup.py

After executing the command, you will need to open your browser and introduce the following url:

      http://localhost:5000/

Now you should see the webpage and be able to add/modify drones statistics.