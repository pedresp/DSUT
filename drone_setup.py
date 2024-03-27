from flask import Flask, render_template, request, redirect, url_for
import classes as c
import utils

import os
import pwd

drones_bag = {}
fly_height = 8.0
ros_ws = 'drone_proy/ros_tfg'
route = f"/home/{pwd.getpwuid(os.getuid()).pw_name}/{ros_ws}/src/simplesim"

print(route)

app = Flask(__name__)

'''Method to represent the actual state of the drones bag'''
@app.route("/", methods=['GET'])
def index():
    return render_template("webpage/index.html", drones_bag=drones_bag, next_drone=utils.next_drone(drones_bag), fly_height=fly_height)

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

'''Method to generate the configuration and launcher files that are
described in the web page'''
@app.route("/generate_config", methods=['POST'])
def generate_config():
    for drone_key, drone_value in drones_bag.items():
        content = render_template('files/drone_template.yaml', drone_id=drone_key, drone_speed=drone_value.speed, drone_acc=drone_value.acc, \
                                  drone_tof=drone_value.tof, drone_sweep_width=drone_value.sweep_width, drone_coordx=drone_value.coordx, \
                                  drone_coordy= drone_value.coordy)
        print(f"{route}/waypoints/{drone_key}.yaml")
        with open(f"{route}/waypoints/{drone_key}.yaml", 'w', encoding='utf-8') as outf:
            outf.write(content)
        conf_content = render_template('files/drone_template_config.yaml', drone_id=drone_key, drone_speed=drone_value.speed, drone_acc=drone_value.acc, \
                                  drone_tof=drone_value.tof, drone_sweep_width=drone_value.sweep_width, drone_coordx=drone_value.coordx, \
                                  drone_coordy= drone_value.coordy)
        with open(f"{route}/config/{drone_key}.yaml", "w", encoding='utf-8') as coutf:
            coutf.write(conf_content)
    
    minus1_list = list(drones_bag.items())[1:]
    element = list(drones_bag.items())[0][0]
    launch_content = render_template('files/launcher_template.txt', drones_bag=minus1_list, last_drone=element, drones_number= float(len(drones_bag)), \
                                     height=fly_height)
    with open(f"{route}/launch/my_launcher_drones.launch.py", 'w', encoding='utf-8') as launch_config:
        launch_config.write(launch_content)

    rviz_content = render_template('files/rviz.yaml', drones_bag= list(drones_bag.items()))
    with open(f"{route}/rviz/mult_config.rviz", "w") as mrviz:
        mrviz.write(rviz_content)

    return redirect(url_for("index"))

if __name__ == '__main__':
    if not os.path.exists(f'{route}/launch'):
        os.makedirs(f'{route}/launch')
    if not os.path.exists(f'{route}/config'):
        os.makedirs(f'{route}/config')
    if not os.path.exists(f'{route}/rviz'):
        os.makedirs(f'{route}/rviz')
    if not os.path.exists(f'{route}/waypoints'):
        os.makedirs(f'{route}/waypoints')
    app.run(debug=True)
