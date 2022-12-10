import cv2
import mrcnn.visualize
import numpy as np
import pickle


class Get_parking_spots:
    def __init__(self,):
        """Self variables"""
        self.image                  = None
        self.coppy_of_org_image     = None 
        self.filename               = None
        self.base_parking_spotsx    = [90, 190, 300, 400, 510, 610, 720, 820, 925, 1035, 1130, 1240, 1350, 1485]
        self.base_parking_spotsy    = 450
        self.r                      = None
        self.whos                   = []
        self.free_spots             = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_filename(self,filename):
        self.filename = filename
        
    def get_image(self):
        """Loads a specific image from a file name"""
        self.image = cv2.imread(self.filename)

    def change_color_space(self):
        """Changes the color space of an image"""
        self.coppy_of_org_image = self.image.copy()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def load_pickle_data(self):
        """loads picke data"""
        with open(self.filename.replace(".jpg", ".pkl"), 'rb') as f:
            self.r = pickle.load(f)

    def make_whos(self):
        """Creates a list of where the empty parking spots are"""
        for index in range(len(self.base_parking_spotsx)):
            found = False
            for i, box in enumerate(self.r['rois']):
                if box[1] < self.base_parking_spotsx[index] < box[3] and box[0] < self.base_parking_spotsy < box[2]:
                    self.whos.append(i)
                    found = True
                    self.free_spots[index] = 0
                    self.base_parking_spotsx[index] = int(np.ceil(self.base_parking_spotsx[index] + ((box[3] - box[1])/2)+box[1])/2)
                    break
                if not found:
                    self.free_spots[index] = 1
    
    def draw_spots(self):
        """Draws a green box where an emnpty spot is and a red whon where a taken spot is."""
        for index in range(len(self.free_spots)):
            if self.free_spots[index] == 0:
                cv2.rectangle(self.coppy_of_org_image, (self.base_parking_spotsx[index]-60, 400), (self.base_parking_spotsx[index]+40, 40+self.base_parking_spotsy), (0, 0, 250), -1)
                cv2.rectangle(self.coppy_of_org_image, (self.base_parking_spotsx[index]-60, 400), (self.base_parking_spotsx[index]+40, 40+self.base_parking_spotsy), (0, 0, 0), 2)
            else:
                cv2.rectangle(self.coppy_of_org_image, (self.base_parking_spotsx[index]-60, 400), (self.base_parking_spotsx[index]+40, 40+self.base_parking_spotsy), (0, 200, 0), -1)
                cv2.rectangle(self.coppy_of_org_image, (self.base_parking_spotsx[index]-60, 400), (self.base_parking_spotsx[index]+40, 40+self.base_parking_spotsy), (0, 0, 0), 2)

        alpha = 0.7  # Transparency factor.
        image_new = cv2.addWeighted(self.coppy_of_org_image, alpha, self.image, 1 - alpha, 0)
        cv2.imshow("image_new", image_new)
        cv2.waitKey(0)

if __name__ == "__main__":
    CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
    Current_spots = Get_parking_spots()
    Current_spots.get_filename(filename = "test_images/2022-12-05 15_00_13.jpg")
    Current_spots.get_image()
    Current_spots.change_color_space()
    Current_spots.load_pickle_data()
    Current_spots.make_whos()
    Current_spots.draw_spots()