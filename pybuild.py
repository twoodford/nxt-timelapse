from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    packages = ["buildlapse"],
    ext_modules = [Extension("buildlapse.gphoto2", ["buildlapse/gphoto2.pyx"], libraries=["gphoto2"])]
)

