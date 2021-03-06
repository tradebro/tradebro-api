#!/usr/bin/env bash

echo 'Environment is: '${ENV}

if test "x${PORT}" = 'x'; then
  export PORT=8080
fi


if test "x${ENV}" = 'xdev'; then
  if test "x${APPNAME}" = "xbackend" ; then
    uvicorn appbackend.web:app --host 0.0.0.0 --port $PORT --log-level debug --reload --reload-dir src
  elif test "x${APPNAME}" = "xfrontend" ; then
    uvicorn appfrontend.web:app --host 0.0.0.0 --port $PORT --log-level debug --reload --reload-dir src
  else
    echo "invalid value for envvar APPNAME '${APPNAME}'"
    exit 1
  fi
else
  if test "x${APPNAME}" = "xbackend" ; then
    uvicorn appbackend.web:app --host 0.0.0.0 --port $PORT --log-level info
  elif test "x${APPNAME}" = "xfrontend" ; then
    uvicorn appfrontend.web:app --host 0.0.0.0 --port $PORT --log-level info
  else
    echo "invalid value for envvar APPNAME '${APPNAME}'"
    exit 1
  fi
fi