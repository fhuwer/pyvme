import setuptools

setuptools.setup(
    name="pyvme",
    version="0.2",
    author="Friedemann Neuhaus",
    author_email="friedemann@neuhaus-tech.de",
    description="Library to control VME devices over the CAEN bridge",
    url="https://github.com/fneuhaus/pyvme",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
)
