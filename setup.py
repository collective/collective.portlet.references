from setuptools import setup, find_packages

version = '1.0.1.dev0'

setup(name='collective.portlet.references',
      version=version,
      description="Display references of a page",
      long_description=(open("README.txt").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='',
      author='Zest Software',
      author_email='m.van.rees@zestsoftware.nl',
      url='https://github.com/collective/collective.portlet.references',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
