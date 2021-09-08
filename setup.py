from setuptools import setup


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='velenium',
    packages=['velenium'],
    version='0.4.1',
    license='MIT',
    description='Interact with an app using visual definitions of elements',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alejandro Manzanero',
    author_email='alejmans@gmail.com',
    url='https://github.com/Manzanero/velenium',
    download_url='https://github.com/Manzanero/velenium/archive/refs/tags/v0.4.1.tar.gz',
    keywords=['visual testing'],
    install_requires=[
        'opencv-python',
        'imutils',
        'numpy',
        'Appium-Python-Client',
        'selenium',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
