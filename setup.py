from setuptools import setup

package_name = 'cv_camera'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
           ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pengtao',
    maintainer_email='497045220@qq.com',
    description='A ROS2 node for camera show v4l2',
    license='apache License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'image_show = cv_camera.image_show:main',
        'v4l2_camera = cv_camera.v4l2_camera:main',
        ],
    },
)
