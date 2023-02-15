import torch

def load_model():
    try:
        model = None
        model = torch.hub.load('ultralytics/yolov5', 'yolov5m')
    except Exception as exception:
        print("Error occured while loading the model", exception.args)
    finally:
        return model