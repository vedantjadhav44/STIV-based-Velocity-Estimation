import pyorc
import matplotlib.pyplot as plt
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from dask.diagnostics import ProgressBar
from matplotlib import patches

cam_config = pyorc.load_camera_config("computation/ngwerere.json")
video_file = "computation/ngwerere_20191103.mp4"

# Area for stabilization, ideally covering water surface and beyond
stabilize = [
    [150, 0],
    [500, 1079],
    [1750, 1079],
    [900, 0]
]

video = pyorc.Video(
    video_file,
    camera_config=cam_config,
    start_frame=0,
    end_frame=125,
    stabilize=stabilize,
    h_a=0.,
)

# === TEMPORARY PLOT: Show raw frame and stabilization polygon ===
"""
patch_kwargs = {
    "alpha": 0.5,
    "zorder": 2,
    "edgecolor": "w",
    "label": "Area of interest",
}
f, ax = plt.subplots(1, 1, figsize=(10, 6))
frame = video.get_frame(0, method="rgb")
ax.imshow(frame)
patch = patches.Polygon(stabilize, **patch_kwargs)
ax.add_patch(patch)
"""

# Get frames from video
da = video.get_frames()

# === TEMPORARY PLOT: Show first grayscale frame ===
"""
da[0].frames.plot(cmap="gray")
"""

# Normalize frames
da_norm = da.frames.normalize()

# === TEMPORARY PLOT: Show normalized frame with colorbar ===
"""
p = da_norm[0].frames.plot(cmap="gray")
plt.colorbar(p)
"""

# Project normalized grayscale frames using camera config
f = plt.figure(figsize=(16, 9))
da_norm_proj = da_norm.frames.project(method="numpy")

# === TEMPORARY PLOT: View projected normalized grayscale frame ===
"""
da_norm_proj[0].frames.plot(cmap="gray")
"""

# Get RGB frames and project them
da_rgb = video.get_frames(method="rgb")
da_rgb_proj = da_rgb.frames.project()

# === TEMPORARY PLOT: Show first projected RGB frame with satellite overlay ===
"""
p = da_rgb_proj[0].frames.plot(mode="geographical")
tiles = cimgt.GoogleTiles(style="satellite")
p.axes.add_image(tiles, 19)
p.axes.set_extent([
    da_rgb_proj.lon.min() - 0.0001,
    da_rgb_proj.lon.max() + 0.0001,
    da_rgb_proj.lat.min() - 0.0001,
    da_rgb_proj.lat.max() + 0.0001
], crs=ccrs.PlateCarree())
"""

# Perform PIV on normalized projected frames and save result
piv = da_norm_proj.frames.get_piv(engine="numba")
piv.to_netcdf("computation/ngwerere_piv.nc")
