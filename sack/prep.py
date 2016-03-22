#!/usr/bin/env python3
"""

Sync list of python packages from repositories like:
    - https://pypi.python.org/simple/
It might be any other pypi compatybile repository as well

"""

import re

from urllib.request import urlopen
from urllib.error import HTTPError

from lxml import etree
from io import StringIO
from pkg_resources import parse_version


class ExtractLinks(object):
    """Extract a tags from returned response.read()"""

    def __init__(self, body):
        super(ExtractLinks, self).__init__()
        self.body = StringIO(body.decode('ascii'))

    def get_path(self, rel=True):
        """Get list of links by parsing reponse body.
            if rel set to True, list only internal,
            else list all links"""
        tree = etree.parse(self.body)
        if rel is True:
            return tree.xpath('/html/body/a[@rel]/@href')
        else:
            return tree.xpath('/html/body/a/@href')

    def details(self):
        """Return tuple of
            - full url
            - package name with version
            - extension"""
        links = self.get_path(rel=True)
        return [(app_ver, ext, link) for link in links for app_ver, ext in
                re.findall((r'(?P<file>[\w\.\-]+?)'
                            r'[.]'
                            r'(?P<ext>tar\.gz|tar\.bz2|zip)#'), link)
                ]


class SearchForPackage(object):
    """Search simple subdirectory for package name"""

    def __init__(self, endpoint):
        super(SearchForPackage, self).__init__()
        self.endpoint = endpoint

    def exist(self, package):
        """ Make GET request to PYPI_ENDPOINT/packagename """
        response = urlopen("{endpoint}/{package}/".format(
            endpoint=self.endpoint,
            package=package.lower()))
        return response

    def __call__(self, package):
        """ Check if self.exist() returned HTTPError.code = 404
             if not - package found """
        try:
            response = self.exist(package)
        except HTTPError as e:
            if e.code == 404:
                print("No such package found")
                return ()
        else:
            extract = ExtractLinks(response.read())
            return sorted(extract.details(),
                          key=lambda x: parse_version(x[0]),
                          reverse=True)
