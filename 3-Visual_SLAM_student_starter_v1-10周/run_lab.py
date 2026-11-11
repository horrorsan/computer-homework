"""Provided experiment driver. Students edit student_tasks.py, not this file."""
from pathlib import Path
import argparse,json,csv
import numpy as np
import student_tasks as st
BASE=Path(__file__).resolve().parent

def save_json(path,record):
    def convert(x):
        if isinstance(x,np.ndarray):return x.tolist()
        if isinstance(x,np.generic):return x.item()
        raise TypeError(type(x).__name__)
    path.write_text(json.dumps(record,ensure_ascii=False,indent=2,default=convert),encoding='utf-8')

def run_core(out):
    d=np.load(BASE/'data'/'scoring_fixture.npz')
    result={'data_type':'synthetic teaching data, NOT real SLAM accuracy','hamming_reading_example':st.hamming_bits('101101','100001'),'candidates':{}}
    rows=[];predictions={}
    for tag in ['A','B']:
        P_c=st.world_to_camera(d['P_w'],d['R_cw'],d['t_'+tag])
        pred=st.project_pinhole(P_c,d['K']);scores=st.reprojection_scores(d['observed'],pred);predictions[tag]=pred
        result['candidates'][tag]={'sse_pixel_squared':scores['sse'],'pointwise_pixel_rmse':scores['pixel_rmse']}
        for j,(obs,p,r,sq)in enumerate(zip(d['observed'],pred,scores['residuals'],scores['per_point_squared'])):
            rows.append([tag,j,*obs,*p,*r,sq])
    with (out/'residuals.csv').open('w',newline='',encoding='utf-8-sig')as f:
        w=csv.writer(f);w.writerow(['candidate','point','u_observed','v_observed','u_predicted','v_predicted','e_u','e_v','squared_pixel_error']);w.writerows(rows)
    save_json(out/'core_report.json',result)
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,axes=plt.subplots(1,2,figsize=(10,4))
        for ax,(tag,pred)in zip(axes,predictions.items()):
            ax.scatter(*d['observed'].T,label='Observed',c='navy');ax.scatter(*pred.T,label='Predicted',marker='x',c='crimson')
            for a,b in zip(d['observed'],pred):ax.plot([a[0],b[0]],[a[1],b[1]],c='goldenrod')
            ax.set_title(f"{tag}: SSE={result['candidates'][tag]['sse_pixel_squared']:.2f} pixel^2");ax.set_xlabel('u [pixel]');ax.set_ylabel('v [pixel]');ax.axis('equal');ax.invert_yaxis();ax.legend()
        fig.suptitle('Synthetic teaching observations: scoring only, not BA optimization');fig.tight_layout();fig.savefig(out/'reprojection.png',dpi=180);plt.close(fig)
    except ImportError:print('Matplotlib unavailable; JSON and CSV were still written')
    return result

def pack_pose(count,R,t,valid,label):
    return {'data_type':label,'valid_count':int(count),'R21':R,'t21_direction':t.ravel(),'translation_norm':float(np.linalg.norm(t)),'valid_mask':valid.ravel(),'convention':'P2=R21*P1+t21; NOT camera world position','scale':'normalized translation direction; NOT measured meters'}

def run_pose(out):
    d=np.load(BASE/'data'/'pose_fixture.npz')
    values=st.recover_one_pose(d['E'],d['pts1'],d['pts2'],d['K'],d['mask'])
    if values[0]<8:raise ValueError('Too few valid points in the known synthetic pose fixture')
    result=pack_pose(*values,'synthetic correspondences with known essential-matrix candidate')
    save_json(out/'pose_report.json',result);return result

def estimate_from_matches(p1,p2,K):
    import cv2
    if len(p1)<8:raise ValueError('Demo input guard: fewer than 8 matches; not a universal solver minimum')
    E,mask=cv2.findEssentialMat(p1,p2,K,method=cv2.RANSAC,prob=.999,threshold=1.)
    if E is None or mask is None:raise ValueError('Essential matrix estimation failed')
    if E.shape[1]!=3 or E.shape[0]%3:raise ValueError('Unexpected essential-matrix shape')
    best=None
    for i in range(0,len(E),3):
        current=st.recover_one_pose(E[i:i+3],p1,p2,K,mask.copy())
        if best is None or current[0]>best[0]:best=current
    if best[0]<8:raise ValueError('Too few accepted points; inspect inputs and scene/motion')
    return best,int(np.count_nonzero(mask))

def run_matching(out):
    d=np.load(BASE/'data'/'matching_fixture.npz');ms=st.match_orb_descriptors(d['des1'],d['des2'])
    p1=np.float64([d['pts1'][m.queryIdx]for m in ms]);p2=np.float64([d['pts2'][m.trainIdx]for m in ms])
    values,rin=estimate_from_matches(p1,p2,d['K'])
    result=pack_pose(*values,'synthetic binary descriptors, NOT extracted from real photos')
    result.update(candidate_count=len(ms),ransac_inliers=rin)
    save_json(out/'matching_report.json',result)
    return result

def run_images(a,out):
    import cv2
    if not a.undistorted:raise ValueError('Confirm pre-undistorted input with --undistorted')
    if not a.image1 or not a.image2 or any(getattr(a,k)is None for k in ['fx','fy','cx','cy']):raise ValueError('Need image paths and actual fx/fy/cx/cy')
    im1=cv2.imread(a.image1,0);im2=cv2.imread(a.image2,0)
    if im1 is None or im2 is None or im1.shape!=im2.shape:raise ValueError('Image read/size mismatch')
    if a.fx<=0 or a.fy<=0:raise ValueError('Positive focal lengths required')
    K=np.array([[a.fx,0,a.cx],[0,a.fy,a.cy],[0,0,1.]])
    orb=cv2.ORB_create(nfeatures=500);k1,d1=orb.detectAndCompute(im1,None);k2,d2=orb.detectAndCompute(im2,None)
    ms=st.match_orb_descriptors(d1,d2)
    p1=np.float64([k1[m.queryIdx].pt for m in ms]);p2=np.float64([k2[m.trainIdx].pt for m in ms])
    values,rin=estimate_from_matches(p1,p2,K);n,R,t,valid=values
    result=pack_pose(*values,'user-supplied real images; no independent accuracy claim')
    result.update(candidate_count=len(ms),ransac_inliers=rin,keypoints=[len(k1),len(k2)])
    save_json(out/'images_report.json',result)
    accepted=[m for m,ok in zip(ms,valid.ravel())if ok]
    cv2.imwrite(str(out/'candidates.jpg'),cv2.drawMatches(im1,k1,im2,k2,ms[:50],None,flags=2))
    cv2.imwrite(str(out/'accepted.jpg'),cv2.drawMatches(im1,k1,im2,k2,accepted[:50],None,flags=2))
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--stage',choices=['core','pose','matching','all','images'],default='core');ap.add_argument('--out',default='outputs')
    ap.add_argument('--image1');ap.add_argument('--image2');ap.add_argument('--undistorted',action='store_true')
    for k in ['fx','fy','cx','cy']:ap.add_argument('--'+k,type=float)
    a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    for name,fn in [('core',run_core),('pose',run_pose),('matching',run_matching)]:
        if a.stage in [name,'all']:
            result=fn(out);print(name,': completed; inspect reports and explain units')
    if a.stage=='images':run_images(a,out);print('images: completed; no independent accuracy claim')
if __name__=='__main__':
    try:main()
    except NotImplementedError as e:raise SystemExit('Incomplete student task: '+str(e))
