import unittest
import numpy as np
import student_tasks as st

class TestOptional(unittest.TestCase):
    def test_T7_inverse(self):
        R=np.array([[0,-1,0],[1,0,0],[0,0,1]],float);t=np.array([2.,1.,0.])
        np.testing.assert_allclose(st.camera_center_in_first(R,t),[-1,2,0])
    def test_T8_scale(self):
        K=np.array([[400,0,320],[0,400,240],[0,0,1]],float)
        a,b=st.scale_invariance_pixels([[.2,.1,2],[-.3,.4,4]],np.eye(3),[.1,0,.2],K,3)
        np.testing.assert_allclose(a,b,atol=1e-10)

if __name__=='__main__':unittest.main()
