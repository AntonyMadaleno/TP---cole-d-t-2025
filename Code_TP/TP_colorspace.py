### IMPORTS ### ==================================================================================

from hsi_loader import *
from hsi_manipulation import *
from hsi_colorspace import *

import matplotlib.pyplot as plt
from tkinter import filedialog as fd

CIE_1931_path = fd.askopenfilename(title = "CIE 1931 Standard Observer")

# 1 . Load spectral cube
cube, cube_wl = load_envi_image(fd.askopenfilename(title="BIN or DAT, raw data"), fd.askopenfilename(title="Header .hdr"))

# 2 . Load scene illuminant
illuminant, illum_wl = load_spectrum_file(fd.askopenfilename(title="Illumination spectrum (csv or spd)"))

# 3 . knowing scene illuminant we can build our XYZ to RGB transfomation matrix
_, _, Xw, Yw, Zw = compute_chromaticity_coordinates(spectrum= illuminant, spectrum_wavelengths= illum_wl, cmf_path= CIE_1931_path)

# 4 . Compute the chromaticity coordinate of the cameras system based on previously aquired sensitivity spectras of the camera channels
red_ssf, red_wl         = load_spectrum_file(fd.askopenfilename(title="Red sensitivity spectrum (csv or spd)"))
green_ssf, green_wl     = load_spectrum_file(fd.askopenfilename(title="Green sensitivity spectrum (csv or spd)"))
blue_ssf, blue_wl       = load_spectrum_file(fd.askopenfilename(title="Blue sensitivity spectrum (csv or spd)"))

xr, yr, _, _, _ = compute_chromaticity_coordinates(spectrum= red_ssf, spectrum_wavelengths= red_wl, cmf_path= CIE_1931_path)
xg, yg, _, _, _ = compute_chromaticity_coordinates(spectrum= green_ssf, spectrum_wavelengths= green_wl, cmf_path= CIE_1931_path)
xb, yb, _, _, _ = compute_chromaticity_coordinates(spectrum= blue_ssf, spectrum_wavelengths= blue_wl, cmf_path= CIE_1931_path)

# les coordonées du système RGB (# sRGB in this case)
"""
xr, yr = 0.6400, 0.3300
xg, yg = 0.3000, 0.6000
xb, yb = 0.1500, 0.0600
"""

Xr = xr / yr;   Zr = (1 - xr - yr) / yr
Xg = xg / yg;   Zg = (1 - xg - yg) / yg
Xb = xb / yb;   Zb = (1 - xb - yb) / yb

T = np.matrix([
    [Xr, Xg, Xb],
    [1., 1., 1.],
    [Zr, Zg, Zb]
])

W = np.matrix([Xw, Yw, Zw]).transpose()

S = np.linalg.inv(T) * W

M = np.matrix(
    [
        [S[0,0] * Xr, S[1,0] * Xg, S[2,0] * Xb],
        [S[0,0] * 1., S[1,0] * 1., S[2,0] * 1.],
        [S[0,0] * Zr, S[1,0] * Zg, S[2,0] * Zb]
    ]
)

M_inv = np.asarray(np.linalg.inv(M))

print(f"M :\n{M}\n")
print(r"$M^{-1}$")
print(f"{M_inv}")

# 4 . Use said matrix to tranform the spectral image to XYZ then to RGB

# 4-A . Spectral to XYZ
xyz_img = cube_to_xyz(cube, cube_wl)

# 4-B . XYZ to RGB
rgb_img = xyz_to_rgb(xyz_img, transformation_matrix= M_inv, gamma_correction= 2.2)

# 5 . Display
plt.imshow(rgb_img)
plt.show()