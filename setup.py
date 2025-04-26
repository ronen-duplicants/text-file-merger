from setuptools import setup, find_packages

setup(
    name='text-file-merger',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple tool to merge multiple text files into one.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/text-file-merger',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)