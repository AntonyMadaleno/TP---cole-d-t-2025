### IMPORTS ### ==================================================================================

from hsi_loader import *
from hsi_manipulation import *
from hsi_colorspace import *

import matplotlib.pyplot as plt
from tkinter import filedialog as fd

# 1 . Load mesured spectras
path_white_spectrum         = fd.askopenfilename(title="white reference spectrum")  # White reference acquired with JETI
path_measured_spectrum      = fd.askopenfilename(title="measured spectrum")         # Measured spectra acquired with JETI
path_measured_reflectance   = fd.askopenfilename(title="measured reflectance")      # Measured reflectance acquired with CS1000

white_spectrum, white_wavelengths = load_spectrum_file(path_white_spectrum)
measured_spectrum, measured_wavelengths = load_spectrum_file(path_measured_spectrum)
measured_reflectance, measured_reflectance_wavelengths = load_spectrum_file(path_measured_reflectance)

# 1-B . resample
wl = np.arange(start= 380, stop= 781, step= 5)
white_spectrum     = resample_spectrum_to_wavelengths(spectrum_values=white_spectrum, original_wavelengths=white_wavelengths, target_wavelengths=wl, interpolation_method='cubic')
measured_spectrum  = resample_spectrum_to_wavelengths(spectrum_values=measured_spectrum, original_wavelengths=measured_wavelengths, target_wavelengths=wl, interpolation_method='cubic')
measured_reference = resample_spectrum_to_wavelengths(spectrum_values=measured_reflectance, original_wavelengths=measured_reflectance_wavelengths, target_wavelengths=wl, interpolation_method='cubic')

# 2 . Compute reflectance
computed_reflectance = measured_spectrum / white_spectrum

# 3 . Display results

plt.plot(wl, white_spectrum, lw= 2, alpha= 0.4, label= "white reference", color = 'red')
plt.plot(wl, measured_reference, lw= 2, alpha= 0.4, label= "measured spectra", color = 'blue')

plt.legend()
plt.show()

############################################################################################################

plt.plot(wl, measured_reflectance, lw= 2, alpha= 0.4, label= "measured reflectance", color = 'red')
plt.plot(wl, computed_reflectance, lw= 2, alpha= 0.4, label= "computed reflectance", color = 'blue')

plt.legend()
plt.show()