#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyproj
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped

MARKERS_MAX =1000000
EPSG4612 = pyproj.Proj("+init=EPSG:4612")
EPSG2451 = pyproj.Proj("+init=EPSG:2451")
ini_lat = rospy.get_param("/gnss_ini_lat")
ini_lon = rospy.get_param("/gnss_ini_lon")

ini_y,ini_x = pyproj.transform(EPSG4612, EPSG2451, ini_lon,ini_lat)
pub_msg = PoseWithCovarianceStamped()
pub_msg.header.frame_id = "/gnss"
pub_msg.pose.pose.position.x = ini_x
pub_msg.pose.pose.position.y = ini_y

def main():
    rospy.init_node('gnss_latlon_to_xy', anonymous=True)
    pub = rospy.Publisher("gnss_ini_xy",PoseWithCovarianceStamped,queue_size=10000)

    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        pub_msg.header.stamp = rospy.Time.now();
        pub.publish(pub_msg)
        r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass
