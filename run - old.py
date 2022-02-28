import cv2
from src.hand_tracker import HandTracker
from src.dyn_gesture import Gesture

from timeit import default_timer as timer


WINDOW = "Hand Tracking"
PALM_MODEL_PATH = "models/palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "models/hand_landmark.tflite"
ANCHORS_PATH = "models/anchors.csv"
MULTIHAND = True
HULL = True
POINT_COLOR = (0, 255, 0)
CONNECTION_COLOR = (255, 0, 0)
HULL_COLOR = (0, 0, 255)
THICKNESS = 2
HULL_THICKNESS = 2

POINT_COLOR = (0, 255, 0)
CONNECTION_COLOR = (30, 50, 255)
THICKNESS = 4

start = timer()


def drawpointstoframe(points, frame):
    if points is not None:

        action.update_points(points)
        rotate = action.get_gesture()



        if rotate == True:
            image_flip = cv2.flip(image, 1)
            points, _ = detector(image_flip)


        if action.write is not None:
            cv2.putText(frame,action.write,(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        for point in points:
            x, y = point
            cv2.circle(frame, (int(x), int(y)), THICKNESS * 2, POINT_COLOR, HULL_THICKNESS)
        for connection in connections:
            try:
                x0, y0 = points[connection[0]]
                x1, y1 = points[connection[1]]
            except TypeError:
                print("Error Exception - this error shows after no hand is seen in Przypadek4")
            cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), CONNECTION_COLOR, THICKNESS)
        if HULL:
            for hull_connection in hull_connections:
                x0, y0 = points[hull_connection[0]]
                x1, y1 = points[hull_connection[1]]
                cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), HULL_COLOR, HULL_THICKNESS)



cv2.namedWindow(WINDOW)
#capture = cv2.VideoCapture(0)


# capture.set(cv2.CAP_PROP_FOURCC, *'MJPG')
# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
# capture.set(cv2.CAP_PROP_FPS,60)

def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

def setfourccmjpg(cap):
    oldfourcc = decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    res=cap.set(cv2.CAP_PROP_FOURCC,codec)
    if res:
        print("codec in ",decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC)))
    else:
        print("error, codec in ",decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC)))
    return decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
capture = cv2.VideoCapture(0)
codec = setfourccmjpg(capture)
w=800
h=450
fps=60
res1=capture.set(cv2.CAP_PROP_FRAME_WIDTH,w)
res2=capture.set(cv2.CAP_PROP_FRAME_HEIGHT,h)
res3=capture.set(cv2.CAP_PROP_FPS,fps)
print('is_codec_ok: ', res3)

if capture.isOpened():
    hasFrame, frame = capture.read()
else:
    hasFrame = False

#        8   12  16  20
#        |   |   |   |
#        7   11  15  19
#    4   |   |   |   |
#    |   6   10  14  18
#    3   |   |   |   |
#    |   5---9---13--17
#    2    \         /
#     \    \       /
#      1    \     /
#       \    \   /
#        ------0-
#thumb_tip = 4
#index_tip = 8
#middle_typ = 12
#ring_tip = 16
#pinky_tip = 20
#base_tip = 0



connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (5, 6), (6, 7), (7, 8),
    (9, 10), (10, 11), (11, 12),
    (13, 14), (14, 15), (15, 16),
    (17, 18), (18, 19), (19, 20),
    (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)
]
pseudo_hull_connections = [(0, 17), (17, 18), (18, 19), (19, 20), (0, 1), (1, 2), (2, 3), (3, 4)]
hull_connections = [(4, 8), (8, 12), (12, 16), (16, 20)]
if HULL:
    hull_connections += pseudo_hull_connections
else:
    connections += pseudo_hull_connections

detector = HandTracker(
    PALM_MODEL_PATH,
    LANDMARK_MODEL_PATH,
    ANCHORS_PATH,
    box_shift=0.2,
    box_enlarge=1.3
)

#Creating Gesture object and initialising timestamp


action = Gesture(connections,w,h,fps,codec)
action.timestamp = [capture.get(cv2.CAP_PROP_POS_MSEC)]
fps = capture.get(cv2.CAP_PROP_FPS)
print('FPS: ', fps)
frame_count = 0
first_time_delay = True
timer_test = capture.get(cv2.CAP_PROP_POS_MSEC)
print(timer_test)
which_hand = "left_hand"
rotate = False


while hasFrame:
    #frame = cv2.flip(frame1,1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if rotate == True:
       points, _ = detector(image)
    elif rotate == False:
        image_flip = cv2.flip(image,1)
        points, _ = detector(image_flip)

    points, _ = detector(image)

    frame_count +=1
    time_ = float(frame_count)/fps
    action.update_time(time_)

    end = timer()
    current_second = end - start
    cv2.putText(frame, "SEC: ", (600, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 40, 60), 2)
    cv2.putText(frame, str(round(end - start, 2)), (680, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 40, 60), 2)
    action.current_second = current_second

    if points is not None:

        #print("TIMER: ", capture.get(cv2.CAP_PROP_POS_MSEC))

        action.update_points(points)
        rotate = action.get_gesture()



        if rotate == True:
            image_flip = cv2.flip(image, 1)
            points, _ = detector(image_flip)


        if action.write is not None:
            cv2.putText(frame,action.write,(0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)



        #cv2.putText(frame, str(elapsed_time), (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 200, 50), 2)
        #print((now - beginning_of_day).seconds)

        for connection in connections:
            try:
                x0, y0, z0 = points[connection[0]]
                x1, y1, z1 = points[connection[1]]
            except TypeError:
                print("Error Exception - this error shows after no hand is seen in Przypadek4")

            cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), CONNECTION_COLOR, THICKNESS)
            if (connection[1] % 4) == 0:
                #Fingertip joints are represented in grayscale using depth data
                cv2.circle(frame, (int(x1), int(y1)), THICKNESS * 2, (int(-z1)*3,int(-z1)*3,int(-z1)*3), THICKNESS)
            elif connection[1] == 1:
                #Hand basejoint
                cv2.circle(frame, (int(x0), int(y0)), THICKNESS * 2, (int(-z0)*3,int(-z0)*3,int(-z0)*3), THICKNESS)


    cv2.imshow(WINDOW, frame)
    hasFrame, frame = capture.read()

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


# while hasFrame:
#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#     if rotate == True:
#        points, _ = detector(image)
#     elif rotate == False:
#         image_flip = cv2.flip(image,1)
#         points, _ = detector(image_flip)
#
#     points1, points2, _, _ = detector(image)
#
#     frame_count +=1
#     time_ = float(frame_count)/fps
#     action.update_time(time_)
#
#     end = timer()
#     current_second = end - start
#     cv2.putText(frame, "SEC: ", (600, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 40, 60), 2)
#     cv2.putText(frame, str(round(end - start, 2)), (680, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 40, 60), 2)
#     action.current_second = current_second
#
#     drawpointstoframe(points1, frame)
#     if MULTIHAND:
#         drawpointstoframe(points2, frame)
#
#     cv2.imshow(WINDOW, frame)
#     hasFrame, frame = capture.read()
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break

capture.release()
cv2.destroyAllWindows()