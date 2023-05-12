import rospy
import numpy as np
import cv2
import time

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

red_lower = (0, 0, 100)
red_upper = (100, 100, 255)
blue_lower = (100, 0, 0)
blue_upper = (255, 200, 200)
green_lower = (0, 100, 0)
green_upper = (100, 255, 100)
yellow_lower = (0, 100, 100)
yellow_upper = (100, 255, 255)


class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count = 0

    def callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            msg = Header()
            msg = data.header
            msg.frame_id = '+1'  # default: STOp      
            cv2.imshow('Image', image)
            
            
            red_mask = cv2.inRange(image, red_lower, red_upper)
            blue_mask = cv2.inRange(image, blue_lower, blue_upper)
            yellow_mask = cv2.inRange(image, yellow_lower, yellow_upper)
            green_mask = cv2.inRange(image, green_lower, green_upper)
            
            red_pixels = cv2.countNonZero(red_mask)
            blue_pixels = cv2.countNonZero(blue_mask)
            yellow_pixels = cv2.countNonZero(yellow_mask)
            green_pixels = cv2.countNonZero(green_mask)
            
            #print(red_pixels, blue_pixels, yellow_mask, green_mask)
            
            if ((red_pixels>=blue_pixels)&(red_pixels>=green_pixels)&(red_pixels>=yellow_pixels)):
            	#print("red!")
            	msg.frame_id = '-1'
            	#print(msg.frame_id)
            elif((blue_pixels>=red_pixels)&(blue_pixels>=green_pixels)&(blue_pixels>=yellow_pixels)):
            	#print("blue!")
            	msg.frame_id = '1'
            	#print(msg.frame_id)
            else: 
            	#print("unknown!")
            	msg.frame_id = '0'
            	#print(msg.frame_id)
            cv2.waitKey(1)
            self.color_pub.publish(msg)
            
        except CvBridgeError as e:
        	print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    detector = DetermineColor()
    rospy.init_node('CompressedImages1', anonymous=False)
    rospy.spin()
