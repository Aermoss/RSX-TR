from setuptools import setup, find_packages

with open("README.md", "r", encoding = "UTF-8") as file:
    long_desc = file.read()

setup(
    name = "rsxtr",
    version = "0.0.1",
    entry_points = {
        "console_scripts": [
            "rsxtr = rsxtr.main:main"
        ]
    },
    description = "Platformlar arası uygulamalar için tasarlanan, yorumlanan, statik olarak yazılan çoklu paradigmalı genel amaçlı bir programlama dili olan R#'ın Türkçe versiyonu.",
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Aermoss/RSX-TR",
    author = "Yusuf Rencber",
    author_email = "yusufrencber546@gmail.com",
    license = "MIT",
    keywords = "",
    packages = find_packages(),
    include_package_data = True,
    install_requires = ["rsharp==0.0.12"]
)