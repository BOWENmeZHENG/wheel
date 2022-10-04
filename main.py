import analysis_for_one as one
import numpy as np
import os
import shutil

# Define parameters of training data
np.random.seed(199)

r_out = 0.1 * np.random.rand(2) + 0.2  # range: 0.2 to 0.3
r_in = r_out - (0.05 * np.random.rand(2) + 0.1)
bar_width = 0.03 * np.random.rand(2) + 0.02

# Write .csv files for ML training
for ro in r_out:
    for ri in r_in:
        for bw in bar_width:
            folder = one.analysis(r_out=ro, r_in=ri, bar_width=bw,
                                  center_x=0.0, center_y=0.0,
                                  E=1.0e8, nu=0.3, load=-20.0e3,
                                  plot=False
                                  )
            data_folder = "try"
            os.makedirs(data_folder, exist_ok=True)
            shutil.copyfile(f"{folder}/{folder}_elements.csv", f"{data_folder}/{folder}_elements.csv")
            shutil.copyfile(f"{folder}/{folder}_nodes.csv", f"{data_folder}/{folder}_nodes.csv")
            # shutil.rmtree(folder)
