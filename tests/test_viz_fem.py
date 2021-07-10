import unittest

from ada import Assembly, Beam, Part
from ada.fem._visualize import get_edges_from_fem


class FemBeam(unittest.TestCase):
    def test_beam_as_edges(self):
        a = Assembly() / (Part("BeamFEM") / Beam("bm1", n1=[0, 0, 0], n2=[2, 0, 0], sec="IPE220", colour="red"))
        pfem = a.get_by_name("BeamFEM")
        pfem.gmsh.mesh(0.1)
        assert len(pfem.fem.elements) == 20
        res = get_edges_from_fem(pfem.fem)
        print(res)

    def test_beam_as_faces(self):
        a = Assembly() / (Part("BeamFEM") / Beam("bm1", n1=[0, 0, 0], n2=[2, 0, 0], sec="IPE220", colour="red"))
        pfem = a.get_by_name("BeamFEM")
        pfem.gmsh.mesh(0.1)
        assert len(pfem.fem.elements) == 20
        res = get_edges_from_fem(pfem.fem)
        print(res)


if __name__ == "__main__":
    unittest.main()
