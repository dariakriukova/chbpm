from setuptools import setup, find_packages

setup(
    name='chbpm',
    version='0.1.0',
    packages=find_packages(),
    description='A Python library for BPM adjustment in audio files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Daria Kriukova',
    author_email='daria.kriukova@pm.me',
    url='https://github.com/dariakriukova/rhythm-is-a-runner.git',
    install_requires=[
        'librosa',
        'pydub',
        'soundfile',
        'audioread',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'chbpm=chbpm.__main__:main',
        ],
    },
)
