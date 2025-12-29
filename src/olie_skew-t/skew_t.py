'''Create a Skew-T diagram from a grib file'''
import sys
import numpy as np
import matplotlib.pyplot as plt
import pygrib

from pathlib import Path
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from metpy.calc import dewpoint_from_relative_humidity, parcel_profile
from metpy.plots import SkewT, Hodograph, add_metpy_logo
from metpy.units import units

try:
    file = sys.argv[1]
    lat = float(sys.argv[2])
    lon = float(sys.argv[3])
    label = sys.argv[4].lower()
except Exception:
    print("Usage: python SkewT.py grib_path lat lon label")
    sys.exit()

outfile = f"{label}.png"
title = f"\"{label}\" {Path(file).stem} ({lat:.2f}, {lon:.2f})"

# Print a fancy headery
print("____  _____")
print("Olie\\/ortex Analytics")
print()
print("Create Skew-T Log P for a point from GRIB2 file")
print()
print(f'SkewT.py {file} {lat:.2f} {lon:.2f} {label}')
print()

grbs = pygrib.open(file)

p = []
T = []
Td = []
bu = []
bv = []
bp = []
hu = []
hv = []
hp = []
UVAL = 0.0
VVAL = 0.0

print("Processing...")

for x in range(1000, 99, -25):
    print(f"  Level: {x}")

    is_hodo = x >= 500
    is_barb = x % 50 == 0

    data, _, _ = grbs.select(name='Temperature', level=x)[0].data(
        lat1=lat, lat2=lat + 0.2, lon1=lon, lon2=lon + 0.2)
    temperature = data[0] - 273.15

    data, _, _ = grbs.select(name='Relative humidity', level=x)[0].data(
        lat1=lat, lat2=lat + 0.2, lon1=lon, lon2=lon + 0.2)
    dewpoint = dewpoint_from_relative_humidity(
        temperature * units.degC, data[0] / 100.0).magnitude

    if (is_hodo or is_barb):
        data, _, _ = grbs.select(name='U component of wind', level=x)[0].data(
            lat1=lat, lat2=lat + 0.2, lon1=lon, lon2=lon + 0.2)
        UVAL = data[0]

        data, _, _ = grbs.select(name='V component of wind', level=x)[0].data(
            lat1=lat, lat2=lat + 0.2, lon1=lon, lon2=lon + 0.2)
        VVAL = data[0]

    if is_hodo:
        hu.append(UVAL)
        hv.append(VVAL)
        hp.append(x)

    if is_barb:
        bu.append(UVAL)
        bv.append(VVAL)
        bp.append(x)

    p.append(x)
    Td.append(dewpoint)
    T.append(temperature)

del grbs
p = np.array(p) * units.hPa
T = np.array(T) * units.degC
Td = np.array(Td) * units.degC
bp = np.array(bp) * units.hPa
bu = np.array(bu) * (units.meters / units.second)
bv = np.array(bv) * (units.meters / units.second)
hp = np.array(hp) * units.hPa
hu = np.array(hu) * (units.meters / units.second)
hv = np.array(hv) * (units.meters / units.second)

print('  Level: Parcel')
# Calculate the parcel profile.
parcel_prof = parcel_profile(p, T[0], Td[0])

print("Plotting...")

# Create a new figure. The dimensions here give a good aspect ratio
fig = plt.figure(figsize=(9, 12))
add_metpy_logo(fig, 115, 100)
skew = SkewT(fig, rotation=20, aspect=150)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r', linewidth=1)
skew.plot(p, Td, 'g', linewidth=1)
skew.plot_barbs(bp, bu, bv)
skew.ax.set_ylim(1000, 100)
skew.ax.set_xlim(-40, 40)

# Better labels
skew.ax.set_title(title)
skew.ax.set_xlabel(f'Temperature ({T.units:~P})')
skew.ax.set_ylabel(f'Pressure ({p.units:~P})')

# Plot the parcel profile as a black line
skew.plot(p, parcel_prof, 'k', linewidth=1)
skew.shade_cape(p, T, parcel_prof)

# Create a hodograph
# Create an inset axes object that is 40% width and height of the
# figure and put it in the upper right hand corner.
ax_hod = inset_axes(skew.ax, '40%', '40%', loc=1)
h = Hodograph(ax_hod, component_range=50.)
h.add_grid(increment=25)
h.plot_colormapped(hu, hv, hp)

print(f"Saving {outfile}...")

# Show the plot
plt.savefig(outfile, bbox_inches='tight', pad_inches=0.1)
plt.close(fig)
