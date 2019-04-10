#!/usr/bin/env bash
TAS_PATH=/home/travis/build/cariel27/pytest_example/
TAS_ALLURE_RESULTS_PATH=/home/travis/build/cariel27/pytest_example/allure_results/
ALLURE_RESULTS_REPO=/home/travis/build/cariel27/allure_results/results

git clone --depth=50 --branch=master https://github.com/cariel27/allure_results.git /home/travis/build/cariel27/allure_results

cd "$ALLURE_RESULTS_REPO"
rm *
touch readme.txt
cp -r "$TAS_ALLURE_RESULTS_PATH"/* "$ALLURE_RESULTS_REPO"
git add .
git commit -m "updating allure results"

# Getting Travis Build Number and Generating the script to update Jenkins.
./travis_build_number.sh

git push 'https://cariel27:P4ssw0rd!11@github.com/cariel27/allure_results.git/' master
