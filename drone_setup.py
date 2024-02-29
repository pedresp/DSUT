from flask import Flask, render_template, request, redirect, url_for
import classes as c
import utils

drones_bag = {}

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", drones_bag=drones_bag, next_drone=utils.next_drone(drones_bag))

@app.route("/add_drone", methods=['POST'])
def basic_add_drone():
    my_data = request.form.to_dict()

    drone_id = my_data["drone_id"]
    drone_speed = float(my_data["drone_speed"])
    drone_acc = float(my_data["drone_acc"])

    drones_bag[drone_id] = c.Drone(drone_id, drone_speed, drone_acc)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)