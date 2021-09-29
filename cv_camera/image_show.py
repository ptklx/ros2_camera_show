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

class my_cv_Listener(Node):
    def __init__(self):
        super().__init__('my_cv_Listener')
        # Create a subscriber to the Image topic
        self.image_subscriber = self.create_subscription(Image, 'image', self.listener_callback, 10)
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        
        # img_data = np.asarray(msg.data)
        # img = np.reshape(img_data,(msg.height, msg.width, 3))
        # start = timer()      
              # Use OpenCV to visualize the images being classified from webcam 
        try:
           cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
           cv2.imshow('image_window', cv_image)
           cv2.waitKey(1)
        except CvBridgeError as e:
          print(e)
        
       

def main(args=None):
    rclpy.init(args=args)

    my_node = my_cv_Listener()
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