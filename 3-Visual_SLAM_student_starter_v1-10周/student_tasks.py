"""Student tasks. Edit only the TODO bodies in this file.
Conventions: row-wise points (N,3); P_c=R_cw P_w+t_cw; zero-skew pinhole K.
T1--T4 require only NumPy. T5--T6 additionally require OpenCV.
"""
import numpy as np
from provided_validation import points,matrix,translation,intrinsics,bits,matching_inputs,pose_inputs

def hamming_bits(a,b):
    """T1: equal-length bit strings -> Python int; unit = differing bits."""
    bits(a,b)
    count = 0
    for x,y in zip(a,b):
        if x != y:
            count += 1
    return count

def world_to_camera(P_w,R_cw,t_cw):
    """T2: (N,3), (3,3), (3,) -> camera points (N,3), same length unit.
    Remember: formula uses column vectors; the array stores points by ROW.
    """
    P_w=points(P_w,3);R_cw=matrix(R_cw,(3,3),'R_cw');t_cw=translation(t_cw)
    
    return P_w @ R_cw.T + t_cw

def project_pinhole(P_c,K):
    """T3: camera points (N,3), K (3,3) -> pixels (N,2).
    No distortion. All input depths must be positive; never divide pixel origins by Z.
    """
    P_c=points(P_c,3);K=intrinsics(K)
    if np.any(P_c[:,2]<=0):raise ValueError('All depths must be positive')
    X = P_c[:, 0]
    Y = P_c[:, 1]
    Z = P_c[:, 2]

    fx = K[0, 0]
    fy = K[1, 1]
    cx = K[0, 2]
    cy = K[1, 2]

    u = fx * X / Z + cx
    v = fy * Y / Z + cy

    return np.column_stack((u, v))

def reprojection_scores(observed,predicted):
    """T4: (N,2), (N,2) -> dictionary with exactly these meanings:
    residuals: observed-predicted, shape (N,2), pixels
    per_point_squared: du^2+dv^2 per point, shape (N,), pixel^2
    sse: sum of per-point squared errors, Python float, pixel^2
    pixel_rmse: sqrt(sse / number_of_points), float, pixels
    This is point-wise Euclidean RMSE, NOT sqrt(sse/(2*N)).
    """
    observed=points(observed,2);predicted=points(predicted,2)
    if observed.shape!=predicted.shape:raise ValueError('Pixel arrays must have equal shapes')

    residuals = observed - predicted
    per_point_squared = np.sum(residuals ** 2, axis=1)
    sse = float(np.sum(per_point_squared))

    n = observed.shape[0]
    pixel_rmse = float(np.sqrt(sse / n)) if n > 0 else 0.0

    return {
        'residuals': residuals,
        'per_point_squared': per_point_squared,
        'sse': sse,
        'pixel_rmse': pixel_rmse,
    }

def match_orb_descriptors(des1,des2):
    """T5: default ORB descriptors -> distance-sorted list of cv2.DMatch.
    WTA_K=2; Hamming norm; crossCheck=True. None/empty -> [] (already handled).
    """
    checked=matching_inputs(des1,des2)
    if checked is None:return []
    des1,des2=checked
    import cv2

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda m: m.distance)
    return matches

def recover_one_pose(E,pts1,pts2,K,mask=None):
    """T6: one (3,3) essential-matrix candidate -> OpenCV result tuple.
    Return: valid_count, R21, t21, valid_mask.
    Convention: P2=R21 P1+t21, normalized t direction, NOT meters.
    OpenCV's chirality test rejects some configurations; it does not prove truth.
    """
    E,pts1,pts2,K,mask=pose_inputs(E,pts1,pts2,K,mask)
    import cv2

    mask_copy = None if mask is None else np.array(mask, copy=True)

    if mask_copy is None:
        valid_count, R21, t21, valid_mask = cv2.recoverPose(
            E, pts1, pts2, K
        )
    else:
        valid_count, R21, t21, valid_mask = cv2.recoverPose(
            E, pts1, pts2, K, mask=mask_copy
        )

    return valid_count, R21, t21, valid_mask
    
def camera_center_in_first(R21,t21):
    """T7 OPTIONAL: inverse-transform camera-2 center in camera-1 coordinates.
    Its scale is still unknown when t21 is only a normalized direction.
    """
    R21=matrix(R21,(3,3),'R21');t21=translation(t21)
    
    return -R21.T @ t21

def scale_invariance_pixels(P_w,R_cw,t_cw,K,scale):
    """T8 OPTIONAL: return (original_pixels, scaled_pixels).
    Scale ALL world points AND the transformation translation by the same factor.
    Rotation and intrinsics stay unchanged. Reuse T2/T3.
    """
    if not np.isscalar(scale)or not np.isfinite(scale)or scale<=0:raise ValueError('scale must be positive')
    P_w=points(P_w,3);R_cw=matrix(R_cw,(3,3),'R_cw');t_cw=translation(t_cw);K=intrinsics(K)

    original_pixels = project_pinhole(
        world_to_camera(P_w, R_cw, t_cw),
        K
    )

    scaled_pixels = project_pinhole(
        world_to_camera(P_w * scale, R_cw, t_cw * scale),
        K
    )

    return original_pixels, scaled_pixels
