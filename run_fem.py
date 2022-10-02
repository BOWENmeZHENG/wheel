import preprocess
from solidspy import solids_GUI
import matplotlib.pyplot as plt


def run(r_out=0.2, r_in=0.15, bar_width=0.02, center_x=0, center_y=0,
        E=1.0e8, nu=0.3, load=20.0e3,
        plot_contours=False, compute_strains=True):
    mesh = preprocess.meshing(r_out=r_out, r_in=r_in, bar_width=bar_width, center_x=center_x, center_y=center_y)
    folder = f"ro{r_out:.3}_ri{r_in:.3}_bw{bar_width:.3}"
    preprocess.write_files(mesh, folder, r_out=r_out, E=E, nu=nu, load=load)
    disp_complete, strain_nodes, stress_nodes = solids_GUI(plot_contours=plot_contours,
                                                           compute_strains=compute_strains,
                                                           folder=folder + '/')
    if plot_contours:
        plt.show()

    return disp_complete, strain_nodes, stress_nodes, folder
