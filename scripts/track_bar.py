
import cv2
import numpy as np
from data_saver import data_saver



def nothing(x):
    pass


class track_bar:

    def __init__(self ,var_name,make_bar, lower, upper):

        self.name = var_name
        self.lower = lower
        self.upper = upper

        self.make_bar = make_bar
        if make_bar is True:

            cv2.namedWindow(self.name)
            cv2.createTrackbar('H_l', self.name, -180, 180, nothing)
            cv2.createTrackbar('H_u', self.name, -180, 180, nothing)
            cv2.createTrackbar('S_l', self.name, 0, 255, nothing)
            cv2.createTrackbar('S_u', self.name, 0, 255, nothing)
            cv2.createTrackbar('V_l', self.name, 0, 255, nothing)
            cv2.createTrackbar('V_u', self.name, 0, 255, nothing)

            cv2.setTrackbarPos('H_l', self.name, self.lower[0])
            cv2.setTrackbarPos('H_u', self.name, self.upper[0])
            cv2.setTrackbarPos('S_l', self.name, self.lower[1])
            cv2.setTrackbarPos('S_u', self.name, self.upper[1])
            cv2.setTrackbarPos('V_l', self.name, self.lower[2])
            cv2.setTrackbarPos('V_u', self.name, self.upper[2])



    def get_track_pos(self):

        if self.make_bar is True :
            self.lower[0] = cv2.getTrackbarPos('H_l', self.name)
            self.upper[0] = cv2.getTrackbarPos('H_u', self.name)
            self.lower[1] = cv2.getTrackbarPos('S_l', self.name)
            self.upper[1] = cv2.getTrackbarPos('S_u', self.name)
            self.lower[2] = cv2.getTrackbarPos('V_l', self.name)
            self.upper[2] = cv2.getTrackbarPos('V_u', self.name)

        self.hsv_l = (self.lower[0] ,self.lower[1] ,self.lower[2])
        self.hsv_u = (self.upper[0] ,self.upper[1] ,self.upper[2])




    def get_mask(self ,roi_frame):

        self.None_detect = roi_frame - roi_frame
        self.get_track_pos()

        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(roi_frame, self.hsv_l, self.hsv_u)
        self.mask = cv2.erode(self.mask, None, iterations=2)
        self.mask = cv2.dilate(self.mask, None, iterations=2)
        self.cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(self.cnts) > 0:
            self.detect_check = True

        else:
            self.mask = self.None_detect
            self.detect_check = False


    def find_cnts_devide_roi(self,num,mask_roi):

        cnts = cv2.findContours(mask_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if num is 1:
            self.cnts_line_1 = cnts
        elif num is 2:
            self.cnts_line_2 = cnts
        elif num is 3:
            self.cnts_line_3 = cnts




    def detect_edge(self,mask):

        Threshold1 = 150
        Threshold2 = 200
        FilterSize = 10

        self.edge = cv2.Canny(mask, Threshold1, Threshold2, FilterSize)



    def get_line(self,roi1,roi2):

        self.line1 = cv2.HoughLinesP(roi1,rho = 1,theta = 1*np.pi/180,threshold = 8,minLineLength = 10,maxLineGap = 50)
        self.line2 = cv2.HoughLinesP(roi2,rho = 1,theta = 1*np.pi/180,threshold = 8,minLineLength = 10,maxLineGap = 50)




    def detect_white_line(self,frame,dat):

        tem_white_1 = []
        tem_white_2 = []
	

        if self.line1 is not None:
            N = self.line1.shape[0]
            #msg.forward_stats = 0
            dat.forward_stats = 0

            for i in range(N):
                x1 = self.line1[i][0][0]
                y1 = self.line1[i][0][1]
                x2 = self.line1[i][0][2]
                y2 = self.line1[i][0][3]
                if dat.cam_start is 1 :
                    tem_white_1.append(dat.init_white_1)
                    		    
                else:
                    if abs(dat.prev_white_x1 - x1) < 50:
                        tem_white_1.append(x1)
               		cv2.line(frame, (x1, y1 + 220), (x2, y2 + 220), (255, 0, 0), 2)
			
            if len(tem_white_1) is 0:
                dat.prev_white_x1 = dat.forward_white_1

            else:
                dat.prev_white_x1 = min(tem_white_1)
            dat.forward_white_1 = dat.prev_white_x1
	

        if self.line2 is not None:
            N = self.line2.shape[0]
            #msg.forward_stats = 0
            dat.forward_stats = 0
            for i in range(N):
                x1 = self.line2[i][0][0]
                y1 = self.line2[i][0][1]
                x2 = self.line2[i][0][2]
                y2 = self.line2[i][0][3]
                
                if dat.cam_start is 1:
                    tem_white_2.append(dat.init_white_2)
		   
                else:
                    if abs(dat.prev_white_x2 - x1) < 50:
                        tem_white_2.append(x1)
			cv2.line(frame, (x1, y1 + 180), (x2, y2+180), (255, 0, 0), 2)

            if len(tem_white_2) is 0:
                dat.prev_white_x2 = dat.forward_white_2

            else:
                dat.prev_white_x2 = min(tem_white_2)
            dat.forward_white_2 = dat.prev_white_x2



    def detect_yello_line(self,frame,dat):

        tem_yellow_1 = []
        tem_yellow_2 = []

        if self.line1 is not None:
            N = self.line1.shape[0]
            dat.forward_stats = 1

            for i in range(N):
                x1 = self.line1[i][0][0]
                y1 = self.line1[i][0][1]
                x2 = self.line1[i][0][2]
                y2 = self.line1[i][0][3]

                if dat.cam_start is 1:
                    tem_yellow_1.append(dat.init_yellow_1)
		else:
    		    if abs(dat.prev_yellow_x1 - x2) < 50:
                        tem_yellow_1.append(x2)
			cv2.line(frame, (x1, y1 + 220), (x2, y2+220), (0, 0, 255), 2)

 	    if len(tem_yellow_1) is 0:
                dat.prev_yellow_x1 = dat.prev_yellow_x1

            else:
                dat.prev_yellow_x1 = max(tem_yellow_1)
            dat.forward_yellow_1 = dat.prev_yellow_x1

            dat.park = 0


        if self.line2 is not None:
            N = self.line2.shape[0]
            dat.forward_stats = 1
            for i in range(N):
                x1 = self.line2[i][0][0]
                y1 = self.line2[i][0][1]
                x2 = self.line2[i][0][2]
                y2 = self.line2[i][0][3]
                if dat.cam_start is 1:
                    tem_yellow_2.append(dat.init_yellow_2)
		    dat.cam_start = 0
		else:
    		    if abs(dat.prev_yellow_x2 - x2) < 50:
                        tem_yellow_2.append(x2)
             		cv2.line(frame, (x1, y1 + 180), (x2, y2 + 180), (0, 0, 255), 2)
 	    if len(tem_yellow_2) is 0:
                dat.prev_yellow_x2 = dat.prev_yellow_x2

            else:
                dat.prev_yellow_x2 = max(tem_yellow_2)
            dat.forward_yellow_2 = dat.prev_yellow_x2

            dat.park = 0                			


        if dat.forward_yellow_2 > dat.forward_white_2:
            dat.forward_stats = 0



    def detect_stop_bar(self,frame,dat):

        red_arr_x = []
        red_arr_w = []
        red_arr_h = []
        red_arr_y = []

        if len(self.cnts) >= 3:
            for cnt in self.cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                red_arr_x.append(x)
                red_arr_w.append(w)
                red_arr_h.append(h)
                red_arr_y.append(y)

            if min(red_arr_x) > 160:
                dat.forward_stats = 2
            for i in range(len(self.cnts)):
                if abs(red_arr_x[i - 1] - red_arr_x[i]) > 25 and red_arr_w[i - 1] >= 25 and red_arr_w[
                            i - 1] >= 20 and abs(red_arr_y[i - 1] - red_arr_y[i]) < 15:
                    dat.forward_stats = 3
                    print("stop bar")
                    cv2.rectangle(frame, (red_arr_x[i - 1], red_arr_y[i - 1]),
                                  (red_arr_x[i - 1] + red_arr_w[i - 1], red_arr_y[i - 1] + red_arr_h[i - 1]),
                                  (0, 255, 0), 2)


    def detect_side_lines(self,frame,dat):

        line_x1 = []
        line_x3 = []

        if len(self.cnts_line_1) > 0:
            for cnt in self.cnts_line_1:
                line_1 = 0
                x, y, w, h = cv2.boundingRect(cnt)
                line_x1.append(x)
                cv2.rectangle(frame, (x + 160, y + 50), (x + 160 + w, y + 50 + h), (0, 255, 0), 2)
        else:
            line_1 = 1

        if len(self.cnts_line_2) > 0:
            for cnt in self.cnts_line_2:
                line_2 = 0
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x + 160, y + 120), (x + 160 + w, y + 120 + h), (0, 255, 0), 2)
        else:
            line_2 = 1

        if len(self.cnts_line_3) > 0:
            for cnt in self.cnts_line_3:
                line_3 = 0
                x, y, w, h = cv2.boundingRect(cnt)
                line_x3.append(x)
                cv2.rectangle(frame, (x + 160, y + 230), (x + 160 + w, y + 230 + h), (0, 255, 0), 2)
        else:
            line_3 = 1

        if line_1 is 0 and line_2 is 1 and line_3 is 0:
            if abs(min(line_x1) - min(line_x3)) < 80:
                dat.count_on = 1

        if dat.count_on is 1:
            dat.count = dat.count + 1




    def park(self,frame,dat):

        white_arr_w = []

        if len(self.cnts) is not 0:
            for cnt in self.cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y + 150), (x + w, y + h + 150), (0, 255, 0), 2)
                white_arr_w.append(w)
        if sum(white_arr_w, 0.0) > 210:
            dat.forward_stats = 6

        else:
            dat.forward_stats = 5
        print(sum(white_arr_w, 0.0))




    def detect_tunnel(self,dat):

        if self.detect_check is False:
            print ("tunnel_mode")

            dat.forward_stats = 7
