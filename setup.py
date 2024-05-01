from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess


class CustomBuildPy(build_py):
    def run(self):
        subprocess.run('./voiceref/compile_proto.sh', check=True)
        build_py.run(self)


setup(
    name='voiceref',
    version='0.1.0',
    author='Shotak Aoki',
    author_email='macakasit@gmail.com',
    packages=find_packages(),
    license='LICENSE',
    description='Voice player with RoboCup SSL Game Controller messages.',
    long_description=open('README.md').read(),
    install_requires=[
        "protobuf <= 3.20",
        "typing_extensions >= 4.9.0",
    ],
    extras_require={
        'dev': [
            'flake8 >= 3.7.9',
            'pytest >= 5.4.1',
            'coverage >= 6.2',
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    cmdclass={
        'build_py': CustomBuildPy
    },
    entry_points={
        'console_scripts': [
            'voiceref=voiceref.main:main'  # 'コマンド名=パッケージ名.モジュール名:関数名'
        ]
    },
)
