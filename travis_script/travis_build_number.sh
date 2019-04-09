#!/usr/bin/env bash
touch travis_script/jenkins_set_build_number.sh
echo "set BUILD_NUMBER="$TRAVIS_BUILD_NUMBER >> travis_script/jenkins_set_build_number.sh
chmod +x travis_script/jenkins_set_build_number.sh