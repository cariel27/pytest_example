#!/usr/bin/env bash
ALLURE_REPO_JENKINS_SCRIPT=/home/travis/build/cariel27/allure_results/jenkins_script

cd "$ALLURE_REPO_JENKINS_SCRIPT"
> jenkins_set_build_number.sh
echo "set BUILD_NUMBER="$TRAVIS_BUILD_NUMBER >> jenkins_set_build_number.sh
chmod +x jenkins_set_build_number.sh
git add jenkins_set_build_number.sh
git commit -m "Creating jenkins_set_build_number.sh"
git push 'https://cariel27:P4ssw0rd!11@github.com/cariel27/allure_results.git/' master