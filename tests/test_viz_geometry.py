import unittest

from ada import Assembly, Beam, Part, Plate
from ada.param_models.basic_module import SimpleStru


class VisualizeTests(unittest.TestCase):
    def test_beams_viz(self):
        bm1 = Beam("bm1", n1=[0, 0, 0], n2=[2, 0, 0], sec="IPE220", colour="red")
        bm2 = Beam("bm2", n1=[0, 0, 1], n2=[2, 0, 1], sec="HP220x10", colour="blue")
        bm3 = Beam("bm3", n1=[0, 0, 2], n2=[2, 0, 2], sec="BG800x400x20x40", colour="green")
        bm4 = Beam("bm4", n1=[0, 0, 3], n2=[2, 0, 3], sec="CIRC200", colour="green")
        bm5 = Beam("bm5", n1=[0, 0, 4], n2=[2, 0, 4], sec="TUB200x10", colour="green")

        bm1._repr_html_()
        bm2._repr_html_()
        bm3._repr_html_()
        bm4._repr_html_()
        bm5._repr_html_()

    def test_viz(self):
        a = Assembly("my_test_assembly")
        a.add_beam(Beam("bm1", n1=[0, 0, 0], n2=[2, 0, 0], sec="IPE220", colour="red"))
        a.add_beam(Beam("bm2", n1=[0, 0, 1], n2=[2, 0, 1], sec="HP220x10", colour="blue"))
        a.add_beam(Beam("bm3", n1=[0, 0, 2], n2=[2, 0, 2], sec="BG800x400x20x40", colour="green"))
        a.add_beam(Beam("bm4", n1=[0, 0, 3], n2=[2, 0, 3], sec="CIRC200", colour="green"))
        a.add_beam(Beam("bm5", n1=[0, 0, 4], n2=[2, 0, 4], sec="TUB200x10", colour="green"))
        a.add_plate(
            Plate(
                "pl1",
                [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)],
                0.01,
                use3dnodes=True,
            )
        )
        a._repr_html_()

    def test_fem(self):
        a = Assembly("MyAssembly") / (Part("MyPart") / Beam("Bm", (0, 0, 0), (1, 0, 0), "IPE300"))
        a.gmsh.mesh()

        a._repr_html_()
        a._renderer.toggle_mesh_visibility()

    def test_module(self):
        a = Assembly("ParametricSite") / SimpleStru("ParametricModel")
        a.gmsh.mesh()

        a._repr_html_()
        a._renderer.toggle_mesh_visibility()

    def test_module2(self):
        param_model = SimpleStru("ParametricModel")
        param_model.gmsh.mesh(size=0.1, max_dim=2)
        param_model.add_bcs()
        a = Assembly("ParametricSite")
        a.add_part(param_model)
        a._repr_html_()
        # a._renderer.toggle_geom_visibility()
        a._renderer.toggle_mesh_visibility()


if __name__ == "__main__":
    unittest.main()
