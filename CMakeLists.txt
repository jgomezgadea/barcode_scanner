cmake_minimum_required(VERSION 2.8.3)
project(robotnik_barcode_scanner)

find_package(catkin REQUIRED COMPONENTS
    roscpp
    rospy
    std_msgs
)

catkin_package(
    CATKIN_DEPENDS
    message_runtime
    std_msgs
)