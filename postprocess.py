import solidspy.preprocesor as pre
import solidspy.postprocesor as post
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from scipy.spatial import distance
import math


def plot_results(folder, disp, strain, stress):
    nodes, _, elements, _ = pre.readin(folder=folder + '/')
    tri = post.mesh2tri(nodes, elements)

    # S_xx
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    c = ax.tricontourf(tri, stress[:, 0], levels=12)
    cbar = fig.colorbar(c, orientation="horizontal")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(r"$\sigma_{xx}$ (MPa)", fontsize=18, labelpad=8)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.axis("image")
    plt.show()

    # S_yy
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    c = ax.tricontourf(tri, stress[:, 1], levels=12)
    cbar = fig.colorbar(c, orientation="horizontal")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(r"$\sigma_{yy}$ (MPa)", fontsize=18, labelpad=8)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.axis("image")
    plt.show()

    # gamma_xy
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    c = ax.tricontourf(tri, stress[:, 2], levels=12)
    cbar = fig.colorbar(c, orientation="horizontal")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(r"$\tau_{xy}$ (MPa)", fontsize=18, labelpad=8)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.axis("image")
    plt.show()

    # e_xx
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    c = ax.tricontourf(tri, strain[:, 0], levels=12)
    cbar = fig.colorbar(c, orientation="horizontal")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(r"$\epsilon_{xx}$", fontsize=18, labelpad=8)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.axis("image")
    plt.show()

    # e_yy
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    c = ax.tricontourf(tri, strain[:, 1], levels=12)
    cbar = fig.colorbar(c, orientation="horizontal")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(r"$\epsilon_{yy}$", fontsize=18, labelpad=8)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.axis("image")
    plt.show()

    # gamma_xy
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    c = ax.tricontourf(tri, strain[:, 2], levels=12)
    cbar = fig.colorbar(c, orientation="horizontal")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(r"$\gamma_{xy}$", fontsize=18, labelpad=8)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.axis("image")
    plt.show()

    # d_x
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    c = ax.tricontourf(tri, disp[:, 0], levels=12)
    cbar = fig.colorbar(c, orientation="horizontal")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(r"$d_x$", fontsize=18, labelpad=8)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.axis("image")
    plt.show()

    # e_yy
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    c = ax.tricontourf(tri, disp[:, 1], levels=12)
    cbar = fig.colorbar(c, orientation="horizontal")
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label(r"$d_y$", fontsize=18, labelpad=8)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.axis("image")
    plt.show()


def output_csv(folder, disp, strain, stress, ro=0.3, ri=0.2, bw=0.05, tol=1e-4, vis=False):
    """
    node index starts at 0
    """
    nodes, _, elements, _ = pre.readin(folder=folder + '/')
    nodes_x = nodes[:, 1]
    nodes_y = nodes[:, 2]
    type_1, type_2, type_3 = node_type(nodes_x, nodes_y, elements[:, -3:], ro=ro, ri=ri, bw=bw, tol=tol, vis=vis)
    disp_x = disp[:, 0]
    disp_y = disp[:, 1]
    strain_xx = strain[:, 0]
    strain_yy = strain[:, 1]
    strain_xy = strain[:, 2]
    stress_xx = stress[:, 0]
    stress_yy = stress[:, 1]
    stress_xy = stress[:, 2]

    with open(f"{folder}/{folder}_nodes.csv", "w") as f:
        f.write("nodeid,nodetype,coorx,coory,dispx,dispy,strainxx,strainyy,strainxy,stressxx,stressyy,stressxy\n")
        for i in range(len(nodes_x)):
            if i in type_1:
                nodetype = 1
            elif i in type_2:
                nodetype = 2
            else:
                nodetype = 3
            f.write(
                f"{i},{nodetype},{nodes_x[i]},{nodes_y[i]},{disp_x[i]:.5},{disp_y[i]:.5},{strain_xx[i]:.5},{strain_yy[i]:.5},{strain_xy[i]:.5},{stress_xx[i]:.5},{stress_yy[i]:.5},{stress_xy[i]:.5}\n")

    with open(f"{folder}/{folder}_elements.csv", "w") as f:
        f.write("elem1,elem2,elem3\n")
        for i in range(len(elements)):
            f.write(f"{elements[i, -3]},{elements[i, -2]},{elements[i, -1]}\n")


def node_type(nodes_x, nodes_y, elements, ro=0.3, ri=0.2, bw=0.05, tol=1e-4, vis=False):
    """
    nodes_x: x coordinates of the node list
    nodes_y: y coordinates of the node list
    elements: element connectivity, size (len, 3)
    Type 1: outside exterior nodes
    Type 2: inside exterior nodes
    Type 3: interior nodes
    """
    elem_list = elements.flatten().tolist()
    # count node appearances
    nodes, _ = np.unique(elem_list, return_index=True)

    # boundary geometries
    angle = math.pi / 4
    coeff = math.cos(angle)
    type_1, type_2 = [], []

    for i in nodes:
        coord_x, coord_y = nodes_x[i], nodes_y[i]
        # outer circle
        if abs(coord_x ** 2 + coord_y ** 2 - ro ** 2) < tol:
            type_1.append(i)
        # inner circle
        tol_in = 0.004
        cond_inner = abs(coord_x) < bw / 2 + tol_in or abs(coord_y) < bw / 2  + tol_in or abs(
            coord_y - coord_x) < + bw / 2 / coeff + tol_in or abs(coord_y + coord_x) < + bw / 2 / coeff + tol_in
        if abs(coord_x ** 2 + coord_y ** 2 - ri ** 2) < tol and not cond_inner:
            type_2.append(i)
        # inside

        condition_1 = abs(coord_y - coord_x) < (bw / 2 + bw * coeff) / coeff - tol_in and abs(coord_y + coord_x) < (
                    bw / 2 + bw * coeff) / coeff - tol_in
        condition_2 = abs(coord_x) < bw / 2 + bw * coeff - tol_in and abs(coord_y) < bw / 2 + bw * coeff - tol_in
        # bar_1
        if abs(coord_x - bw / 2) < tol_in or abs(coord_x + bw / 2) < tol_in:
            if coord_x ** 2 + coord_y ** 2 <= ri ** 2 and not condition_1 and not condition_2:
                type_2.append(i)
        # bar_2
        if abs(coord_y - bw / 2) < tol_in or abs(coord_y + bw / 2) < tol_in:
            if coord_x ** 2 + coord_y ** 2 <= ri ** 2 and not condition_1 and not condition_2:
                type_2.append(i)
        # bar_3
        if abs(coord_y - coord_x + bw / 2 / coeff) < tol_in or abs(coord_y - coord_x - bw / 2 / coeff) < tol_in:
            if coord_x ** 2 + coord_y ** 2 <= ri ** 2 and not condition_1 and not condition_2:
                type_2.append(i)
        # bar_4
        if abs(coord_y + coord_x + bw / 2 / coeff) < tol_in or abs(coord_y + coord_x - bw / 2 / coeff) < tol_in:
            if coord_x ** 2 + coord_y ** 2 <= ri ** 2 and not condition_1 and not condition_2:
                type_2.append(i)
    type_3 = [node for node in nodes if node not in type_1 + type_2]
    if vis:
        x_1 = [nodes_x[i] for i in type_1]
        y_1 = [nodes_y[i] for i in type_1]
        x_2 = [nodes_x[i] for i in type_2]
        y_2 = [nodes_y[i] for i in type_2]
        x_3 = [nodes_x[i] for i in type_3]
        y_3 = [nodes_y[i] for i in type_3]
        plt.figure(figsize=(8, 8))
        plt.title(f"ro={ro:.3}, ri={ri:.3}, bw={bw:.3}", fontsize=16)
        plt.scatter(x_1, y_1, label="Type 1")
        plt.scatter(x_2, y_2, label="Type 2")
        plt.scatter(x_3, y_3, label="Type 3")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.show()

    return type_1, type_2, type_3

