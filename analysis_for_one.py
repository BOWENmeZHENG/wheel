import run_fem
import postprocess


def analysis(r_out=0.2, r_in=0.15, bar_width=0.02, center_x=0., center_y=0., E=1.0e8, nu=0.3, load=-20.0e3,
             plot=False, csv=True):
    disp, strain, stress, folder = run_fem.run(r_out=r_out, r_in=r_in, bar_width=bar_width,
                                               center_x=center_x, center_y=center_y,
                                               E=E, nu=nu, load=load)
    stress /= 1e6  # Unit: MPa

    if plot:
        postprocess.plot_results(folder, disp, strain, stress)
    if csv:
        postprocess.output_csv(folder, disp, strain, stress, ro=r_out, ri=r_in, bw=bar_width, vis=True)

    return folder
