#!/usr/bin/env bash
TAS_ALLURE_RESULTS_PATH=/home/travis/build/cariel27/pytest_example/allure_results/
ALLURE_RESULTS_REPO=/home/travis/build/cariel27/allure_results/results

if test -f "/home/travis/build/cariel27/pytest_example/allure_results/*.json"; then
    cp -r "$TAS_ALLURE_RESULTS_PATH"/* "$ALLURE_RESULTS_REPO"
    cd /home/travis/build/cariel27/allure_results/
    git add .
    git commit -m "updating allure results"
    git push 'https://cariel27:P4ssw0rd!11@github.com/cariel27/allure_results.git/' master
fi