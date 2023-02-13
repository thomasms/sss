from setuptools import setup

VERSION = "0.0.2"


setup(
    name="esses",
    version=VERSION,
    description="Stupidly Simple Storage",
    url="https://github.com/thomasms/sss",
    author="Tom Stainer",
    author_email="me@physicstom.com",
    license="Apache License 2.0",
    packages=[
        "sss",
        "sss.stores",
    ],
    install_requires=["pandas"],
    python_requires=">=3.8",
    scripts=[],
    setup_requires=[
        "pytest-runner",
    ],
    # test_suite="tests.testsuite",
    # tests_require=[
    #     "pytest",
    # ],
    include_package_data=True,
    zip_safe=False,
)
