

import cv2
#from track_bar2 import track_bar2

class data_saver:

    def __init__(self):
        self.init_white_1 = 260
        self.init_white_2 = 230
        self.init_yellow_1 = 70
        self.init_yellow_2 = 100
        self.prev_white_x1 = 0
        self.prev_white_x2 = 0
        self.prev_yellow_x1 = 0
        self.prev_yellow_x2 = 0
        self.cam_start = 1
        self.forward_stats = None
        self.forward_white_1 = 250
        self.forward_white_2 = 230
        self.forward_yellow_1 = 50
        self.forward_yellow_2 = 80
        self.park = 0
        self.count_on = 0
        self.count = 0
        self.traffic_meet = 0
        self.red_detect = 0
        self.traffic_detect_off = 0





    def get_frame_roi_edge(self,roi_gray):

        Threshold1 = 150
        Threshold2 = 200
        FilterSize = 10

        self.edge = cv2.Canny(roi_gray, Threshold1, Threshold2, FilterSize)


    def traffic_light(self,cap,T_R,T_G,hsv_roi):


        if self.traffic_meet == 1 and self.red_detect == 1 and self.traffic_detect_off == 0:

            while cap.isOpened():
                print ("stopped")

                ret11, frame11 = cap.read()
                hsv1 = cv2.cvtColor(frame11, cv2.COLOR_BGR2HSV)
                roi1_trafic = hsv1[50:240, 160:320]
                T_R.get_mask(roi1_trafic)

                if T_R.detect_check is False :
                    print("red_ off")
                    self.traffic_detect_off = 1
                    break


        if self.traffic_meet is 0:
            T_G.get_mask(hsv_roi)
            if T_G.detect_check is True:
                print("detect_green")
                self.traffic_meet = 1


        if self.traffic_meet is 1 and self.red_detect is 0:
            T_R.get_mask(hsv_roi)
            if T_R.detect_check is True:
                self.red_detect = 1
                print ("detect_red")
