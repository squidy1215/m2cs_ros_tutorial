#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, SetPenRequest
from std_srvs.srv import Empty, EmptyRequest
# hint: some imports are missing
from m2_ps4.msg import Ps4Data
old_data = Ps4Data()
k=2.5
def callback(data):
    global old_data,k
    ve=data.hat_ly*k
    an=data.hat_rx*3
    c=Twist()
    c.linear.x = ve
    c.angular.z = an
    pub.publish(c)
    # you should publish the velocity here!
    
    # hint: to detect a button being pressed, you can use the following pseudocode:
    if data.dpad_y==1 and old_data.dpad_y!=1 and k<4:
    	k+=1.0
    elif data.dpad_y==-1 and old_data.dpad_y!=-1 and k>1:
    	k-=1.0
    # if ((data.button is pressed) and (old_data.button not pressed)),
    # then do something...
    
    t = SetPenRequest()
    
    if data.triangle and not old_data.triangle:
    	t.r = 0
    	t.g = 255
    	t.b = 0
    	srv_col(t)
    elif data.circle and not old_data.circle:
    	t.r=255
    	t.g=0
    	t.b=0
    	srv_col(t)
    elif data.square and not old_data.square:
    	t.r=0
    	t.g=0
    	t.b=255
    	srv_col(t)
    elif data.cross and not old_data.cross:
    	t.r=255
    	t.g=0
    	t.b=255
    	srv_col(t)
    if data.ps:
    	srv_emp()
    old_data = data

if __name__ == '__main__':
    rospy.init_node('ps4_controller')
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1) # publisher object goes here... hint: the topic type is Twist
    #sub = "/input/ps4_data" # subscriber object goes here Type: Ps4Data
    rospy.Subscriber("/input/ps4_data", Ps4Data, callback)
    # one service object is needed for each service called!
    srv_col = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
    srv_emp = rospy.ServiceProxy('/clear', Empty)
    ## srv_col = # service client object goes here... hint: the srv type is SetPen
    # fill in the other service client object...
    
    rospy.spin()
