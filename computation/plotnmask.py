import pyorc
import xarray as xr
import numpy as np
import copy
from matplotlib.colors import Normalize
import cartopy.io.img_tiles as cimgt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# Load dataset and video
ds = xr.open_dataset("computation/ngwerere_piv.nc")
video = pyorc.Video("computation/ngwerere_20191103.mp4", start_frame=0, end_frame=125)
video.camera_config = ds.velocimetry.camera_config

# RGB frame projection
da_rgb = video.get_frames(method="rgb")
da_rgb_proj = da_rgb.frames.project()

# Plot raw frame
p = da_rgb_proj[0].frames.plot()

# Plot masked average velocimetry (basic)
ds_mean = ds.mean(dim="time", keep_attrs=True)
ds_mean.velocimetry.plot.pcolormesh(ax=p.axes, alpha=0.3, cmap="rainbow", add_colorbar=True, vmax=0.6)
ds_mean.velocimetry.plot(ax=p.axes, color="w", alpha=0.5)

# Apply default masking methods
ds_mask = copy.deepcopy(ds)
ds_mask.velocimetry.mask.corr(inplace=True)
ds_mask.velocimetry.mask.minmax(inplace=True)
ds_mask.velocimetry.mask.rolling(inplace=True)
ds_mask.velocimetry.mask.outliers(inplace=True)
ds_mask.velocimetry.mask.variance(inplace=True)
ds_mask.velocimetry.mask.angle(inplace=True)
ds_mask.velocimetry.mask.count(inplace=True)

# Mean after masking
ds_mean_mask = ds_mask.mean(dim="time", keep_attrs=True)
p = da_rgb_proj[0].frames.plot()
ds_mean_mask.velocimetry.plot(ax=p.axes, alpha=0.4, norm=Normalize(vmax=0.6, clip=False), add_colorbar=True)

# More aggressive filtering with relaxed angle and window mean
ds_mask2 = copy.deepcopy(ds)
ds_mask2.velocimetry.mask.corr(inplace=True)
ds_mask2.velocimetry.mask.minmax(inplace=True)
ds_mask2.velocimetry.mask.rolling(inplace=True)
ds_mask2.velocimetry.mask.outliers(inplace=True)
ds_mask2.velocimetry.mask.variance(inplace=True)
ds_mask2.velocimetry.mask.angle(angle_tolerance=0.5 * np.pi)
ds_mask2.velocimetry.mask.count(inplace=True)
ds_mask2.velocimetry.mask.window_mean(wdw=2, inplace=True, tolerance=0.5, reduce_time=True)

# Mean after advanced masking
ds_mean_mask2 = ds_mask2.mean(dim="time", keep_attrs=True)
p = da_rgb_proj[0].frames.plot()
ds_mean_mask2.velocimetry.plot(ax=p.axes, alpha=0.4, norm=Normalize(vmax=0.6, clip=False), add_colorbar=True)

# Geographical plot with satellite background
p = da_rgb_proj[0].frames.plot(mode="geographical")
ds_mean_mask2.velocimetry.plot(ax=p.axes, mode="geographical", alpha=0.4, norm=Normalize(vmax=0.6, clip=False), add_colorbar=True)
tiles = cimgt.GoogleTiles(style="satellite")
p.axes.add_image(tiles, 19)
p.axes.set_extent([
    da_rgb_proj.lon.min() - 0.00005,
    da_rgb_proj.lon.max() + 0.00005,
    da_rgb_proj.lat.min() - 0.00005,
    da_rgb_proj.lat.max() + 0.00005],
    crs=ccrs.PlateCarree()
)

# Camera mode augmented reality plot
p = da_rgb[0].frames.plot(mode="camera")
ds_mean_mask.velocimetry.plot(
    ax=p.axes,
    mode="camera",
    alpha=0.4,
    norm=Normalize(vmin=0., vmax=0.6, clip=False),
    add_colorbar=True
)

plt.savefig("computation/camera_overlay.png", dpi=150, bbox_inches="tight")
plt.close()
print("camera_overlay.png")

# Save masked dataset
ds_mask2.velocimetry.set_encoding()
ds_mask2.to_netcdf("computation/ngwerere_masked.nc")

# Compute average velocity magnitude
'''u = ds_mean_mask2['v_x']
v = ds_mean_mask2['v_y']
velocity_magnitude = np.sqrt(u**2 + v**2)
average_velocity = velocity_magnitude.mean(skipna=True)
units = u.attrs.get('units', "")

print("Average velocity magnitude:", average_velocity.values)
print("Units of velocity:", units)'''
