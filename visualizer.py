from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from smb.SMBConnection import SMBConnection

hostName = "localhost"
serverPort = 8080

userID = 'airvisual'
password = ''
client_machine_name = 'localhost'

server_name = 'AirVisual'
server_ip = ''

domain_name = ''


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=UTF-8")
        self.end_headers()

        conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                             is_direct_tcp=True)

        conn.connect(server_ip, 445)

        temp_file = BytesIO()

        conn.retrieveFile(
            'airvisual', 'latest_config_measurements.json', temp_file)

        self.wfile.write(temp_file.getvalue())

        conn.close()


if __name__ == "__main__":

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
