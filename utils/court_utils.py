def get_court_layout(keypoints):
    """
    Extracts net and baseline positions from flat keypoint list.
    Args:
        keypoints (list): [x1, y1, x2, y2, ..., x14, y14]
    Returns:
        dict: Dictionary of court layout info
    """
    kps = [(int(keypoints[i]), int(keypoints[i+1])) for i in range(0, len(keypoints), 2)] #kps = [(x1,y1),(x2,y2),...,(x14,y14)]
    
    layout = {
    "top_baseline": min(kps[2][1], kps[3][1]),
    "bottom_baseline": max(kps[2][1], kps[3][1]),
    "net": int((kps[0][1] + kps[1][1]) / 2),
    "left": min(k[0] for k in kps),
    "right": max(k[0] for k in kps)} 

    return layout