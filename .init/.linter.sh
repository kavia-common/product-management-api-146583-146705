#!/bin/bash
cd /home/kavia/workspace/code-generation/product-management-api-146583-146705/products_backend_api
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

