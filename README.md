# Ray-Tracing-The-Next-Week-with-SlangPy
![](https://raw.githubusercontent.com/Delee0209/Ray-Tracing-The-Next-Week-with-SlangPy/refs/heads/main/captured/screenshot.png)
Implementation of Ray Tracing The Next Week written in python and slang via [SlangPy](https://slangpy.shader-slang.org/en/latest/)
- currently only implement to [section 7.3](https://raytracing.github.io/books/RayTracingTheNextWeek.html#lights/turningobjectsintolights)

## Dependencies
- Python >= 3.9
- SlangPy   `pip install slangpy==0.38.1`
  - at the moment, only work with version 0.38.1 due to the slang compiler version
- NumPy     `pip install numpy`

## Run Program
- `rttnw.py` is the main program
  - containing scene setup and camera parameters
  - to execute, simply use `python rttnw.py`
