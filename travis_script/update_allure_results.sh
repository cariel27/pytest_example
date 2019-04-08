#!/usr/bin/env bash

cp -r /home/travis/build/cariel27/pytest_example/allure_results/* /home/travis/build/cariel27/allure_results/results
cd /home/travis/build/cariel27/allure_results/
git add .
git commit -m "updating allure results"
git push 'https://cariel27:P4ssw0rd!11@github.com/cariel27/allure_results.git/' master