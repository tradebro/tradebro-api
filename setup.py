from setuptools import find_packages, setup

setup(
    name='src',
    version='1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    scripts=['bin/test'],
    classifiers=[
        'Environment :: Console',
        'Development Status :: 2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
    ],
)
