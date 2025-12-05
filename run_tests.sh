#!/bin/bash

python3 -m unittest test.test_construct_vector -v
echo "----------------------------------------"
python3 -m unittest test.test_backend_server_local -v