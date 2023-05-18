import setuptools

setuptools.setup(
    name='tsi',
    version='1.0',
    description='UCD-500 API package',
    author='author@INTEL',
    license='BSD License',
    packages=setuptools.find_packages(),
    install_requires=['Pillow', 'reportlab'],
    python_requires='>=3.6',
    package_data={'': ['*.dll', '*.pdf', '*.json', '*.so', '*.hex', '*.bin']},
)