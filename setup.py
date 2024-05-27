from setuptools import find_packages, setup

setup(
    name='netbox-lifecycle',
    version='1.0.4',
    description='NetBox Lifecycle',
    long_description='NetBox Support Contract and EOL/EOS management',
    url='https://github.com/dansheps/netbox-lifecycle/',
    download_url='https://pypi.org/project/netbox-lifecycle/',
    author='Daniel Sheppard',
    author_email='dans@dansheps.com',
    maintainer='Daniel Sheppard',
    maintainer_email='dans@dansheps.com',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    license='Proprietary',
    zip_safe=False,
    platform=[],
    keywords=['netbox', 'netbox-plugin'],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ]
)