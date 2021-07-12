from dataclasses import dataclass

import numpy as np
from pythreejs import Group

from ada.base.threejs_geom import edges_to_mesh, faces_to_mesh, vertices_to_mesh

from . import FEM


@dataclass
class ViewItem:
    fem: FEM
    vertices: np.array
    edges: np.array
    faces: np.array


class BBox:
    max: list
    min: list
    center: list


def fem_to_mesh(
    fem: FEM, face_colors=None, vertex_colors=(8, 8, 8), edge_color=(8, 8, 8), edge_width=1, vertex_width=1
):
    from ada.base.threejs_geom import faces_to_mesh

    vertices, faces, edges = get_vertices_from_fem(fem), get_faces_from_fem(fem), get_edges_from_fem(fem)

    name = fem.name

    vertices_m = vertices_to_mesh(f"{name}_vertices", vertices, vertex_colors, vertex_width)
    edges_m = edges_to_mesh(f"{name}_edges", vertices, edges, edge_color=edge_color, linewidth=edge_width)
    faces_mesh = faces_to_mesh(f"{name}_faces", vertices, faces, colors=face_colors)

    return vertices_m, edges_m, faces_mesh


class FemRenderer:
    def __init__(self):
        self._view_items = []
        self._meshes = []

        # the group of 3d and 2d objects to render
        self._displayed_pickable_objects = Group()

    def add_fem(self, fem: FEM):
        vertices, faces, edges = get_vertices_from_fem(fem), get_faces_from_fem(fem), get_edges_from_fem(fem)
        self._view_items.append(ViewItem(fem, vertices, edges, faces))

    def to_mesh(self):
        for vt in self._view_items:
            self._view_to_mesh(vt)

    def _view_to_mesh(
        self, vt, face_colors=None, vertex_colors=(8, 8, 8), edge_color=(8, 8, 8), edge_width=1, vertex_width=1
    ):
        """

        :param vt:
        :type vt: ViewItem
        :return:
        """
        fem = vt.fem
        vertices = vt.vertices
        edges = vt.edges
        faces = vt.faces

        vertices_m = vertices_to_mesh(f"{fem.name}_vertices", vertices, vertex_colors, vertex_width)
        edges_m = edges_to_mesh(f"{fem.name}_edges", vertices, edges, edge_color=edge_color, linewidth=edge_width)
        face_geom, faces_m = faces_to_mesh(f"{fem.name}_faces", vertices, faces, colors=face_colors)

        return vertices_m, edges_m, faces_m

    def get_bounding_box(self):
        bounds = np.asarray([get_bounding_box(m) for m in self._meshes], dtype="float32")
        mi, ma = np.min(bounds, 0), np.max(bounds, 0)
        center = (mi + ma) / 2
        return mi, ma, center


def get_edges_and_faces_from_meshio(mesh):
    """

    :param mesh:
    :type mesh: meshio.Mesh
    :return:
    """
    from ada.fem._shapes import ElemShapes
    from ada.fem.io.io_meshio import meshio_to_ada_type

    edges = []
    faces = []
    for cell_block in mesh.cells:
        el_type = meshio_to_ada_type[cell_block.type]
        for elem in cell_block.data:
            res = ElemShapes(el_type, elem)
            edges += res.edges
            if res.type in res.beam:
                continue
            faces += res.faces
    return edges, faces


def get_faces_from_fem(fem, convert_bm_to_shell=False):
    """

    :param fem:
    :param convert_bm_to_shell: Converts Beam elements to a shell element equivalent
    :type fem: ada.fem.FEM
    :return:
    :rtype: list
    """
    from ._shapes import ElemShapes

    ids = []
    for el in fem.elements.elements:
        if ElemShapes.is_beam_elem(el):
            continue
        for f in el.shape.faces:
            # Convert to indices, not id
            ids += [[int(e.id - 1) for e in f]]
    return ids


def get_edges_from_fem(fem):
    """

    :param fem:
    :type fem: ada.fem.FEM
    :return:
    :rtype: list
    """
    ids = []
    for el in fem.elements.elements:
        for f in el.shape.edges_seq:
            # Convert to indices, not id
            ids += [[int(el.nodes[e].id - 1) for e in f]]
    return ids


def get_faces_for_bm_elem(elem):
    """

    :param elem:
    :type elem: ada.fem.Elem
    :return:
    """

    # if ElemShapes.beam


def get_vertices_from_fem(fem):
    """

    :param fem:
    :type fem: ada.fem.FEM
    :return:
    """

    return np.asarray([n.p for n in fem.nodes.nodes], dtype="float32")


def get_bounding_box(vertices):
    return np.min(vertices, 0), np.max(vertices, 0)


def magnitude(u):
    return np.sqrt(u[0] ** 2 + u[1] ** 2 + u[2] ** 2)
