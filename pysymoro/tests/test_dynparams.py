#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Unit test module for Screw6 class."""


import unittest

from sympy import eye, var
from sympy import Matrix

from pysymoro import screw
from pysymoro import screw6
from symoroutils import tools

from pysymoro.dynparams import DynParams


class TestDynParams(unittest.TestCase):
    """Unit test for Screw6 class."""
    def setUp(self):
        link = 33
        # setup an instance of DynParams
        self.data = DynParams(link)
        # setup data to compare against
        self.link = link
        # inertia matrix terms
        self.xx = var('XX33')
        self.xy = var('XY33')
        self.xz = var('XZ33')
        self.yy = var('YY33')
        self.yz = var('YZ33')
        self.zz = var('ZZ33')
        # mass tensor terms
        self.msx = var('MX33')
        self.msy = var('MY33')
        self.msz = var('MZ33')
        # link mass
        self.mass = var('M33')
        # rotor inertia term
        self.ia = var('IA33')
        # coulomb friction parameter
        self.frc = var('FS33') 
        # viscous friction parameter
        self.frv = var('FV33')
        # external forces and moments
        self.fx_ext = var('FX33')
        self.fy_ext = var('FY33')
        self.fz_ext = var('FZ33')
        self.mx_ext = var('CX33')
        self.my_ext = var('CY33')
        self.mz_ext = var('CZ33')
        # setup matrix terms to compare against
        self.inertia = Matrix([
            [self.xx, self.xy, self.xz],
            [self.xy, self.yy, self.yz],
            [self.xz, self.yz, self.zz]
        ])
        self.mass_tensor = Matrix([self.msx, self.msy, self.msz])
        m_eye = self.mass * eye(3)
        ms_skew = tools.skew(self.mass_tensor)
        self.spatial_inertia = screw6.Screw6(
            tl=m_eye, tr=ms_skew.transpose(),
            bl=ms_skew, br=self.inertia
        )
        self.wrench = screw.Screw(
            lin=Matrix([self.fx_ext, self.fy_ext, self.fz_ext]),
            ang=Matrix([self.mx_ext, self.my_ext, self.mz_ext])
        )

    def test_init(self):
        """Test constructor."""
        # test instance type
        self.assertIsInstance(DynParams(self.link), DynParams)

    def test_inertia(self):
        """Test get of inertia()"""
        # test get
        self.assertEqual(self.data.inertia, self.inertia)

    def test_mass_tensor(self):
        """Test get of mass_tensor()"""
        # test get
        self.assertEqual(self.data.mass_tensor, self.mass_tensor)

    def test_spatial_inertia(self):
        """Test get of spatial_inertia()"""
        # test get
        self.assertEqual(self.data.spatial_inertia, self.spatial_inertia)

    def test_wrench(self):
        """Test get of wrench()"""
        # test get
        self.assertEqual(self.data.wrench, self.wrench)

    def test_force(self):
        """Test get and set of force()"""
        # test get
        self.assertEqual(self.data.force, self.wrench.lin)
    
    def test_moment(self):
        """Test get of moment()"""
        # test get
        self.assertEqual(self.data.moment, self.wrench.ang)


def run_tests():
    """Load and run the unittests"""
    unit_suite = unittest.TestLoader().loadTestsFromTestCase(
        TestDynParams
    )
    unittest.TextTestRunner(verbosity=2).run(unit_suite)


def main():
    """Main function."""
    run_tests()


if __name__ == '__main__':
    main()


