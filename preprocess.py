import os
import pygmsh
import math


def meshing(r_out=0.2, r_in=0.15, bar_width=0.02, center_x=0, center_y=0, mesh_size=0.01):
    end = (r_out + r_in) / 2
    angle = math.pi / 4
    coeff = math.cos(angle)
    with pygmsh.occ.Geometry() as geom:
        geom.characteristic_length_max = mesh_size
        outer = geom.add_disk([center_x, center_y], r_out)
        inner = geom.add_disk([center_x, center_y], r_in)
        bar_1 = geom.add_polygon([
            [-end, bar_width / 2],
            [-end, -bar_width / 2],
            [end, -bar_width / 2],
            [end, bar_width / 2]
        ])
        bar_2 = geom.add_polygon([
            [-bar_width / 2, -end],
            [bar_width / 2, -end],
            [bar_width / 2, end],
            [-bar_width / 2, end]
        ])
        bar_3 = geom.add_polygon([
            [(end+bar_width/2)*coeff, (end-bar_width/2)*coeff],
            [(end-bar_width/2)*coeff, (end+bar_width/2)*coeff],
            [-(end+bar_width/2)*coeff, -(end-bar_width/2)*coeff],
            [-(end-bar_width/2)*coeff, -(end+bar_width/2)*coeff]
        ])
        bar_4 = geom.add_polygon([
            [(end - bar_width / 2) * coeff, -(end + bar_width / 2) * coeff],
            [(end + bar_width / 2) * coeff, -(end - bar_width / 2) * coeff],
            [-(end - bar_width / 2) * coeff, (end + bar_width / 2) * coeff],
            [-(end + bar_width / 2) * coeff, (end - bar_width / 2) * coeff]
        ])

        geom.boolean_union([geom.boolean_difference(outer, inner),
                            bar_1, bar_2, bar_3, bar_4])
        mesh = geom.generate_mesh()
    return mesh


def write_files(mesh, folder, r_out=0.2, E=1.0e8, nu=0.3, load=20.0e3):
    mesh_pts = mesh.points
    elements = mesh.cells_dict['triangle']

    os.makedirs(folder, exist_ok=True)

    # Write nodes.txt
    # fix bottom
    with open(f'{folder}/nodes.txt', 'w') as f_nodes:
        for i, point in enumerate(mesh_pts):
            if point[1] < -r_out + 0.02:  # == min(mesh_pts[:, 1]):
                bc_x, bc_y = -1, -1
            else:
                bc_x, bc_y = 0, 0
            f_nodes.write(f"{i:4} {point[0]:8.4f} {point[1]:8.4f}  {bc_x:4}  {bc_y:4} \n")

    # Write eles.txt
    with open(f'{folder}/eles.txt', 'w') as f_eles:
        for i, element in enumerate(elements):
            f_eles.write(f"{i:4}   3   0  {element[0]:4} {element[1]:4}  {element[2]:4} \n")

    # Write mater.txt
    with open(f'{folder}/mater.txt', 'w') as f_mater:
        f_mater.write(f"{E:8.4f} {nu:8.4f}")

    # Write loads.txt
    with open(f'{folder}/loads.txt', 'w') as f_loads:
        for i, point in enumerate(mesh_pts):
            if point[1] > r_out - 0.02:
                f_loads.write(f"{i:4} {0.0:8.4f} {load:8.4f} \n")
