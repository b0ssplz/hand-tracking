import numpy as np
from varname import Wrapper
from datetime import datetime,time


class Gesture():

    def __init__(self, connections,w,h,fps,codec):

        self.thumb_tip = 4
        self.fore_tip = 8
        self.middle_tip = 12
        self.ring_tip = 16
        self.pinky_tip = 20
        self.base_tip = 0

        self.timestamp = None
        self.time_passed = False
        self.flag_NEW = 'none'
        self.flag_NEW_before = 'none'

        self.thumb_tip_pos = []
        self.fore_tip_pos = []
        self.middle_tip_pos = []
        self.ring_tip_pos = []
        self.pinky_tip_pos = []
        self.base_pos = []

        self.flag = 0
        self.flag_MAIN = True
        self.t = 0
        self.write = None

        self.info_counter = 1
        self.logFileSeparation = True

        self.w = w
        self.h =h
        self.fps = fps
        self.codec = codec

        self.right_hand = False
        self.left_hand = True

        self.left_hand_before = False
        self.right_hand_before = False
        self.przypadek = 0
        self.rotate = False

        self.current_second = 0


    def update_time(self, timestamp_val):
        """
        Updates timestamps of new frames
        Updates flag
        """

        self.timestamp.append(timestamp_val)
        self.getdiff()

    def getdiff(self):
        """
        1sec wait time before next gesture inferred
        """
        if (self.timestamp[-1] - self.t) > 0.3:
            self.flag = 0
        else:
            self.flag = 1
        # self.flag = 0

    def update_points(self, points):
        """
        Updates position of finger and base

        Args:
        points: array containing coordinates of joints
        """
        self.thumb_tip_pos.append(points[self.thumb_tip])
        self.fore_tip_pos.append(points[self.fore_tip])
        self.middle_tip_pos.append(points[self.middle_tip])
        self.ring_tip_pos.append(points[self.ring_tip])
        self.pinky_tip_pos.append(points[self.pinky_tip])
        self.base_pos.append(points[self.base_tip])

    def update_flags(self, flags):
        pass

    def print_info(self,info):

        print(self.info_counter,": ",info)
        logFile = open('logFile.txt', "a")
        if self.logFileSeparation:
            logFile.writelines("{}\n".format("----------------------------"))
            logFile.writelines("{}\n".format(str(datetime.now())))
            logFile.writelines("Resolution: {} x {}\n".format(self.w,self.h))
            logFile.writelines("FPS: {}\n".format(self.fps))
            logFile.writelines("Codec: {}\n".format(self.codec))
            logFile.writelines("{}\n".format("----------------------------"))

            self.logFileSeparation = False

        if self.logFileSeparation == False:

            logFile.writelines("[{}-{}-{}-{}]  {}: {}\n".format(datetime.now().hour,datetime.now().minute,datetime.now().second,datetime.now().microsecond,self.info_counter,info))
        logFile.close()

        self.info_counter +=1

    def get_gesture(self):

        # print('thumb_triangle_diff_X: ', abs(self.thumb_tip_pos[-1][0] - (self.thumb_tip_pos[-1][0] + self.ring_tip_pos[-1][0] + self.pinky_tip_pos[-1][0])/3))
        # print('Fore X: ', self.fore_tip_pos[-1][0])
        # print('Fore Y: ', self.fore_tip_pos[-1][1])
        # print('Middle X: ', self.middle_tip_pos[-1][0])
        # print('Middle Y: ', self.middle_tip_pos[-1][1])
        # print('Base X: ', self.base_pos[-1][0])
        # print('Base Y: ', self.base_pos[-1][1])

        print("PRZYPADEK: ", self.przypadek)

        if len(self.fore_tip_pos) > 8:

            if self.timestamp[-1] - self.t > 0.3:
                self.time_passed = True

            if self.time_passed:

                diff_dict1 = self.check_diffs(1, 1)
                #diff_dict3 = self.check_diffs(3, 3)
                diff_dict5 = self.check_diffs(5, 5)
                #diff_dict9 = self.check_diffs(9, 9)
                diff_dict_speed = self.check_diffs(3, 1) #so fast gestures won't be recognized

                # Creating Thumb-Ring-Pinky Triangle
                Triangle_X = (self.thumb_tip_pos[-1][0] + self.ring_tip_pos[-1][0] + self.pinky_tip_pos[-1][0]) / 3
                Triangle_Y = (self.thumb_tip_pos[-1][1] + self.ring_tip_pos[-1][1] + self.pinky_tip_pos[-1][1]) / 3

                ###Checking
                # diff_dict = self.check_diffs()

                thumb_triangle_diff_X = abs(self.thumb_tip_pos[-1][0] - Triangle_X)
                thumb_triangle_diff_Y = abs(self.thumb_tip_pos[-1][1] - Triangle_Y)

                ring_triangle_diff_X = abs(self.ring_tip_pos[-1][0] - Triangle_X)
                ring_triangle_diff_Y = abs(self.ring_tip_pos[-1][1] - Triangle_Y)

                pinky_triangle_diff_X = abs(self.pinky_tip_pos[-1][0] - Triangle_X)
                pinky_triangle_diff_Y = abs(self.pinky_tip_pos[-1][1] - Triangle_Y)

                self.swipe_left()
                self.swipe_right()
                self.secret_gesture(diff_dict1, diff_dict_speed, Triangle_X, Triangle_Y,thumb_triangle_diff_X, thumb_triangle_diff_Y, ring_triangle_diff_X, ring_triangle_diff_Y, pinky_triangle_diff_X, pinky_triangle_diff_Y )
                self.halt(diff_dict1, diff_dict5)
                self.peace(diff_dict1, diff_dict_speed, Triangle_X, Triangle_Y,thumb_triangle_diff_X, thumb_triangle_diff_Y, ring_triangle_diff_X, ring_triangle_diff_Y, pinky_triangle_diff_X, pinky_triangle_diff_Y )
                self.okay(diff_dict1, diff_dict_speed)
                self.empty()
                self.scroll_down()
                self.scroll_up()
                self.fist(diff_dict1, diff_dict_speed, Triangle_X, thumb_triangle_diff_X, thumb_triangle_diff_Y, ring_triangle_diff_X, ring_triangle_diff_Y, pinky_triangle_diff_X, pinky_triangle_diff_Y  )


            if self.przypadek == 0 or self.przypadek == 1:
                if self.empty() == True:
                    self.przypadek = 1
                if self.empty_right() == True: #was elif
                    self.przypadek = 2
                self.rotate = False
                return False

            elif self.przypadek == 2:
                if self.empty() == True:
                    self.przypadek = 3
                if self.empty_right() == True:
                    self.przypadek = 4
                if self.rotate == False:
                    return True  # OBROT

            elif self.przypadek == 3:
                if self.empty() == True:
                    self.przypadek = 3
                if self.empty_right() == True:
                    self.przypadek = 4
                return False

            elif self.przypadek == 4:
                if self.empty() == True:
                    self.przypadek = 1
                if self.empty_right() == True:
                    self.przypadek = 2
                if self.rotate == False:
                    return True

    def gesture_detected_procedures(self, text):
        self.write = text
        self.print_info(text)
        self.flag_NEW = text
        self.flag_MAIN = False
        self.t = self.timestamp[-1]
        self.time_passed = False


    def swipe_right(self):

        if self.flag_NEW != 'Swipe left' and self.flag_NEW == 'Empty':

            frame_before = False

            if self.fore_tip_pos[-3][0] < 0.8 * self.fore_tip_pos[-8][0]:
                self.print_info('swipe right - if nr 1 passed')
                if self.middle_tip_pos[-3][0] < 0.8 * self.middle_tip_pos[-8][0]:
                    self.print_info('swipe right - if nr 2 passed')
                    if self.ring_tip_pos[-3][0] < 0.8 * self.ring_tip_pos[-8][0]:
                        self.print_info('swipe right - if nr 3 passed')
                        if self.pinky_tip_pos[-3][0] < 0.8 * self.pinky_tip_pos[-8][0]:
                            frame_before = True

            if frame_before:
                if self.fore_tip_pos[-1][0] < 1.2 * self.fore_tip_pos[-3][0] and self.fore_tip_pos[-1][0] > 0.8 * \
                        self.fore_tip_pos[-3][0]:
                    self.print_info('swipe right - if nr 4 passed')
                    if self.middle_tip_pos[-1][0] < 1.2 * self.middle_tip_pos[-3][0] and self.middle_tip_pos[-1][
                        0] > 0.8 * self.middle_tip_pos[-3][0]:
                        self.print_info('swipe right - if nr 5 passed')
                        if self.ring_tip_pos[-1][0] < 1.2 * self.ring_tip_pos[-3][0] and self.ring_tip_pos[-1][
                            0] > 0.8 * self.ring_tip_pos[-3][0]:
                            self.print_info('swipe right - if nr 6 passed')
                            if self.pinky_tip_pos[-1][0] < 1.2 * self.pinky_tip_pos[-3][0] and self.pinky_tip_pos[-1][
                                0] > 0.8 * self.pinky_tip_pos[-3][0]:
                                self.gesture_detected_procedures("Swipe right")

    def swipe_left(self):

        if self.flag_NEW != 'Swipe left' and self.flag_NEW == 'Empty':


            # check_right_frame = self.middle_tip_pos[-1][0] > self.base_pos[-1][0]
            # check_left_frame = self.middle_tip_pos[len(self.middle_tip_pos) - 2][0] < self.base_pos[len(self.base_pos) - 2][0]
            # diff_tip_tip = abs(self.middle_tip_pos[len(self.middle_tip_pos) - 2][0] - self.middle_tip_pos[-1][0])
            # diff_tip_base = abs(self.middle_tip_pos[-1][0] - self.base_pos[-1][0])
            #
            # if check_right_frame and check_left_frame:
            #     if diff_tip_tip > 50 and diff_tip_base > 30:
            #         self.write = "Swipe right"
            #         print("Swipe right")
            #         self.flag_NEW = 'Swipe right'
            #         self.flag_MAIN = False
            #         self.t = self.timestamp[-1]
            #         self.time_passed = False

            frame_before = False

            if self.fore_tip_pos[-3][0] > 1.2 * self.fore_tip_pos[-8][0]:
                self.print_info('swipe left - if nr 1 passed')
                if self.middle_tip_pos[-3][0] > 1.2 * self.middle_tip_pos[-8][0]:
                    self.print_info('swipe left - if nr 2 passed')
                    if self.ring_tip_pos[-3][0] > 1.2 * self.ring_tip_pos[-8][0]:
                        self.print_info('swipe left - if nr 3 passed')
                        if self.pinky_tip_pos[-3][0] > 1.2 * self.pinky_tip_pos[-8][0]:
                            frame_before = True

            if frame_before:
                if self.fore_tip_pos[-1][0] < 1.2 * self.fore_tip_pos[-3][0] and self.fore_tip_pos[-1][0] > 0.8 * self.fore_tip_pos[-3][0]:
                    self.print_info('swipe left - if nr 4 passed')
                    if self.middle_tip_pos[-1][0] < 1.2 * self.middle_tip_pos[-3][0] and self.middle_tip_pos[-1][0] > 0.8 * self.middle_tip_pos[-3][0]:
                        self.print_info('swipe left - if nr 5 passed')
                        if self.ring_tip_pos[-1][0] < 1.2 * self.ring_tip_pos[-3][0] and self.ring_tip_pos[-1][0] > 0.8 * self.ring_tip_pos[-3][0]:
                            self.print_info('swipe left - if nr 6 passed')
                            if self.pinky_tip_pos[-1][0] < 1.2 * self.pinky_tip_pos[-3][0] and self.pinky_tip_pos[-1][0] > 0.8 * self.pinky_tip_pos[-3][0]:
                                self.gesture_detected_procedures("Swipe left")

    def scroll_up(self):

        if self.flag_NEW != 'Scroll Up' and self.flag_NEW == 'Empty':

            frame_before = False

            if self.fore_tip_pos[-9][1] > self.fore_tip_pos[-3][1] * 1.9:
                self.print_info('Scroll Up - if nr 1 passed')
                if self.middle_tip_pos[-9][1] > self.middle_tip_pos[-3][1] * 1.9:
                    self.print_info('Scroll Up - if nr 2 passed')
                    if self.ring_tip_pos[-9][1] > self.ring_tip_pos[-3][1] * 1.9:
                        self.print_info('Scroll Up - if nr 3 passed')
                        if self.pinky_tip_pos[-9][1] > self.pinky_tip_pos[-3][1] * 1.9:
                            self.print_info('Scroll Up - if nr 4 passed')
                            frame_before = True

            if frame_before:
                if self.fore_tip_pos[-1][1] < 1.2 * self.fore_tip_pos[-3][1] and self.fore_tip_pos[-1][1] > 0.8 * self.fore_tip_pos[-3][1]:
                    self.print_info('Scroll Up - if nr 5 passed')
                    if self.middle_tip_pos[-1][1] < 1.2 * self.middle_tip_pos[-3][1] and self.middle_tip_pos[-1][1] > 0.8 * self.middle_tip_pos[-3][1]:
                        self.print_info('Scroll Up - if nr 6 passed')
                        if self.ring_tip_pos[-1][1] < 1.2 * self.ring_tip_pos[-3][1] and self.ring_tip_pos[-1][1] > 0.8 * self.ring_tip_pos[-3][1]:
                            self.print_info('Scroll Up - if nr 7 passed')
                            if self.pinky_tip_pos[-1][1] < 1.2 * self.pinky_tip_pos[-3][1] and self.pinky_tip_pos[-1][1] > 0.8 * self.pinky_tip_pos[-3][1]:

                                self.gesture_detected_procedures("Scroll Up")

    def scroll_down(self):

        if self.flag_NEW != 'Scroll Down' and self.flag_NEW == 'Empty':

            frame_before = False

            if self.fore_tip_pos[-5][1] > self.base_pos[-8][1]:
                self.print_info('Scroll Down - if nr 1 passed')
                if self.middle_tip_pos[-5][1] > self.base_pos[-8][1]:
                    self.print_info('Scroll Down - if nr 2 passed')
                    if self.ring_tip_pos[-5][1] > self.base_pos[-8][1]:
                        self.print_info('Scroll Down - if nr 3 passed')
                        if self.pinky_tip_pos[-5][1] > self.base_pos[-8][1]:
                            self.print_info('Scroll Down - if nr 4 passed')
                            frame_before = True

            if frame_before == True:
                if self.fore_tip_pos[-1][1] < 0.9 * self.base_pos[-1][1]:
                    self.print_info('Scroll Down - if nr 5 passed')
                    if self.middle_tip_pos[-1][1] < 0.9 * self.base_pos[-1][1]:
                        self.print_info('Scroll Down - if nr 6 passed')
                        if self.ring_tip_pos[-1][1] < 0.9 * self.base_pos[-1][1]:
                            self.print_info('Scroll Down - if nr 7 passed')
                            if self.pinky_tip_pos[-1][1] < 0.9 * self.base_pos[-1][1]:

                                self.gesture_detected_procedures("Scroll Down")

    def scroll_NEW(self):

        if self.flag_NEW != 'Scroll Up' and self.flag_NEW == 'Empty':

            frame_before = False

            if self.fore_tip_pos[-5][1] < self.base_pos[-5][1]:
                if self.middle_tip_pos[-5][1] < self.base_pos[-5][1]:
                    if self.ring_tip_pos[-5][1] < self.base_pos[-5][1]:
                        if self.pinky_tip_pos[-5][1] < self.base_pos[-5][1]:
                            frame_before = True

            if frame_before == True:
                if self.fore_tip_pos[-1][1] > self.base_pos[-1][1]:
                    if self.middle_tip_pos[-1][1] > self.base_pos[-1][1]:
                        if self.ring_tip_pos[-1][1] > self.base_pos[-1][1]:
                            if self.pinky_tip_pos[-1][1] > self.base_pos[-1][1]:

                                self.gesture_detected_procedures("Scroll Up")

    def peace(self, diff_dict, diff_dict_speed, Triangle_X, Triangle_Y,thumb_triangle_diff_X, thumb_triangle_diff_Y, ring_triangle_diff_X, ring_triangle_diff_Y, pinky_triangle_diff_X, pinky_triangle_diff_Y ):

        if self.flag_NEW != 'Peace':

            #check_fore = self.fore_tip_pos[-1][1] < self.fore_tip_pos[len(self.fore_tip_pos) - 2][1]
            #check_middle = self.middle_tip_pos[-1][1] < self.middle_tip_pos[len(self.middle_tip_pos) - 2][1]

            #diff_fore_tip_base = self.base_pos[-1][1] - self.fore_tip_pos[-1][1]
            #diff_middle_tip_base = self.base_pos[-1][1] - self.middle_tip_pos[-1][1]

            if diff_dict_speed["base_base_diff_X"] < 30 and  diff_dict_speed["base_base_diff_Y"] < 30:


                if thumb_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and thumb_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3) \
                        and ring_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and ring_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3) \
                        and pinky_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and pinky_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3):
                    self.print_info('peace - if nr 1 passed')
                    if Triangle_X > 0.8 * self.fore_tip_pos[-1][0] and Triangle_X < 1.2 * self.middle_tip_pos[-1][0] :
                        self.print_info('peace - if nr 2 passed')
                        if Triangle_Y < self.base_pos[-1][1] and Triangle_Y > self.fore_tip_pos[-1][1] and Triangle_Y > \
                                self.middle_tip_pos[-1][1]:
                            self.print_info('peace - if nr 3 passed')
                            if diff_dict["fore_base_diff_Y"] > (diff_dict["fore_middle_diff_X"] * 1.5) and diff_dict[
                                "middle_base_diff_Y"] > (diff_dict["fore_middle_diff_X"] * 1.5):  # Darkblue and Violet
                                self.print_info('peace - if nr 4 passed')
                                if diff_dict["fore_middle_diff_X"] > (diff_dict["middle_base_diff_Y"] / 4.15):  # Green
                                    self.print_info('peace - if nr 5 passed')
                                    if self.base_pos[-1][0] > 0.8 * self.fore_tip_pos[-1][0] and self.base_pos[-1][0] < \
                                            1.2 * self.middle_tip_pos[-1][0]:  # base between fingers
                                        self.print_info('peace - if nr 6 passed')

                                        self.gesture_detected_procedures("Peace")

    def secret_gesture(self, diff_dict, diff_dict_speed, Triangle_X, Triangle_Y,thumb_triangle_diff_X, thumb_triangle_diff_Y, ring_triangle_diff_X, ring_triangle_diff_Y, pinky_triangle_diff_X, pinky_triangle_diff_Y ):

        if self.flag_NEW != 'Secret_gesture':

            #check_fore = self.fore_tip_pos[-1][1] < self.fore_tip_pos[len(self.fore_tip_pos) - 2][1]
            #check_middle = self.middle_tip_pos[-1][1] < self.middle_tip_pos[len(self.middle_tip_pos) - 2][1]

            #diff_fore_tip_base = self.base_pos[-1][1] - self.fore_tip_pos[-1][1]
            #diff_middle_tip_base = self.base_pos[-1][1] - self.middle_tip_pos[-1][1]

            if diff_dict_speed["base_base_diff_X"] < 30 and  diff_dict_speed["base_base_diff_Y"] < 30:


                if thumb_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and thumb_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3) \
                        and ring_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and ring_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3) \
                        and pinky_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and pinky_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3):
                    self.print_info('secret_gesture - if nr 1 passed')
                    if self.middle_tip_pos[-1][1] < 0.9 * self.fore_tip_pos[-1][1] and Triangle_X < self.middle_tip_pos[-1][0]:
                        self.print_info('secret_gesture - if nr 2 passed')
                        if Triangle_Y < self.base_pos[-1][1] and Triangle_Y > self.fore_tip_pos[-1][1] and Triangle_Y > \
                                self.middle_tip_pos[-1][1]:
                            self.print_info('secret_gesture - if nr 3 passed')
                            if diff_dict["fore_base_diff_Y"] > (diff_dict["fore_middle_diff_X"] * 1.5) and diff_dict[
                                "middle_base_diff_Y"] > (diff_dict["fore_middle_diff_X"] * 1.5):  # Darkblue and Violet
                                self.print_info('secret_gesture - if nr 4 passed')
                                if diff_dict["fore_base_diff_Y"] < 0.9 * diff_dict["middle_base_diff_Y"]:  # Green
                                    self.print_info('Secret_gesture - if nr 5 passed')

                                    self.gesture_detected_procedures("Secret_gesture")

    def okay(self, diff_dict, diff_dict_speed) :

        if self.flag_NEW != 'Okay':

            #diff_dict = self.check_diffs()

            if diff_dict_speed["base_base_diff_X"] < 30 and  diff_dict_speed["base_base_diff_Y"] < 30:



                if self.thumb_tip_pos[-1][1] < self.fore_tip_pos[-1][1] <  self.pinky_tip_pos[-1][1] and self.ring_tip_pos[-1][1] < self.base_pos[-1][1]:
                    self.print_info('okay - if nr 1 passed')

                    if diff_dict["thumb_base_diff_Y"] > 2.5 * diff_dict["fore_middle_diff_Y"]:
                        self.print_info('okay - if nr 2 passed')
                        if diff_dict["pinky_base_diff_X"] < 1.35 * diff_dict["fore_base_diff_X"]:
                            self.print_info('okay - if nr 3 passed')
                            print("diff_dict["'pinky_base_diff_X'"] :  ", diff_dict["pinky_base_diff_X"])
                            print("diff_dict["'fore_base_diff_X'"] :  ", diff_dict["fore_base_diff_X"])
                            if diff_dict["pinky_base_diff_X"] > 0.35 * diff_dict["fore_base_diff_X"]:
                                self.print_info('okay - if nr 4 passed')
                                if self.thumb_tip_pos[-1][0] > 0.65 * self.fore_tip_pos[-1][0]:
                                    self.print_info('okay - if nr 5 passed')
                                    if self.thumb_tip_pos[-1][0] < 1.35 * self.fore_tip_pos[-1][0]:
                                        self.print_info('okay - if nr 6 passed')

                                        self.gesture_detected_procedures("Okay")

    def empty(self):

        detected = False

        if self.flag_NEW != 'Empty':

            diff_dict = self.check_diffs()
            diff_dict_speed = self.check_diffs(3, 1)  # so fast gestures won't be recognized

            if diff_dict_speed["base_base_diff_X"] < 30 and  diff_dict_speed["base_base_diff_Y"] < 30:

                if self.thumb_tip_pos[-1][0] < self.fore_tip_pos[-1][0] < self.middle_tip_pos[-1][0] < \
                        self.ring_tip_pos[-1][0] < self.pinky_tip_pos[-1][0]:
                    self.print_info('empty - if nr 1 passed')
                    if self.base_pos[-1][0] > self.thumb_tip_pos[-1][0] and self.base_pos[-1][0] < self.pinky_tip_pos[-1][0]:
                        self.print_info('empty - if nr 2 passed')
                        if self.pinky_tip_pos[-1][1] > self.middle_tip_pos[-1][1]:
                            self.print_info('empty - if nr 3 passed')
                            if self.pinky_tip_pos[-1][1] < self.thumb_tip_pos[-1][1] < self.base_pos[-1][1]:
                                self.print_info('empty - if nr 4 passed')
                                if diff_dict["fore_middle_diff_Y"] < 1.25 * diff_dict["fore_pinky_diff_Y"]:
                                    self.print_info('empty = if nr 5 passed')
                                    # if middle_base_diff_X < middle_pinky_diff_X:
                                    #   print('empty - if nr 6 passed')
                                    if diff_dict["middle_base_diff_Y"] > diff_dict["thumb_middle_diff_Y"]:

                                        self.gesture_detected_procedures("Empty")
                                        if self.right_hand == True:
                                            print("HAND HAS BEEN SWITCHED TO LEFT.")
                                        self.right_hand = False
                                        return True
                else:
                    return False

                self.empty_right()

    def empty_right(self):

        if self.flag_NEW != 'Empty':

            diff_dict = self.check_diffs()



            if self.thumb_tip_pos[-1][0] > self.fore_tip_pos[-1][0] > self.middle_tip_pos[-1][0] > \
                    self.ring_tip_pos[-1][0] > self.pinky_tip_pos[-1][0]:
                self.print_info('empty - if nr 1 passed')
                if self.base_pos[-1][0] < self.thumb_tip_pos[-1][0] and self.base_pos[-1][0] > self.pinky_tip_pos[-1][0]:
                    self.print_info('empty - if nr 2 passed')
                    if self.pinky_tip_pos[-1][1] > self.middle_tip_pos[-1][1]:
                        self.print_info('empty - if nr 3 passed')
                        if self.pinky_tip_pos[-1][1] < self.thumb_tip_pos[-1][1] < self.base_pos[-1][1]:
                            self.print_info('empty - if nr 4 passed')
                            if diff_dict["fore_middle_diff_Y"] < 1.25 * diff_dict["fore_pinky_diff_Y"]:
                                self.print_info('empty = if nr 5 passed')
                                # if middle_base_diff_X < middle_pinky_diff_X:
                                #   print('empty - if nr 6 passed')
                                if diff_dict["middle_base_diff_Y"] > diff_dict["thumb_middle_diff_Y"]:

                                    self.gesture_detected_procedures("Empty")

                                    if self.right_hand == False:
                                        print("HAND HAS BEEN SWITCHED TO RIGHT.")
                                    self.right_hand = True
                                    return True
            else:
                return False



    def halt(self, diff_dict1, diff_dict5):

        if self.flag_NEW != 'Halt' and self.flag_NEW == 'Empty':

            #diff_dict1 = self.check_diffs(1, 1)
            #diff_dict3 = self.check_diffs(3, 3)
            #diff_dict5 = self.check_diffs(5, 5)
            #diff_dict9 = self.check_diffs(9, 9)



            frame_before = False

            if diff_dict1["thumb_base_diff_X"] < 0.5 * diff_dict5["thumb_base_diff_X"]:
                self.print_info('halt - if nr 1 passed')
                if diff_dict1["fore_middle_diff_X"] < 0.95 * diff_dict5["fore_middle_diff_X"]:
                    self.print_info('halt - if nr 2 passed')
                    if diff_dict1["middle_pinky_diff_X"] < 0.95 * diff_dict5["middle_pinky_diff_X"]:
                        frame_before = True
                        self.print_info('halt - if nr 3 passed')

            if frame_before == True:
                if self.base_pos[-1][1] > 0.9 * self.base_pos[-9][1] and self.base_pos[-1][1] < 1.1  * self.base_pos[-9][1]:
                    self.print_info('halt - if nr 4 passed')
                    if self.thumb_tip_pos[-1][0] > 0.9 * self.thumb_tip_pos[-3][0] and self.thumb_tip_pos[-1][0] < 1.1 * self.thumb_tip_pos[-3][0]:
                        self.print_info('halt - if nr 5 passed')
                        if self.fore_tip_pos[-1][0] > 0.9 * self.fore_tip_pos[-3][0] and self.fore_tip_pos[-1][0] < 1.1 * self.fore_tip_pos[-3][0]:
                            self.print_info('halt - if nr 6 passed')
                            if self.middle_tip_pos[-1][0] > 0.9 * self.middle_tip_pos[-3][0] and self.middle_tip_pos[-1][0] < 1.1 * self.middle_tip_pos[-3][0]:
                                self.print_info('halt - if nr 7 passed')
                                if self.ring_tip_pos[-1][0] > 0.9 * self.ring_tip_pos[-3][0] and self.ring_tip_pos[-1][0] < 1.1 * self.ring_tip_pos[-3][0]:
                                    self.print_info('halt - if nr 8 passed')
                                    if self.pinky_tip_pos[-1][0] > 0.9 * self.pinky_tip_pos[-3][0] and self.pinky_tip_pos[-1][0] < 1.1 * self.pinky_tip_pos[-3][0]:

                                        self.gesture_detected_procedures("Halt")

    def fist(self, diff_dict, diff_dict_speed, Triangle_X, thumb_triangle_diff_X, thumb_triangle_diff_Y, ring_triangle_diff_X, ring_triangle_diff_Y, pinky_triangle_diff_X, pinky_triangle_diff_Y  ):

        if self.flag_NEW != 'Fist':

            #diff_dict1 = self.check_diffs(1, 1)
            #diff_dict3 = self.check_diffs(3, 3)
            #diff_dict5 = self.check_diffs(5, 5)
            #diff_dict9 = self.check_diffs(9, 9)

            #combo = (diff_dict1["fore_middle_diff_Y"] )


            #jesli nagle wszystkie 5 punktow zblizylo sie do siebie
            #baza jest oddalona od pozostalych 4
            # te 4 palce sa mega blisko w linii poziomej

            #obecnie pass1: roznica w Y miedzy czubkami palcow mniejsza od 30
            #pass 2: base ponizej palca
            #pass 3: if thumb-base Y jest wieksza od fore_base

            if diff_dict_speed["base_base_diff_X"] < 30 and diff_dict_speed["base_base_diff_Y"] < 30:

                average_fingers_pos = (self.fore_tip_pos[-1][1] + self.middle_tip_pos[-1][1] + self.ring_tip_pos[-1][1] + self.pinky_tip_pos[-1][1] + self.thumb_tip_pos[-1][1]) / 5
                average_base_diff = self.base_pos[-1][1] - average_fingers_pos
                average_thumb_diff = abs(self.thumb_tip_pos[-1][1] - average_fingers_pos)
                average_fore_diff = abs(self.fore_tip_pos[-1][1] - average_fingers_pos)
                average_middle_diff = abs(self.middle_tip_pos[-1][1] - average_fingers_pos)
                average_ring_diff = abs(self.ring_tip_pos[-1][1] - average_fingers_pos)




                if not(thumb_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and thumb_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3) \
                        and ring_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and ring_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3) \
                        and pinky_triangle_diff_X < (diff_dict["middle_base_diff_Y"] / 3) and pinky_triangle_diff_Y < (
                        diff_dict["middle_base_diff_Y"] / 3)):
                    self.print_info('fist - if nr 1 passed')
                    if not(Triangle_X > self.fore_tip_pos[-1][0] and Triangle_X < self.middle_tip_pos[-1][0]):
                        self.print_info('fist - if nr 2 passed')
                        if average_thumb_diff < 0.5 * average_base_diff:
                            self.print_info('fist - if nr 3 passed')
                            if self.base_pos[-1][1] > self.fore_tip_pos[-1][1]:
                                self.print_info('fist - if nr 4 passed')
                                if average_thumb_diff < 2 * average_ring_diff:
                                    self.print_info('fist - if nr 5 passed')
                                    if average_middle_diff < 2 * average_ring_diff:
                                        self.print_info('fist - if nr 6 passed')
                                        if average_fore_diff < 2 * average_ring_diff:

                                            self.gesture_detected_procedures("Fist")



    def check_diffs(self, i = 1, j = 1):

        thumb_thumb_diff_X = Wrapper(abs(self.thumb_tip_pos[-i][0] - self.thumb_tip_pos[-j][0]))
        thumb_thumb_diff_Y = Wrapper(abs(self.thumb_tip_pos[-i][1] - self.thumb_tip_pos[-j][1]))

        fore_fore_diff_X = Wrapper(abs(self.fore_tip_pos[-i][0] - self.fore_tip_pos[-j][0]))
        fore_fore_diff_Y = Wrapper(abs(self.fore_tip_pos[-i][1] - self.fore_tip_pos[-j][1]))

        middle_middle_diff_X = Wrapper(abs(self.middle_tip_pos[-i][0] - self.middle_tip_pos[-j][0]))
        middle_middle_diff_Y = Wrapper(abs(self.middle_tip_pos[-i][1] - self.middle_tip_pos[-j][1]))

        ring_ring_diff_X = Wrapper(abs(self.ring_tip_pos[-i][0] - self.ring_tip_pos[-j][0]))
        ring_ring_diff_Y = Wrapper(abs(self.ring_tip_pos[-i][1] - self.ring_tip_pos[-j][1]))

        pinky_pinky_diff_X = Wrapper(abs(self.pinky_tip_pos[-i][0] - self.pinky_tip_pos[-j][0]))
        pinky_pinky_diff_Y = Wrapper(abs(self.pinky_tip_pos[-i][1] - self.pinky_tip_pos[-j][1]))

        base_base_diff_X = Wrapper(abs(self.pinky_tip_pos[-i][0] - self.pinky_tip_pos[-j][0]))
        base_base_diff_Y = Wrapper(abs(self.pinky_tip_pos[-i][1] - self.pinky_tip_pos[-j][1]))


        thumb_fore_diff_X = Wrapper(abs(self.thumb_tip_pos[-i][0] - self.fore_tip_pos[-j][0]))
        thumb_fore_diff_Y = Wrapper(abs(self.thumb_tip_pos[-i][1] - self.fore_tip_pos[-j][1]))
        thumb_middle_diff_X = Wrapper(abs(self.thumb_tip_pos[-i][0] - self.fore_tip_pos[-j][0]))
        thumb_middle_diff_Y = Wrapper(abs(self.thumb_tip_pos[-i][1] - self.fore_tip_pos[-j][1]))
        thumb_ring_diff_X = Wrapper(abs(self.thumb_tip_pos[-i][0] - self.fore_tip_pos[-j][0]))
        thumb_ring_diff_Y = Wrapper(abs(self.thumb_tip_pos[-i][1] - self.fore_tip_pos[-j][1]))
        thumb_pinky_diff_X = Wrapper(abs(self.thumb_tip_pos[-i][0] - self.fore_tip_pos[-j][0]))
        thumb_pinky_diff_Y = Wrapper(abs(self.thumb_tip_pos[-i][1] - self.fore_tip_pos[-j][1]))
        thumb_base_diff_X = Wrapper(abs(self.base_pos[-i][0] - self.thumb_tip_pos[-j][0]))
        thumb_base_diff_Y = Wrapper(abs(self.base_pos[-i][1] - self.thumb_tip_pos[-j][1]))

        fore_middle_diff_X = Wrapper(abs(self.middle_tip_pos[-i][0] - self.fore_tip_pos[-j][0]))  # DarkGrey
        fore_middle_diff_Y = Wrapper(abs(self.middle_tip_pos[-i][1] - self.fore_tip_pos[-j][1]))
        fore_ring_diff_X = Wrapper(abs(self.ring_tip_pos[-i][0] - self.fore_tip_pos[-j][0]))
        fore_ring_diff_Y = Wrapper(abs(self.ring_tip_pos[-i][1] - self.fore_tip_pos[-j][1]))
        fore_pinky_diff_X = Wrapper(abs(self.pinky_tip_pos[-i][0] - self.fore_tip_pos[-j][0]))
        fore_pinky_diff_Y = Wrapper(abs(self.pinky_tip_pos[-i][1] - self.fore_tip_pos[-j][1]))
        fore_base_diff_X = Wrapper(abs(self.base_pos[-i][0] - self.fore_tip_pos[-j][0]))  # LightOrange
        fore_base_diff_Y = Wrapper(abs(self.base_pos[-i][1] - self.fore_tip_pos[-j][1]))  # LightOrange

        middle_ring_diff_X = Wrapper(abs(self.base_pos[-i][0] - self.middle_tip_pos[-j][0]))  # DarkOrange
        middle_ring_diff_Y = Wrapper(abs(self.base_pos[-i][1] - self.middle_tip_pos[-j][1]))  # DarkOrange
        middle_pinky_diff_X = Wrapper(abs(self.pinky_tip_pos[-i][0] - self.middle_tip_pos[-j][0]))
        middle_pinky_diff_Y = Wrapper(abs(self.pinky_tip_pos[-i][1] - self.middle_tip_pos[-j][1]))
        middle_base_diff_X = Wrapper(abs(self.middle_tip_pos[-i][0] - self.base_pos[-j][0]))  # Blue
        middle_base_diff_Y = Wrapper(abs(self.middle_tip_pos[-i][1] - self.base_pos[-j][1]))  # Blue

        ring_pinky_diff_X = Wrapper(abs(self.pinky_tip_pos[-i][0] - self.ring_tip_pos[-j][0]))
        ring_pinky_diff_Y = Wrapper(abs(self.pinky_tip_pos[-i][0] - self.ring_tip_pos[-j][0]))
        ring_base_diff_X = Wrapper(abs(self.base_pos[-i][0] - self.ring_tip_pos[-j][0]))
        ring_base_diff_Y = Wrapper(abs(self.base_pos[-i][1] - self.ring_tip_pos[-j][1]))

        pinky_base_diff_X = Wrapper(abs(self.base_pos[-i][0] - self.pinky_tip_pos[-j][0]))
        pinky_base_diff_Y = Wrapper(abs(self.base_pos[-i][1] - self.pinky_tip_pos[-j][1]))

        def values_to_dict(*args):
            #print(args)
            return {i.name: i.value for i in args}

        mydict = values_to_dict(thumb_fore_diff_X, thumb_fore_diff_Y, thumb_middle_diff_X, thumb_middle_diff_Y,
                                thumb_ring_diff_X, thumb_ring_diff_Y, thumb_pinky_diff_X, thumb_pinky_diff_Y,
                                thumb_base_diff_X,
                                thumb_base_diff_Y, fore_middle_diff_X, fore_middle_diff_Y, fore_ring_diff_X,
                                fore_ring_diff_Y,
                                fore_pinky_diff_X, fore_pinky_diff_Y, fore_base_diff_X, fore_base_diff_Y,
                                middle_ring_diff_X,
                                middle_ring_diff_Y, middle_pinky_diff_X, middle_pinky_diff_Y, middle_base_diff_X,
                                middle_base_diff_Y,
                                ring_pinky_diff_X, ring_pinky_diff_Y, ring_base_diff_X, ring_base_diff_Y,
                                pinky_base_diff_X, pinky_base_diff_Y,
                                thumb_thumb_diff_X, thumb_thumb_diff_Y, fore_fore_diff_X, fore_fore_diff_Y,
                                middle_middle_diff_X,middle_middle_diff_Y,ring_ring_diff_X,ring_ring_diff_Y,
                                pinky_pinky_diff_X,pinky_pinky_diff_Y,base_base_diff_Y,base_base_diff_X)

        return mydict

