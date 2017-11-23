#!/usr/bin/env python

#================================================================================
# PROJECT   : ASSISTED DRIVING BY ARTIFICIAL VISION                             *
#           : (DETECTING LINES ON THE DAY)                                      *
# VERSION   : 1.0                                                               *
# AUTHOR    : Jonas Carrillo Sisalima           jonascs1692@gmail.com           *
# PROFESSOR : Rodrigo Barba                     lrbarba@utpl.edu.ec             *
# COMPANY   : Sic ElectriTelecom  Loja-Ecuador                                  *
# DATE      : 13/07/2015                                                        *
#================================================================================

#Import packages needed
import roslib; roslib.load_manifest('autorace')
import rospy
from std_msgs.msg import Float32
from autorace.msg import forwardVision
import numpy as np
import imutils
import math
import cv2
import time
from track_bar import track_bar
from data_saver import data_saver

def nothing(x):  
	pass


#==================================== default set up ===================================#


tunnel_lower = [0, 0, 205]
tunnel_upper = [180, 255, 255]
tunnel = track_bar('dark', True ,tunnel_lower, tunnel_upper)

white_lower = [40, 0, 140]
white_upper = [100, 255, 255]
white = track_bar('white', False ,white_lower, white_upper)

yellow_lower = [20, 35, 60]
yellow_upper = [40, 255, 255]
yellow = track_bar('yellow',False ,yellow_lower, yellow_upper)

stop_lower = [0, 50, 60]
stop_upper = [10, 255, 255]
stop = track_bar('stop',False ,stop_lower, stop_upper)

side_lower = [20, 0, 200]
side_upper = [80, 255, 255]
side = track_bar('side', False,side_lower, side_upper)

trafic_R_lower = [144, 44, 137]
trafic_R_upper = [170, 129, 170]
trafic_R = track_bar('trafic_R',False,trafic_R_lower, trafic_R_upper)

trafic_Y_lower = [0, 40, 100]
trafic_Y_upper = [20, 255, 255]
trafic_Y = track_bar('trafic_Y',False,trafic_Y_lower, trafic_Y_upper)

trafic_G_lower = [93, 181, 235]
rafic_G_upper = [178, 241, 255]
trafic_G = track_bar('rafic_G',False,trafic_G_lower, rafic_G_upper)

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)
cap.set(3, 320)
cap.set(4, 240)
cap1.set(3, 320)
cap1.set(4, 240)

pub = rospy.Publisher('/forwardVision', forwardVision, queue_size=10)
rospy.init_node('forward_vision')
msg = forwardVision()

dat = data_saver()

#========================================================================================#
while (cap.isOpened() and cap1.isOpened()):

	ret,frame = cap.read()
	ret,frame1 = cap1.read()

#================================ hsv ===================================================#
	hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	cv2.rectangle(frame,(0,275),(600,300),(0,255,0),2)

	roi1 = hsv1[150:240, 0:320]
	roi1_trafic = hsv1[50:240, 160:320]
	roi2 = hsv2[0:240, 160:320]
# =======================================================================================#
# ================================ edge =================================================#

	frame_roi_for_edge = gray[150:240, 0:320]
	dat.get_frame_roi_edge(frame_roi_for_edge)

# =======================================================================================#
# ================================ mask =================================================#
  	white.get_mask(roi1)
  	yellow.get_mask(roi1)
	stop.get_mask(hsv1)
	side.get_mask(roi2)
	tunnel.get_mask(hsv1)

# =======================================================================================#
# ================================ edge =================================================#
	
	white.detect_edge(white.mask)
	yellow.detect_edge(yellow.mask)
	side.detect_edge(side.mask)

	roi_yellow_1=yellow.edge[70:90, 0:320]
	roi_yellow_2=yellow.edge[30:50, 0:320]


	roi_white_1=white.edge[70:90, 0:320]
	roi_white_2=white.edge[30:50, 0:320]

	side_roi_1 = side.edge[50:60, 0:160]
	side_roi_2 = side.edge[120:130, 0:160]
	side_roi_3 = side.edge[230:240, 0:160]

	side.find_cnts_devide_roi(1, side_roi_1)
	side.find_cnts_devide_roi(2, side_roi_2)
	side.find_cnts_devide_roi(3, side_roi_3)

# =======================================================================================#




# ================================ line =================================================#
  	white.get_line(roi_white_1,roi_white_2)
   	yellow.get_line(roi_yellow_1,roi_yellow_2)

  	white.detect_white_line(frame,dat)
  	yellow.detect_yello_line(frame,dat)

# =======================================================================================#
# ================================ stop bar==============================================#

	stop.detect_stop_bar(frame,dat)

# =======================================================================================#
# ================================ park area ============================================#
	side.detect_side_lines(frame1,dat)
	if dat.forward_stats is 4:
		white.park(frame,dat)
	if dat.count is 10:
		msg.forward_stats = 4
		pub.publish(msg)
		dat.park = 1
		dat.count = 0
		dat.count_on = 0
# =======================================================================================#
# ================================ traffic light ========================================#
	dat.traffic_light(cap,trafic_R,trafic_G,roi1_trafic)
# =======================================================================================#

# ================================ tunnel_mode ========================================#
	tunnel.detect_tunnel(dat)
# =======================================================================================#
	
	msg.forward_white_1=dat.forward_white_1
	msg.forward_white_2=dat.forward_white_2
	msg.forward_yellow_1=dat.forward_yellow_1
	msg.forward_yellow_2=dat.forward_yellow_2
	msg.forward_stats = dat.forward_stats


	rospy.loginfo(msg)
	pub.publish(msg)
	cv2.imshow('total video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		msg.forward_stats = 3
		pub.publish(msg)
		break



