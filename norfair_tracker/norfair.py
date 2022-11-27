# https://github.com/tryolabs/norfair/blob/master/demos/yolov5/src/demo.py

from typing import Callable, Optional, Union
from norfair.filter import OptimizedKalmanFilterFactory, FilterFactory
from norfair import Tracker, Detection
import numpy as np

class NorFairTracker:
    def __init__(
        self,
        distance_function: Union[str, Callable] = "frobenius",
        distance_threshold: float = 0.3,
        hit_counter_max: int = 15,
        initialization_delay: Optional[int] = None,
        pointwise_hit_counter_max: int = 4,
        detection_threshold: float = 0,
        filter_factory: FilterFactory = OptimizedKalmanFilterFactory(),
        past_detections_length: int = 4,
        reid_distance_function: Optional[Union[str, Callable]] = None,
        reid_distance_threshold: float = 0,
        reid_hit_counter_max: Optional[int] = None,
    ):
        self.tracker = Tracker(
            distance_function=distance_function,
            distance_threshold=distance_threshold,
            hit_counter_max=hit_counter_max,
            initialization_delay=initialization_delay,
            pointwise_hit_counter_max=pointwise_hit_counter_max,
            detection_threshold=detection_threshold,
            filter_factory=filter_factory,
            past_detections_length=past_detections_length,
            reid_distance_function=reid_distance_function,
            reid_distance_threshold=reid_distance_threshold,
            reid_hit_counter_max=reid_hit_counter_max,
        )
        
    
    def update(self, dets, _):
        xyxys = dets[:, 0:4].numpy()
        confs = dets[:, 4].numpy()
        category_ids = dets[:, 5].numpy()

        output_results = np.column_stack((xyxys, confs, category_ids))

        norfair_detections = []
        for ind in range(len(output_results)):
            bbox = np.array([[xyxys[ind][0].item(), xyxys[ind][1].item()],[xyxys[ind][2].item(), xyxys[ind][3].item()]])
            scores = np.array([confs[ind].item(), confs[ind].item()])
            category_id = int(category_ids[ind])
            norfair_detections.append(
                Detection(
                    bbox,
                    scores,
                    label=category_id,
                )
            )
        tracked_objects = self.tracker.update(norfair_detections)
        outputs = []
        for obj in tracked_objects:
            if not obj.live_points.any():
                continue
            
            points = obj.estimate[obj.live_points]
            points = points.astype(int)
            x1, y1, x2, y2 = points[0][0], points[0][1], points[1][0], points[1][1]
            track_id = obj.id
            cls_id = obj.label
            score =  obj.last_detection.scores[0] 
            outputs.append(np.array([x1, y1, x2, y2, track_id, cls_id, score]))
        if len(outputs) > 0:
            outputs = np.stack(outputs, axis=0)
        else:
            outputs = np.empty((0, 7))
        return outputs
        