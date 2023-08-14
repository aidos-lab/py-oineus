from setuptools import setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext

import os
import subprocess
import sys


class CMakeExtension(Extension):
    def __init__(self, name, root_dir, **kwargs):
        super().__init__(name, sources=[], **kwargs)
        self.root_dir = os.path.abspath(root_dir)


class CMakeExtensionBuilder(build_ext):
    def run(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise "heck"

        self.install_dependencies()

        for ext in self.extensions:
            self.build_extension(ext)

    def install_dependencies(self):
        subprocess.check_call(["git", "submodule", "update", "--init", "--recursive"])

    def build_extension(self, ext):
        # Specifies the path under which we can expect the output
        # library. This depends on the package and may change.
        ext_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(self.get_ext_fullpath(ext.name)),
                "oineus",
                "bindings",
                "python",
            )
        )

        # Additional arguments for `CMake`. These ensure that we are
        # using the right version of Python and specify the *output*
        # directory of the library.
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
        ]

        # Additional arguments for building the module.
        build_args = ["-j4"]

        # Let's make sure we have a temporary directory for building
        # everything.
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(["cmake", ext.root_dir] + cmake_args, cwd=self.build_temp)

        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )


setup(
    name="py-oineus",
    version="",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="",
    license="MIT",
    packages=["oineus"],
    install_requires=[
        "Cython",
        "numpy",
    ],
    ext_modules=[CMakeExtension("oineus", "oineus")],
    cmdclass={"build_ext": CMakeExtensionBuilder},
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="",
)
