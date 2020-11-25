import cv2 as cv
import socket
import json
import datetime
import data_collection as dc
import ratio_calculation as rc

# Server settings
HOST = '172.20.10.6'  # Raspberry Pi IP-address
PORT = 65432  # Port number

capture = cv.VideoCapture(1)  # Video capture index[1] for Kinect
ret, first = capture.read()  # Read video capture index, ret = true/false boolean

kernel_size = 41

# Reference frames for background subtraction
first_gray = cv.cvtColor(first, cv.COLOR_BGR2GRAY)
first_gray = cv.GaussianBlur(first_gray, (kernel_size, kernel_size), 0)

# height and width of capture frame
height = first_gray.shape[0]
width = first_gray.shape[1]
print(height)
print(width)

# Threshold variables
threshold_level = 45
threshold_max = 255

contour_size = 1300  # Ignore blobs less than this value

distance_pixels = 180  # 1 meter distance in pixels
size_ratio = 2.14  # Number of LEDs corresponding to 1 pixel on camera

# Index positions for LED range
index0_1 = 0
index1_1 = 0

index0_2 = 0
index1_2 = 0

index0_3 = 0
index1_3 = 0

distance0 = rc.RatioCalculation()
distance1 = rc.RatioCalculation()
distance2 = rc.RatioCalculation()

# Creating data collection / hit detection log objects
sheet_index = 0  # Sheet index in Google Sheets

hit_obj0 = dc.DataCollection()
hit0 = hit_obj0.run_once_hit(hit_obj0.hit_count)
time0 = hit_obj0.run_once_time(hit_obj0.time_count)

hit_obj1 = dc.DataCollection()
hit1 = hit_obj1.run_once_hit(hit_obj1.hit_count)
time1 = hit_obj1.run_once_time(hit_obj1.time_count)

hit_obj2 = dc.DataCollection()
hit2 = hit_obj2.run_once_hit(hit_obj2.hit_count)
time2 = hit_obj2.run_once_time(hit_obj2.time_count)

start_time = datetime.datetime.now().replace(microsecond=0)
print(start_time)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to our defined host and port

    while True:
        centers = []

        ret, frame = capture.read()

        # if there is no video capture frame break the loop
        if not ret:
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (kernel_size, kernel_size), 0)

        difference = cv.absdiff(gray, first_gray)

        thresh = cv.threshold(difference, threshold_level, threshold_max, cv.THRESH_BINARY)[1]
        # thresh = cv.adaptiveThreshold(difference, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, -2)

        # Dilate the threshold source(input array), none in output(output array),
        # iterations = number of times dilation are applied
        thresh = cv.dilate(thresh, None, iterations=2)

        (contours, hierarchy) = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv.contourArea(c) < contour_size:
                continue

            (x, y, w, h) = cv.boundingRect(c)

            x_center = x + int(w / 2)
            centers.append(x_center)
            centers.sort()

            # Draw rectangle around shape
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 50, 0), 2)

            # Calculating distance and append to centers list
            if len(centers) == 2:
                y0 = distance0.y(centers[0], centers[1])
                if abs(centers[1] - centers[0]) < distance0.distance(y0):
                    index0_1 = int(centers[0] / size_ratio)
                    index1_1 = int(centers[1] / size_ratio)
                    hit0()
                    time0.has_run = False
                else:
                    index0_1 = 0
                    index1_1 = 0
                    time0()
                    hit0.has_run = False
            elif len(centers) == 3:
                y0 = distance0.y(centers[0], centers[1])
                y1 = distance1.y(centers[1], centers[2])
                if abs(centers[1] - centers[0]) < distance0.distance(y0):
                    index0_1 = int(centers[0] / size_ratio)
                    index1_1 = int(centers[1] / size_ratio)
                    hit0()
                    time0.has_run = False
                else:
                    index0_1 = 0
                    index1_1 = 0
                    time0()
                    hit0.has_run = False
                if abs(centers[2] - centers[1]) < distance1.distance(y1):
                    index0_2 = int(centers[1] / size_ratio)
                    index1_2 = int(centers[2] / size_ratio)
                    hit1()
                    time1.has_run = False
                else:
                    index0_2 = 0
                    index1_2 = 0
                    time1()
                    hit1.has_run = False
            elif len(centers) == 4:
                y0 = distance0.y(centers[0], centers[1])
                y1 = distance1.y(centers[1], centers[2])
                y2 = distance2.y(centers[2], centers[3])
                if abs(centers[1] - centers[0]) <  distance0.distance(y0):
                    index0_1 = int(centers[0] / size_ratio)
                    index1_1 = int(centers[1] / size_ratio)
                    hit0()
                    time0.has_run = False
                else:
                    index0_1 = 0
                    index1_1 = 0
                    time0()
                    hit0.has_run = False
                if abs(centers[2] - centers[1]) < distance1.distance(y1):
                    index0_2 = int(centers[1] / size_ratio)
                    index1_2 = int(centers[2] / size_ratio)
                    hit1()
                    time1.has_run = False
                else:
                    index0_2 = 0
                    index1_2 = 0
                    time1()
                    hit1.has_run = False
                if abs(centers[3] - centers[2]) < distance1.distance(y2):
                    index0_3 = int(centers[2] / size_ratio)
                    index1_3 = int(centers[3] / size_ratio)
                    hit2()
                    time2.has_run = False
                else:
                    index0_3 = 0
                    index1_3 = 0
                    time2()
                    hit2.has_run = False
            else:
                index0_1 = 0
                index1_1 = 0
                index0_2 = 0
                index1_2 = 0
                index0_3 = 0
                index1_3 = 0

        # Show normal video frame and threshold frame
        cv.imshow("frame", frame)
        cv.imshow("thresh", thresh)

        # Send JSON over socket
        data = json.dumps(
            {
                "index0_1": index0_1,
                "index1_1": index1_1,
                "index0_2": index0_2,
                "index1_2": index1_2,
                "index0_3": index0_3,
                "index1_3": index1_3,
            }
        )
        s.send(data.encode())

        # Stops program when 'q' is pressed
        key = cv.waitKey(1) & 0xFF

        if key == ord('q'):
            end_time = datetime.datetime.now().replace(microsecond=0)
            print(end_time)

            dc.calculate_time(start_time, end_time)
            #              sheet_index, placement, time_end_list, time_start_list, time_taken_list, hit_count_list
            dc.create_data(sheet_index, 0, hit_obj0.time_end_list, hit_obj0.time_start_list, hit_obj0.time_taken_list,
                           hit_obj0.hit_count_list)
            dc.create_data(sheet_index, 6, hit_obj1.time_end_list, hit_obj1.time_start_list, hit_obj1.time_taken_list,
                           hit_obj1.hit_count_list)
            dc.create_data(sheet_index, 12, hit_obj2.time_end_list, hit_obj2.time_start_list, hit_obj2.time_taken_list,
                           hit_obj2.hit_count_list)
            break

capture.release()
cv.destroyAllWindows()
