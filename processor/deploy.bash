#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
pydoover deploy_config ../doover_config.json --agent 0f7ec471-5509-4bc6-bd4a-00c058bf51e9 --profile prod