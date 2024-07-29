import onnxruntime as rt
import cv2
import numpy as np
import time
import os



script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(script_dir, 'finetuned_effv2s_128x128.onnx')
runtime = rt.InferenceSession(model_dir)

with open(os.path.join(script_dir, 'classname.txt'), 'r') as f:
    classes = f.readlines()
    classnames = sorted([x.strip() for x in classes])

def fruit_classifier(img_array):
    if len(img_array.shape) == 2:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)

    elif img_array.shape[2] == 4:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
    
    test_image = cv2.resize(img_array, (128, 128))
    img_array = np.expand_dims(test_image, axis=0)
    
    # time_start = time.time()
    pred = runtime.run(['dense_5'], {'input':img_array})
    # time_end = time.time() - time_start

    fruit = classnames[np.argmax(pred)].replace('_', ' ').title()
    
    return {
        'fruit': fruit,
        # 'time_elapsed': str(time_end)
    }