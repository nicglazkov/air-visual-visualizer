import json
from flask import Flask
from flask import Response
from flask import send_file
from io import BytesIO
from smb.SMBConnection import SMBConnection


hostName = "localhost"
serverPort = 8080

client_machine_name = 'localhost'
server_name = 'AirVisual'
domain_name = ''

app = Flask(__name__)

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

userID = data["userID"]
password = data["password"]
server_ip = data["server_ip"]
password_2 = data["password_2"]
server_ip_2 = data["server_ip_2"]


@app.route("/")
def index():

    return send_file("index.html")


def get_json(server_ip, password):
    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                         is_direct_tcp=True)

    conn.connect(server_ip, 445)

    temp_file = BytesIO()

    conn.retrieveFile(
        'airvisual', 'latest_config_measurements.json', temp_file)

    json = temp_file.getvalue()

    conn.close()

    return Response(json, mimetype="application/json; charset=UTF-8")


@app.route("/data/airvisual_office.json")
def get_office_json():

    return get_json(server_ip, password)


@app.route("/data/airvisual_kitchen.json")
def get_kitchen_json():

    return get_json(server_ip_2, password_2)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
