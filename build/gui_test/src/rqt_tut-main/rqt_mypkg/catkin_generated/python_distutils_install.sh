#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/jetchair/Desktop/be/src/gui_test/src/rqt_tut-main/rqt_mypkg"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/jetchair/Desktop/be/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/jetchair/Desktop/be/install/lib/python2.7/dist-packages:/home/jetchair/Desktop/be/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/jetchair/Desktop/be/build" \
    "/usr/bin/python2" \
    "/home/jetchair/Desktop/be/src/gui_test/src/rqt_tut-main/rqt_mypkg/setup.py" \
     \
    build --build-base "/home/jetchair/Desktop/be/build/gui_test/src/rqt_tut-main/rqt_mypkg" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/jetchair/Desktop/be/install" --install-scripts="/home/jetchair/Desktop/be/install/bin"
