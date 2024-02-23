#!/bin/bash
source ./.venv/bin/activate
if $(pyinstaller piggybot.spec); then
    echo "Build success"
else
    echo "Build failed"
    exit 1
fi

scp dist/piggybot zhouxinliang@192.168.1.115:.