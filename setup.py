from setuptools import setup, find_namespace_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    name="dsxquant",  # 包名称
    version="1.1.0",  # 版本号
    author="fangyunsm",  # 作者
    author_email="934476300@qq.com",  # 作者邮箱
    description="Dsxquant 是一个基于python语言开发的的量化工具箱，主要特征是其工具属性，专为上层策略应用提供服务。",  # 描述
    long_description=readme(),  # 长文描述
    keywords="quant 量化",  # 项目关键词
    url="https://github.com/dsxkline/dsx_quant_python",  # 项目主页
    license="MIT License",  # 许可证
    # packages=find_namespace_packages('pydsxkline'),
    zip_safe=False,
    packages=['dsxquant'],
    package_dir={"dsxquant": "src/dsxquant"},
    include_package_data=True,
    # package_data={"": ['*.py', '*.js', '*.html']},
    # install_requires=['pywebview'],
    python_requires='>=3.6,<4'
)
