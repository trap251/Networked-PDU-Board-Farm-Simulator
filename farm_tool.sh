#!/usr/bin/env bash

SERVER_HOST="127.0.0.1"
SERVER_PORT=8000

log_msg() {
    echo -e "[\e[1;34mFARM-AUTOMATION\e[0m] $1"
}

case "$1" in
--cleanup)
    log_msg "Starting workplace directory cleanup."

    mkdir -p test_logs/
    rm -rf test_logs/*.log
    touch test_logs/.gitkeep
    log_msg "Dynamic logs directory has been cleared. Ready for a clean test run now."
    ;;

--status)
    log_msg "Requesting board farm infrastructure status."
    payload='{"action": "status"}'
    echo "$payload" | nc $SERVER_HOST $SERVER_PORT
    echo ""
    ;;

--reboot)
    if [ -z "$2" ]; then
        echo "Usage: $0 --reboot <outlet_id>"
        exit 1
    fi
    log_msg "Issuing a remote hard reboot sequence to outlet $2."
    payload="{\"action\": \"reboot\", \"outlet_id\": $2}"
    echo "$payload" | nc $SERVER_HOST $SERVER_PORT
    echo ""
    ;;

*)
    echo "Board Farm Automation Utility"
    echo "Usage: $0 {--cleanup|--status|--reboot <id>}"
    exit 1
    ;;
esac
