#!/bin/bash
cd /home/kavia/workspace/code-generation/home-buying-guide-platform-47241-47271/interactive_home_buying_guide_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

