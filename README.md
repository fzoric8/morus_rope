# Gazebo ROS Demos

* Author: Filip Zoric <fzoric8@gmail.com>
* License: 

In order to initialize rope with wanted paramaters it's necessary to enter following commands:
```cd myrobot_description```
Inside that folder there is a scripts folder which contains XML_creator.py and myrobot1.xacro.
In order to create rope one must run following commands:
```$ cd scripts```
```$ python XML_creator.py```
After entering wanted paramaters it generates xacro macro myrobot1.xacro which is used in launch file
Launch file is located at myrobot_gazebo/launch and it's called myrobot1.launch
If you want to launch generated rope one must run commands as follows:
```$ roscore &```
```$ roslaunch myrobot_gazebo myrobot1.launch```
** This creates myrobt1.xacro with base initialized, it's necessary to remove base manually
and configure base link on wanted coordinates


