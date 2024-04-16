from flask import Flask, render_template, request, redirect, url_for
import classes as c
import utils

import os
import pwd
import json

drones_bag = {}
perimeter_points = []
perimeter_str = ''
fly_height = 8.0
ros_ws = 'ros_tfg'
route = f"/home/{pwd.getpwuid(os.getuid()).pw_name}/{ros_ws}/src"
downloads = f"/home/{pwd.getpwuid(os.getuid()).pw_name}/Downloads"

print(route)

app = Flask(__name__)

'''Method to represent the actual state of the drones bag'''
@app.route("/", methods=['GET'])
def index():
    print(perimeter_str)
    return render_template("webpage/index.html", drones_bag=drones_bag, next_drone=utils.next_drone(drones_bag), fly_height=fly_height, perimeter=perimeter_str, downloads=downloads)

'''Method to add a brand new drone from the data introduced in the first form'''
@app.route("/add_drone", methods=['POST'])
def basic_add_drone():
    my_data = request.form.to_dict()

    drone_id = my_data["drone_id"]
    drone_speed = float(my_data["drone_speed"])
    drone_acc = float(my_data["drone_acc"])
    drone_tof = float(my_data["drone_tof"])
    drone_sweep_width = float(my_data["drone_sweep_width"])
    drone_coordx = float(my_data["drone_coordx"])
    drone_coordy = float(my_data["drone_coordy"])

    drones_bag[drone_id] = c.Drone(drone_id, drone_speed, drone_acc, drone_tof, drone_sweep_width, drone_coordx, drone_coordy)
    return redirect(url_for("index"))

'''Method to change height'''
@app.route('/change_height', methods=['POST'])
def change_height():
    global fly_height
    my_data = request.form.to_dict()

    fly_height = float(my_data['fly_height'])

    return redirect(url_for("index"))

'''Method to modify/delete or add a copy of an existing drone'''
@app.route("/action_on_drone", methods=['POST'])
def modify_drone():
    my_data = request.form.to_dict()

    drone_id = my_data["drone_id"]
    drone_speed = float(my_data["drone_speed"])
    drone_acc = float(my_data["drone_acc"])
    drone_tof = float(my_data["drone_tof"])
    drone_sweep_width = float(my_data["drone_sweep_width"])
    drone_coordx = float(my_data["drone_coordx"])
    drone_coordy = float(my_data["drone_coordy"])

    if (my_data['aod'] == 'modify_drone'):
        drones_bag[drone_id].speed = drone_speed
        drones_bag[drone_id].acc = drone_acc
        drones_bag[drone_id].tof = drone_tof
        drones_bag[drone_id].sweep_width = drone_sweep_width
        drones_bag[drone_id].coordx = drone_coordx
        drones_bag[drone_id].coordy = drone_coordy
    elif (my_data['aod'] == 'remove_drone'):
        del drones_bag[drone_id]
    else:
        new_drone = utils.next_drone(drones_bag)
        drones_bag[new_drone] = c.Drone(new_drone, drone_speed, drone_acc, drone_tof, drone_sweep_width, drone_coordx, drone_coordy)

    return redirect(url_for("index"))

@app.route("/perimeter", methods=['POST'])
def perimeter():
    global perimeter_str, perimeter_points

    my_data = request.form.to_dict()['textbox']
    print("my data:", my_data)
    return_list = utils.read_coords(my_data)

    perimeter_str = my_data if not return_list == None else 'an error ocurred!'
    perimeter_points = return_list 

    return redirect(url_for("index"))


@app.route("/export_json", methods=['GET'])
def export_json():
    global perimeter_points, perimeter_str

    _route = request.args.get('e_json')

    dictionary = {}
    dictionary["perimeter_points"] = perimeter_points
    dictionary["perimeter_str"] = perimeter_str
    dictionary["height"] = fly_height
    dictionary["drones_bag"] = drones_bag

    json_dict = json.dumps(dictionary, default=c.dronson, indent=4)

    with open(f"{_route}/exported.json", "w") as file:
        file.write(json_dict)

    return redirect(url_for("index"))

@app.route("/import_json", methods=['POST'])
def import_json():
    global perimeter_points, perimeter_str, fly_height, drones_bag

    imp_json = request.form.to_dict()['i_json']

    with open(imp_json, "r") as file:
        file_content = file.read()
        config_dict = json.loads(file_content)
        c.jsondrone(config_dict['drones_bag'])
        perimeter_points = config_dict['perimeter_points']
        perimeter_str = config_dict['perimeter_str']
        fly_height = config_dict['height']
        drones_bag = config_dict['drones_bag']        

    return redirect(url_for("index"))

'''Method to generate the configuration and launcher files that are
described in the web page'''
@app.route("/generate_config", methods=['POST'])
def generate_config():
    for drone_key, drone_value in drones_bag.items():
        content = render_template('files/drone_template.yaml', drone_id=drone_key, drone_speed=drone_value.speed, drone_acc=drone_value.acc, \
                                  drone_tof=drone_value.tof, drone_sweep_width=drone_value.sweep_width, drone_coordx=drone_value.coordx, \
                                  drone_coordy= drone_value.coordy)
        print(f"{route}/simplesim/waypoints/{drone_key}.yaml")
        with open(f"{route}/simplesim/waypoints/{drone_key}.yaml", 'w', encoding='utf-8') as outf:
            outf.write(content)
        conf_content = render_template('files/drone_template_config.yaml', drone_id=drone_key, drone_speed=drone_value.speed, drone_acc=drone_value.acc, \
                                  drone_tof=drone_value.tof, drone_sweep_width=drone_value.sweep_width, drone_coordx=drone_value.coordx, \
                                  drone_coordy= drone_value.coordy)
        with open(f"{route}/simplesim/config/{drone_key}.yaml", "w", encoding='utf-8') as coutf:
            coutf.write(conf_content)
    
    minus1_list = list(drones_bag.items())[1:]
    element = list(drones_bag.items())[0][0]
    launch_content = render_template('files/launcher_template.txt', drones_bag=minus1_list, last_drone=element, drones_number= float(len(drones_bag)), \
                                     height=fly_height)
    with open(f"{route}/simplesim/launch/my_launcher_drones.launch.py", 'w', encoding='utf-8') as launch_config:
        launch_config.write(launch_content)

    rviz_content = render_template('files/rviz.yaml', drones_bag= list(drones_bag.items()))
    with open(f"{route}/simplesim/rviz/mult_config.rviz", "w") as mrviz:
        mrviz.write(rviz_content)

    perimeter_content = render_template('files/perimeter.yaml', point_list=perimeter_points)
    with open(f"{route}/planner/config/perimeter.yaml", "w") as perimc:
        perimc.write(perimeter_content)

    return redirect(url_for("index"))

if __name__ == '__main__':
    if not os.path.exists(f'{route}/simplesim/launch'):
        os.makedirs(f'{route}/simplesim/launch')
    if not os.path.exists(f'{route}/simplesim/config'):
        os.makedirs(f'{route}/simplesim/config')
    if not os.path.exists(f'{route}/simplesim/rviz'):
        os.makedirs(f'{route}/simplesim/rviz')
    if not os.path.exists(f'{route}/simplesim/waypoints'):
        os.makedirs(f'{route}/simplesim/waypoints')
    if not os.path.exists(f'{route}/planner/config'):
        os.makedirs(f'{route}/planner/config')
    app.run(debug=True)
