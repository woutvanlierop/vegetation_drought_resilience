"""
Setup configuration for vegetation_drought_resilience package.
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="vegetation-drought-resilience",
    version="0.1.0",
    author="Vegetation Drought Resilience Team",
    description="Drought impact monitoring using satellite imagery and weather data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vegetation_drought_resilience",
    packages=find_packages(where=".", exclude=["tests*", "notebooks*", "docs*"]),
    include_package_data=True,
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="drought monitoring satellite imagery weather climate geospatial",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/vegetation_drought_resilience/issues",
        "Source": "https://github.com/yourusername/vegetation_drought_resilience",
        "Documentation": "https://github.com/yourusername/vegetation_drought_resilience/blob/main/docs/",
    },
)
