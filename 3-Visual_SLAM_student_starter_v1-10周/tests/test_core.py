import unittest
import numpy as np
import student_tasks as st

class TestT1(unittest.TestCase):
    def test_example(self):self.assertEqual(st.hamming_bits('101101','100001'),2)
    def test_zero_and_all(self):
        self.assertEqual(st.hamming_bits('0000','0000'),0)
        self.assertEqual(st.hamming_bits('0000','1111'),4)
    def test_bad_input(self):
        with self.assertRaises(ValueError):st.hamming_bits('10','101')

class TestT2(unittest.TestCase):
    def test_translation(self):
        np.testing.assert_allclose(st.world_to_camera([[5,3,4]],np.eye(3),[-2,-1,0]),[[3,2,4]])
    def test_rows_and_rotation(self):
        R=np.array([[0,-1,0],[1,0,0],[0,0,1]],float)
        np.testing.assert_allclose(st.world_to_camera([[1,0,2],[0,1,3]],R,[.1,.2,0]),[[.1,1.2,2],[-.9,.2,3]])

class TestT3(unittest.TestCase):
    K=np.array([[400,0,320],[0,400,240],[0,0,1]],float)
    def test_reading_example(self):np.testing.assert_allclose(st.project_pinhole([[.5,.2,2]],self.K),[[420,280]])
    def test_depth_and_center(self):np.testing.assert_allclose(st.project_pinhole([[.5,.2,4],[0,0,3]],self.K),[[370,260],[320,240]])
    def test_invalid_depth(self):
        with self.assertRaises(ValueError):st.project_pinhole([[1,1,0]],self.K)

class TestT4(unittest.TestCase):
    def test_one_point(self):
        d=st.reprojection_scores([[320,240]],[[323,238]])
        np.testing.assert_allclose(d['residuals'],[[-3,2]])
        np.testing.assert_allclose(d['per_point_squared'],[13])
        self.assertAlmostEqual(d['sse'],13);self.assertAlmostEqual(d['pixel_rmse'],np.sqrt(13))
    def test_multi_point_rmse(self):
        d=st.reprojection_scores([[0,0],[0,0]],[[3,4],[0,0]])
        self.assertAlmostEqual(d['sse'],25);self.assertAlmostEqual(d['pixel_rmse'],np.sqrt(12.5))
    def test_shape_error(self):
        with self.assertRaises(ValueError):st.reprojection_scores([[0,0]],[[0,0],[1,1]])

if __name__=='__main__':unittest.main()
