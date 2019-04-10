#!/usr/bin/env bash
TAS_PATH=/home/travis/build/cariel27/pytest_example/

cd "$TAS_PATH"
> travis_script/jenkins_set_build_number.sh
echo "set BUILD_NUMBER="$TRAVIS_BUILD_NUMBER >> travis_script/jenkins_set_build_number.sh
chmod +x travis_script/jenkins_set_build_number.sh
git add travis_script/jenkins_set_build_number.sh
git commit -m "Creating jenkins_set_build_number.sh"
git push origin master
