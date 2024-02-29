from flask import Flask, render_template, request, redirect, url_for
import classes as c

drones_bag = {}

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", drones_bag=drones_bag)

@app.route("/add_drone", methods=['POST'])
def basic_add_drone():
    my_data = request.form.to_dict()

    drone_id = my_data["drone_id"]
    drone_speed = float(my_data["drone_speed"])
    drone_acc = float(my_data["drone_acc"])

    print(type(drone_id), type(drone_speed), type(drone_acc))

    drones_bag[drone_id] = c.Drone(drone_id, drone_speed, drone_acc)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)