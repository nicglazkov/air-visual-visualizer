import json
from flask import Flask
from flask import Response
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


@app.route("/")
def get_json():

    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                         is_direct_tcp=True)

    conn.connect(server_ip, 445)

    temp_file = BytesIO()

    conn.retrieveFile(
        'airvisual', 'latest_config_measurements.json', temp_file)

    json = temp_file.getvalue()

    conn.close()

    return Response(json, mimetype="application/json; charset=UTF-8")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
