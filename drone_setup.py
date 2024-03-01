from flask import Flask, render_template, request, redirect, url_for
import classes as c
import utils

import os
import pwd

drones_bag = {}
ros_ws = 'drone_proy/ros_tfg'
route = f"/home/{pwd.getpwuid(os.getuid()).pw_name}/{ros_ws}/src/simplesim"

print(route)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("webpage/index.html", drones_bag=drones_bag, next_drone=utils.next_drone(drones_bag))

@app.route("/add_drone", methods=['POST'])
def basic_add_drone():
    my_data = request.form.to_dict()

    drone_id = my_data["drone_id"]
    drone_speed = float(my_data["drone_speed"])
    drone_acc = float(my_data["drone_acc"])

    drones_bag[drone_id] = c.Drone(drone_id, drone_speed, drone_acc)
    return redirect(url_for("index"))

@app.route("/action_on_drone", methods=['POST'])
def modify_drone():
    my_data = request.form.to_dict()

    drone_id = my_data["drone_id"]
    drone_speed = float(my_data["drone_speed"])
    drone_acc = float(my_data["drone_acc"])

    if (my_data['aod'] == 'modify_drone'):
        drones_bag[drone_id].speed = drone_speed
        drones_bag[drone_id].acc = drone_acc
    elif (my_data['aod'] == 'remove_drone'):
        del drones_bag[drone_id]
    else:
        new_drone = utils.next_drone(drones_bag)
        drones_bag[new_drone] = c.Drone(new_drone, drone_speed, drone_acc)

    return redirect(url_for("index"))

@app.route("/generate_config", methods=['POST'])
def generate_config():
    for drone_key, drone_value in drones_bag.items():
        content = render_template('files/drone_template.yaml', drone_id=drone_key, drone_speed=drone_value.speed, drone_acc=drone_value.acc)
        print(f"{route}/config/{drone_key}.yaml")
        with open(f"{route}/config/{drone_key}.yaml", 'w', encoding='utf-8') as outf:
            outf.write(content)

    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)