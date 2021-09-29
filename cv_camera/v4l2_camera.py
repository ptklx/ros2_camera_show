import rclpy
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
# from std_msgs.msg import Header

# We will be publishing on vision_msgs
# from vision_msgs.msg import Classification2D, ObjectHypothesis

# Import necessary PyTorch and related frameworks
# import torch
# import torchvision
# from torchvision import models
# from torchvision import transforms
import numpy as np
from timeit import default_timer as timer
import os
import cv2
from cv_bridge import CvBridge, CvBridgeError

def open_cam_usb(dev, width, height):
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ('v4l2src device=/dev/video{} ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)RGB ! '
               'videoconvert ! appsink').format(dev, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


class my_v4l2_talker(Node):
    def __init__(self):
        super().__init__('my_v4l2_talker')
        # Create a subscriber to the Image topic
        self.image_publisher = self.create_publisher(Image, 'image', 10)
        self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        bool=self.cap.isOpened()
        if  not bool:
            self.get_logger().info("open camera fail! ") 

        timer_period = 1.0/30.0   # seconds
        self.tmr = self.create_timer(timer_period,self.talker_callback)
        # Use CV bridge to convert ROS Image to CV_image for visualizing in window
        self.bridge = CvBridge()

    def talker_callback(self):
        
        # img_data = np.asarray(msg.data)
        # img = np.reshape(img_data,(msg.height, msg.width, 3))
        # start = timer()      
              # Use OpenCV to visualize the images being classified from webcam 
        ret,frame=self.cap.read()
        if ret:
            ros_image = self.bridge.cv2_to_imgmsg(frame,"bgr8")
            ros_image.header.frame_id = 'camera_frame'
            self.image_publisher.publish(ros_image)
        
            # try:
            # cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            # except CvBridgeError as e:
            # print(e)


            # cv2.imshow('camera_image', frame)
            # cv2.waitKey(1)
       

def main(args=None):
    rclpy.init(args=args)

    my_node = my_v4l2_talker()
    try:
        rclpy.spin(my_node)
    except KeyboardInterrupt:
        pass
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    my_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()