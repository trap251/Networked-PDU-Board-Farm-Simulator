# Networked-PDU-Board-Farm-Simulator
A lightweight, native client-server framework built to simulate a networked Power Distribution Unit (PDU) for remote hardware board farm management. This platform allows automated testing infrastructures (like CI/CD runners) to query target statuses and execute automated hard-reboot sequences on embedded deployment nodes over custom TCP network layers.

## System Architecture

This project maps standard embedded test farm infrastructure patterns:
* **Infrastructure Configuration:** Dynamic mapping of target physical boards, hardware architectures, and power outlet assignments using structured `YAML`.
* **Network Control Layer:** Native execution of asynchronous control sequences via a multi-connection `Python` TCP socket server.
* **Control Payloads:** Structured machine-to-machine messaging using serialization via `JSON`.
* **Environment Automation:** Native `Bash` script wrappers to manage runtime spaces, clean localized debug artifacts, pipeline client requests via `netcat`.


---

## Technical Specifications & Codebase Layout

```text
├── farm_config.yaml    # Infrastructure configration registry (Outlets & Targets)
├──pdu_server.py        # Main TCP Network listener & state machine processor
├── farm_tool.sh        # Environment automation script and network client frontend
├── README.md           # Documentation
```

## Support API Actions (JSON Format)
- Get Infrastructure Status:
{ "action: "status" }
- Trigger Power Cycle (Hard Reboot):
{ "action": "reboot", "outlet_id": 2 }

## Quickstart
### Prerequisites
- Linux environment (Ubuntu, Arch, WSL2, etc.)
- Python 3.x with PyYAML installed:
```text
pip install pyyaml
```
- Netcat (nc) tool installed for network automation piplines.
#### 1. Launch the Network PDU Server
Initialize he listener on the aster farm management machine;
```text
python pdu_server.py
```
#### 2. Run the Automation Utility
Open a separate terminal shell to interact with the running server infrastructure using the automation suite:
- Query all monitored boards:
```text
./farm_tool.sh --status
```
- Execute remote hard powercycle sequence:
```text
./farm_tool.sh --reboot 2
```
- Perform workspace directory environment cleanup:
```text
./farm_tool.sh --cleanup
```
## Professional Highlights Mapped to Embedded Roles
This simulation platform explicitly demonstrates key concepts found in professional hardware regression test labs:
1. Network Relay Emulation: Handles nework sockes to simulate remote terminal interfaces (Telnet/SSH equivalents).
2. Configuration vs Code Separation: Modifying hardware states directly through configuration descriptors (YAML), mirroring production board farm architectures.
3. Automated Error Handling: Safe handling of corrupt serialization matrices and invalid configuration parameters without crashing critical hardware pipelines.
