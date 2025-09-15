execute_process(COMMAND "/home/jetchair/Desktop/be/build/gui_test/src/rqt_tut-main/rqt_mypkg/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/jetchair/Desktop/be/build/gui_test/src/rqt_tut-main/rqt_mypkg/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
