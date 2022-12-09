import cv2
import mrcnn.visualize
import numpy as np


CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

# load the input image, convert it from BGR to RGB channel
filename = "test_images/2022-12-05 15_00_13.jpg"
image = cv2.imread(filename)
overlay = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

import pickle
with open(filename.replace(".jpg", ".pkl"), 'rb') as f:
    r = pickle.load(f)

print(len(r['rois']))

space_xpos = [90, 190, 300, 400, 510, 610, 720, 820, 925, 1035, 1130, 1240, 1350, 1485]
print(space_xpos)
whos = []
for space_nr, x in enumerate(space_xpos):
    found = False
    for i, box in enumerate(r['rois']):
        if box[1] < x < box[3] and box[0] < 450 < box[2]:
            whos.append(i)
            found = True
            cv2.rectangle(overlay, (space_xpos[space_nr]-60, 400), (space_xpos[space_nr]+40, 40+450), (0, 0, 250), -1)
            cv2.rectangle(overlay, (space_xpos[space_nr]-60, 400), (space_xpos[space_nr]+40, 40+450), (0, 0, 0), 2)
            space_xpos[space_nr]= int(np.ceil(space_xpos[space_nr] + ((box[3] - box[1])/2)+box[1])/2)

            break
    if not found:
        cv2.rectangle(overlay, (space_xpos[space_nr]-60, 400), (space_xpos[space_nr]+40, 40+450), (0, 200, 0), -1)
        cv2.rectangle(overlay, (space_xpos[space_nr]-60, 400), (space_xpos[space_nr]+40, 40+450), (0, 0, 0), 2)
        #print("empty space!", space_nr)
print(space_xpos)
alpha = 0.4  # Transparency factor.
# Following line overlays transparent rectangle
# over the image
overlay = cv2.addWeighted(overlay, alpha, overlay, 1 - alpha, 0)
cv2.imshow("some", overlay)
cv2.waitKey(0)
# Visualize the detected objects.
# mrcnn.visualize.display_instances(image=overlay,
#                                 boxes=r['rois'][whos, :],
#                                 masks=r['masks'][:, :, whos],
#                                 class_ids=r['class_ids'][whos],
#                                 class_names=CLASS_NAMES,
#                                 scores=r['scores'][whos])
