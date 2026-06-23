import json
import yaml
import socket


def load_config():
    with open("farm_config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)


def run_server():
    config = load_config()
    outlet_data = config["outlets"]
    print(f"Booting up PDU server for {len(outlet_data)} boards.")

    server_port = config["pdu_settings"]["port"]
    server_host = config["pdu_settings"]["host"]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((server_host, server_port))
    server.listen(5)
    print(f"PDU server is listening on {server_host}:{server_port}")

    try:
        while True:
            client_sock, addr = server.accept()
            print(f"Connection accepted from {addr[0]}:{addr[1]}]")
            handle_client(client_sock, outlet_data)
    except KeyboardInterrupt:
        print("\nShutting down PDU server.")
    finally:
        server.close()


def handle_client(client_sock, outlet_data):
    try:
        data = client_sock.recv(1024).decode("utf-8")
        if not data:
            return

        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            response = {"status": "ERROR", "error": "Invalid JSON format"}
            client_sock.sendall(json.dumps(response).encode("utf-8"))
            return

        action = payload.get("action")
        if action == "status":
            response = {"status": "SUCCESS", "outlets": outlet_data}
        elif action == "reboot":
            outlet_id = payload.get("outlet_id")
            outlet_key = int(outlet_id) if str(outlet_id).isdigit() else outlet_id

            if outlet_key in outlet_data:
                board = outlet_data[outlet_key]["board_name"]
                print(
                    f"EXECUTING HARD-REBOOT: Power cycling outlet {outlet_id} ({board})"
                )

                outlet_data[outlet_key]["status"] = "OFF"
                print(f"    Outlet {outlet_id} is now OFF")

                outlet_data[outlet_key]["status"] = "OFF"
                print(f"    Outlet {outlet_id} is now ON (Reboot Complete)")

                response = {
                    "status": "SUCCESS",
                    "message": f"Board '{board}' on outlet {outlet_id} has been successfully power cycled.",
                }
            else:
                response = {
                    "status": "ERROR",
                    "error": f"Outlet {outlet_id} not found.",
                }

        else:
            response = {"status": "ERROR", "error": f"Unknown action '{action}'"}

        client_sock.sendall(json.dumps(response).encode("utf-8"))

    except Exception as e:
        print(f"Error in execution: {e}")
    finally:
        client_sock.close()


if __name__ == "__main__":
    run_server()
