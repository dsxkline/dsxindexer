from setuptools import setup, find_namespace_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    name="dsxindexer",  # 包名称
    version="1.1.0",  # 版本号
    author="fangyunsm",  # 作者
    author_email="934476300@qq.com",  # 作者邮箱
    description="dsxindexer 是一个基于麦语言的指标生成器，支持常用指标，自定义扩展指标算法，公式编辑功能",  # 描述
    long_description=readme(),  # 长文描述
    keywords="通达信指标,公式编辑器,量化指标",  # 项目关键词
    url="https://github.com/dsxkline/dsxindexer",  # 项目主页
    license="MIT License",  # 许可证
    # packages=find_namespace_packages('pydsxkline'),
    zip_safe=False,
    packages=['dsxindexer'],
    package_dir={"dsxindexer": "src/dsxindexer"},
    include_package_data=True,
    # package_data={"": ['*.py', '*.js', '*.html']},
    install_requires=[
        "dsxquant>=2.1.0",
        "numba==0.56.4",
        "progressbar33==2.4"
    ],
    python_requires='>=3.6,<4'
)
