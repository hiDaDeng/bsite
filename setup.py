from setuptools import setup
import setuptools
setup(
    name='bsite',     # 包名字
    version='1.0',   # 包版本
    description='bsite是用于采集B站用户视频列表页、视频评论数据的python包。 https://github.com/thunderhit/bsite',
    author='大邓',  # 作者
    author_email='thunderhit@qq.com',  # 邮箱
    url='https://github.com/thunderhit/bsite',      # 包的主页
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    python_requires='>=3.5',
    license="MIT",
    keywords=['data collect', '数据采集', 'bilibili'],
    long_description=open('README.md').read(), # 读取的Readme文档内容
    long_description_content_type="text/markdown")  # 指定包文档格式为markdown
    #py_modules = ['eventextraction.py']
