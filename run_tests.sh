#!/bin/bash
TEST_DIR="$( cd "$( dirname "$0" )" && pwd )"
python -m unittest discover ${TEST_DIR}