"""Provided infrastructure. Do not change this file for the assignment."""
import numpy as np

def points(a,dim):
    a=np.asarray(a,dtype=float)
    if a.ndim!=2 or a.shape[1]!=dim or len(a)==0 or not np.isfinite(a).all():
        raise ValueError(f'Expected non-empty finite (N,{dim}) array')
    return a

def matrix(a,shape,name):
    a=np.asarray(a,dtype=float)
    if a.shape!=shape or not np.isfinite(a).all():raise ValueError(f'Invalid {name}')
    return a

def translation(a):
    a=np.asarray(a,dtype=float)
    if a.shape not in [(3,),(3,1)]or not np.isfinite(a).all():raise ValueError('Expected t shape (3,) or (3,1)')
    return a.reshape(3)

def intrinsics(K):
    K=matrix(K,(3,3),'K')
    if K[0,0]<=0 or K[1,1]<=0 or not np.allclose(K[2],[0,0,1])or abs(K[0,1])+abs(K[1,0])>1e-12:
        raise ValueError('Need zero-skew pinhole K, positive focal lengths')
    return K

def bits(a,b):
    if not isinstance(a,str)or not isinstance(b,str)or len(a)==0 or len(a)!=len(b)or set(a+b)-{'0','1'}:
        raise ValueError('Need equal non-empty bit strings')

def matching_inputs(a,b):
    if a is None or b is None:return None
    a=np.asarray(a);b=np.asarray(b)
    if a.ndim!=2 or b.ndim!=2:raise ValueError('Descriptor arrays must be two-dimensional')
    if len(a)==0 or len(b)==0:return None
    if a.shape[1]!=32 or b.shape[1]!=32 or a.dtype!=np.uint8 or b.dtype!=np.uint8:
        raise ValueError('Expect default ORB uint8 descriptors shaped (N,32)')
    return a,b

def pose_inputs(E,p1,p2,K,mask):
    E=matrix(E,(3,3),'single E candidate');p1=points(p1,2);p2=points(p2,2);K=intrinsics(K)
    if p1.shape!=p2.shape or len(p1)<8:raise ValueError('Demo guard: need >=8 corresponding candidates')
    # This guard is not a statement of the theoretical minimum for all solvers.
    if mask is None:mask=np.ones((len(p1),1),dtype=np.uint8)
    else:
        mask=np.asarray(mask)
        if mask.size!=len(p1):raise ValueError('mask length mismatch')
        mask=(mask.reshape(-1,1)!=0).astype(np.uint8)
    return E,p1,p2,K,mask.copy()
