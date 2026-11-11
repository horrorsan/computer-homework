import unittest
from pathlib import Path
import numpy as np
import student_tasks as st
try:
    import cv2
    CV_ERROR=None
except Exception as e:
    CV_ERROR=f'{type(e).__name__}: {e}'

@unittest.skipIf(CV_ERROR is not None,'OpenCV unavailable: '+str(CV_ERROR))
class TestT5(unittest.TestCase):
    def test_binary_hamming(self):
        # Controlled binary descriptors, not image-based accuracy evaluation.
        a=np.array([[0]*32,[255]*32],np.uint8)
        b=a[::-1].copy()
        m=st.match_orb_descriptors(a,b)
        self.assertEqual(len(m),2)
        self.assertEqual({(x.queryIdx,x.trainIdx)for x in m},{(0,1),(1,0)})
        self.assertTrue(all(x.distance==0 for x in m))
    def test_sort_and_empty(self):
        a=np.array([[0]*32,[255]*32],np.uint8);b=a.copy();b[0,0]=1
        m=st.match_orb_descriptors(a,b)
        self.assertEqual([x.distance for x in m],sorted(x.distance for x in m))
        self.assertEqual(st.match_orb_descriptors(None,None),[])

@unittest.skipIf(CV_ERROR is not None,'OpenCV unavailable: '+str(CV_ERROR))
class TestT6(unittest.TestCase):
    def test_known_synthetic_geometry(self):
        d=np.load(Path(__file__).resolve().parents[1]/'data'/'pose_fixture.npz')
        mask=d['mask'].copy();before=mask.copy()
        n,R,t,valid=st.recover_one_pose(d['E'],d['pts1'],d['pts2'],d['K'],mask)
        self.assertGreaterEqual(n,70);self.assertEqual(R.shape,(3,3));self.assertEqual(t.shape,(3,1))
        np.testing.assert_allclose(R,d['R21_truth'],atol=1e-4)
        self.assertAlmostEqual(float(np.linalg.norm(t)),1.,places=5)
        self.assertGreater(float(t.ravel()@d['t21_direction_truth']),.999)
        np.testing.assert_array_equal(mask,before)
        self.assertEqual(valid.shape,(len(d['pts1']),1))

if __name__=='__main__':unittest.main()
