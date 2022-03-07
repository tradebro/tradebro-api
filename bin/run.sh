#!/usr/bin/env bash

echo 'Environment is: '${ENV}

if test "x${ENV}" = 'xdev'; then
  if test "x${APPNAME}" = "xaccount" ; then
    uvicorn appaccount.web:app --host 0.0.0.0 --port 8080 --log-level debug --reload --reload-dir src
  elif test "x${APPNAME}" = "xtrade" ; then
    uvicorn apptrade.web:app --host 0.0.0.0 --port 8080 --log-level debug --reload --reload-dir src
  else
    echo "invalid value for envvar APPNAME '${APPNAME}'"
    exit 1
  fi
else
  if test "x${APPNAME}" = "xaccount" ; then
    uvicorn appaccount.web:app --host 0.0.0.0 --port 8080 --log-level info
  elif test "x${APPNAME}" = "xtrade" ; then
    uvicorn apptrade.web:app --host 0.0.0.0 --port 8080 --log-level info
  else
    echo "invalid value for envvar APPNAME '${APPNAME}'"
    exit 1
  fi
fi