def centre_of_bbox(bbox):
    x1,y1,x2,y2 = bbox
    cX = int((x1+x2)/2)
    cY = int((y1+y2)/2)

    return (cX,cY)

#Based on pythagoras theorem
def measure_dist(p1,p2):
    return((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)**0.5

def get_foot_position(bbox):
    """
    Get the foot position of the player based on their bounding box
    Args:
        bbox (tuple): Tuple containing the bounding box coordinates (x1, y1, x2, y2).
    Returns:
        tuple: Tuple containing the foot position (x, y).
    """
    x1,y1,x2,y2 = bbox

    return(int((x1+x2)/2),y2)

def get_closest_keypoint_index(point,keypoints,keypoint_index):
    """
    Get the index of the closest keypoint to a given point.
    Args:
        point (tuple): Tuple containing the coordinates of the point (x, y).
        keypoints (list): List of keypoints coordinates.
        keypoint_index (list): List of indices of keypoints.
    Returns:
        keypoint_idx (int): Index of the closest keypoint.
    """
    closest_dist = float('inf')
    keypoint_id = keypoint_index[0]
    for keypoint_idx in keypoint_index:
        keypoint = keypoints[keypoint_idx*2],keypoints[keypoint_idx*2+1]
        distance = abs(point[1]-keypoint[1])

        if distance < closest_dist:
            closest_dist = distance
            keypoint_id = keypoint_idx

    return keypoint_id

def get_height_of_bbox(bbox):
    """
    Gets the height of the bounding box of the player
    Returns:
        int: Height of the bounding box of the player
    """
    print(f"bbox:{bbox}")
    return bbox[3] - bbox[1] #max y - min y

def measure_xy_dist(p1,p2):
    """
    Gets the distance between 2 points
    Returns:
        int: x and y distance between 2 points
    """
    return abs(p2[0]-p1[0]),abs(p2[1]-p1[1])

def centre_of_bbox(bbox):
    return (int((bbox[0]+bbox[2])/2),int((bbox[1]+bbox[3])/2))