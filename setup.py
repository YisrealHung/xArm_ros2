from setuptools import find_packages, setup

package_name = 'xarm'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Yisreal',
    maintainer_email='nagual1414@gmail.com',
    description='TODO: xArm ROS 2 Humble Package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'xarm_node = xarm.xarm:main',
            'xarm_teleop_keyboard = xarm.xarm_teleop_keyboard:main'
        ],
    },
)
