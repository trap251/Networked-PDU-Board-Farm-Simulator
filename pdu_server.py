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

    server_port = config["pdu_settigs"]["port"]
    server_host = config["pdu_settigs"]["host"]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((server_host, server_port))
    server.listen(5)
    print(f"PDU server is listening on {server_host}:{server_port}")

    try:
        while True:
            client_sock, addr = server.accept()
            print(f"Connection accepted from {addr[0]}:{addr[1]}]")
            handle_client(client_sock)
    except KeyboardInterrupt:
        print("\nShutting down PDU server.")
    finally:
        server.close()


def handle_client(client_sock):
    try:
        data = client_sock.recv(1024).decode("utf-8")
        if not data:
            return

        print(f"[RAW RECEIVE]: {data.strip()}")
        response = {"status": "connected", "message": "PDU ready"}
        client_sock.sendall(json.dumps(response).encode("utf-8"))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_sock.close()


if __name__ == "__main__":
    run_server()
