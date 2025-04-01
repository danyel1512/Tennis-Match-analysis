from ultralytics import YOLO
import cv2 as cv
import pickle
from utils import centre_of_bbox,measure_dist

class TrackPlayer:
    def __init__(self,model_path):
        self.model = YOLO(model_path)
        self.role_history = {} #Keeps track of roles per track ID

    #Assign roles in the video based on proximity of the keypoints
    def assign_and_filter_players(self,court_keypoints,player_detections):
        player_detection = player_detections[0]
        chosen_role = self.choose_players(court_keypoints,player_detection)
        filtered_players_detection = []

        for player_dict in player_detections:
            filtered_players_dict = {track_id:bbox for track_id,bbox in player_dict.items() if track_id in chosen_role}
            filtered_players_detection.append(filtered_players_dict)

        return filtered_players_detection

    def choose_players(self,court_keypoints,player_dict):
        distances = []
        for track_id, bbox in player_dict.items():
            #Get the center of the bbox
            bbox_centre = centre_of_bbox(bbox)

            min_dist = float('inf')
            #Iterate through each court keypoint
            for i in range(0,len(court_keypoints),2):
                court_keypoint = (court_keypoints[i],court_keypoints[i+1])
                dist = measure_dist(bbox_centre,court_keypoint)

                if dist < min_dist:
                    min_dist = dist
            distances.append((track_id,min_dist))

        #sort distance in ascending order
        distances.sort(key=lambda x:x[1])
        print(f"Distances: {distances}")
        chosen_roles = [distances[0][0],distances[1][0]]
        return chosen_roles
    
    #Detect and track the players in the video
    def detect_frames(self,frames,read_from_stub=False,stub_path=None,court_layout=None):
        """
        Detects and tracks players in the video
        Args:
            frames (list): List of frames as an array
            read_from_stub (bool): If True, put data into a stub. Default = False
            stub_path (str): path to save the output so that we dont have to run the detector again

        Returns:
            player_detection (list): List of dictionaries with player id and bounding box coordinates
        """
        player_detections = []

        if read_from_stub and stub_path is not None:
            with open(stub_path, 'rb') as f:
                player_detections = pickle.load(f)
            return player_detections
     
        for frame in frames:
            player_dict = self.detect_frame(frame,court_layout)
            player_detections.append(player_dict)

        if stub_path is not None:
            with open(stub_path,'wb') as f:
                pickle.dump(player_detections,f)
        
        return player_detections

    #Detect and track the players in the frame
    def detect_frame(self,frame,court_layout=None):
        """
        Detects and tracks players in the frame
        Args:
            frame (array): Input frame
            court_layout (dict): Dictionary of court description

        Returns:
            player_dict (dict): Dictionary with player id and bounding box coordinates
        """
        results = self.model.track(frame,persist=True)[0] #Runs tracking on the input frame
        id_name_dict = results.names
        player_dict = {} #Dictionary to store player id and bounding box coordinates

        for box in results.boxes:
            track_id = int(box.id.tolist()[0]) #Add track id of each box to the dictionary
            result = box.xyxy.tolist()[0] #Add bounding box coordinates to the dictionary
            object_cls_id = box.cls.tolist()[0] #Add object class id to the dictionary
            object_cls_name = id_name_dict[object_cls_id] #Get the object class name

            if object_cls_name == "person":
                x1,y1,x2,y2 = result
                player_dict[track_id] = result
        
        return player_dict
    
    def draw_bounding_box(self,video_frames,player_detections):
        """
        Draws bounding box around the players in the video
        Args:
            video_frames (list): List of frames as an array
            player_detections (list): List of dictionaries with player id and bounding box coordinates
        Returns:
            output_video_frames (list): List of frames with bounding box around the players
        """
        output_video_frames = []
        for frame, player_dict in zip(video_frames, player_detections):
            # Draw Bounding Boxes
            for track_id, bbox in player_dict.items():
                x1, y1, x2, y2 = bbox
                cv.putText(frame, f"Player ID: {track_id}",(int(bbox[0]),int(bbox[1] -10)),cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            output_video_frames.append(frame)

        return output_video_frames
        
        
  