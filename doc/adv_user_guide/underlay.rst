How to bootstrap ROS from source
================================

.. highlight:: catkin-sh

This page explains the preferred way to create a catkin and ROS underlay.
An underlay is a build from source (with an optional installation) of
catkin and the base ROS packages.  It has to be manually updated and
maintained, but enables to modify these packages.

This is required for systems where the Debian packages cannot be
installed (e.g. Windows, MacOS), or for developers of the base ROS
packages.

Install CMake and ROS bootstrap tools::

   $ sudo apt-get install cmake python-catkin-pkg python-rosdep python-rosinstall

Pick a temp directory::

   $ cd `mktemp -d`

Get the rosinstall file::

   $ wget https://raw.github.com/ros/catkin/master/rosinstalls/base.rosinstall

.. todo:: get the file from outside catkin

Rosinstall it.  You don't want it built, use ``-n``, like this::

   $ rosinstall --catkin -n src base.rosinstall

  [list of repositories checked out...]

   rosinstall update complete.

``--catkin`` suppresses the generation of setup.bash/sh files.  Catkin will generate them for you later.

*Remove the generated file ``src/CMakeLists.txt`` which was generated by rosinstall*::

   $ rm src/CMakeLists.txt

.. todo:: rosinstall should be modified to not generate that file or better create the correct symlink directly.

*Instead of using rosinstall you could also checkout the repositories manually.*

Then you need a toplevel ``CMakeLists.txt`` for the workspace::

   $ src/catkin/bin/catkin_init_workspace src

If catkin is already installed and not part of the workspace you just omit the path to the script.

That script creates a symlink to ``catkin/cmake/toplevel.cmake`` using the command ``ln -s catkin/cmake/toplevel.cmake src/CMakeLists.txt``.

The ``src`` folder should now contain all checked out repositories and a CMakeLists.txt::

   $ ls src
   actionlib/  catkin/  CMakeLists.txt  common_msgs/  gencpp/  genlisp/  genmsg/  genpy/  langs/  langs-dev/  ros/  ros_comm/  roscpp_core/  rospack/  ros_tutorials/  std_msgs/

Now do the typical CMake thing::

   $ mkdir build
   $ cd build
   $ cmake ../src
   -- The C compiler identification is GNU
   -- The CXX compiler identification is GNU

   ...

   -- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   -- ~~  traversing projects in topological order:

   ...

   -- Configuring done
   -- Generating done
   -- Build files have been written to: /tmp/tmp.XXX/build

If you want to install the workspace later you should pass the additional argument ``-DCMAKE_INSTALL_PATH=/path/to/install`` when invoking CMake.

And make (preferably with multiple threads)::

   $ make -j4
   Scanning dependencies of target ...
   [  0%] Building CXX object ...

   ...

   [100%] Built target ...

Build and run unit tests
------------------------

To build all unit tests call::

   $ make tests

To run all unit tests call::

   $ make run_tests

Press tab at the end of the command-line to see additional targets for groups of tests and individual tests.

To get a summary of the test results call::

   $ buildspace/bin/catkin_test_results

Again, if catkin is already installed and not part of the workspace you just omit the path to the script.

Setup environment to run anything
---------------------------------

In order to setup the environment that you can run arbitrary code from the workspace the ``setup.bash/*`` must be sourced::

   $ source buildspace/setup.bash

   or

   $ source /path/to/install/setup.bash

After that the core ROS binaries are on the PATH and you can use rosrun/roslaunch to start arbitrary programs.
The setup script does a best effort to provide you with a clean environment and tries to unset everything catkin-related (which has been set by a previous invocation of any setup script) before adding its own paths.

Chain workspaces
----------------

After one workspace has been built (and optionally installed) you can create another workspace on-top of the first one.
Therefore first setup the environment by sourcing the appropriate ``setup.bash``.
Thereby the ``setup.bash`` can be both from either a *buildspace* or an *installspace*.

Then create a second workspace the same way as the first one.
Catkin will automatically use the workspaces already referenced in the environment (in the ``CMAKE_PREFIX_PATH`` variable) as *parent* workspaces for the new one to look up dependencies.
