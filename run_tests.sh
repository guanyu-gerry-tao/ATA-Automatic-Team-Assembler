#!/bin/bash
# Run all test suites for the project

set -e

# Run vector construction and team matching tests
python3 -m unittest test.test_construct_vector -v

# Run backend API server tests
python3 -m unittest test.test_backend_server_local -v