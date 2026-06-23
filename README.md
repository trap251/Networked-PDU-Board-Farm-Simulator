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
