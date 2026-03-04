from setuptools import find_packages, setup

package_name = 'speed_zone_limiter'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),

        ('share/' + package_name, ['package.xml']),

        ('share/' + package_name + '/launch', ['launch/speed_zone_limiter.launch.py']),

        ('share/' + package_name + '/config', ['config/slow_zone.yaml']),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yash',
    maintainer_email='yash@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'speed_zone_limiter = speed_zone_limiter.speed_zone_limiter_node:main',
    ],
  },
)
