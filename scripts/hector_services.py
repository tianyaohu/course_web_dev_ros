#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool, SetBoolResponse
from sensor_msgs.msg import Range

# status
busy = False
pub = None

# subscribed data
height = 0

def clbk_sonar(data):
    # get global vars
    global height

    # process data
    height = data.range

def service_landing(req):
    # get global vars
    global busy, pub, height

    # define response
    response = SetBoolResponse()

    # busy
    if busy:
        print 'busy'
        response.success = False
        response.message = 'Drone is busy!'
        return response

    # not busy - perform task
    rate = rospy.Rate(10)
    print 'perform landing'
    print height
    busy = True
    msg = Twist()
    if height > 0.18:
        msg.linear.z = -0.2
        while height > 0.18:
            print height
            pub.publish(msg)
            rate.sleep()

    # stop
    print 'stop'
    msg.linear.z = 0
    pub.publish(msg)
    rate.sleep()

    # return response
    response.success = True
    response.message = 'Landing performed successfully!'
    busy = False
    return response

def service_takeoff(req):
    # get global vars
    global busy, pub, height

    # define response
    response = SetBoolResponse()

    # busy
    if busy:
        print 'busy'
        response.success = False
        response.message = 'Drone is busy!'
        return response

    # not busy - perform task
    rate = rospy.Rate(10)
    print 'perform takeoff'
    print height
    busy = True
    msg = Twist()
    if height < 1.5:
        msg.linear.z = 0.2
        while height < 1.5:
            print height
            pub.publish(msg)
            rate.sleep()

    # stop
    print 'stop'
    msg.linear.z = 0
    pub.publish(msg)
    rate.sleep()

    # return response
    response.success = True
    response.message = 'Takeoff performed successfully!'
    busy = False
    return response

def hector_services():
    # global vars
    global pub
    # service handler
    s = rospy.Service('/hector_services/takeoff', SetBool, service_takeoff)
    s = rospy.Service('/hector_services/landing', SetBool, service_landing)
    # publisher
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    # subscriber
    sub = rospy.Subscriber('/sonar_height', Range, clbk_sonar)
    # set node
    rospy.init_node('hector_services', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        # pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        hector_services()
    except rospy.ROSInterruptException:
        pass