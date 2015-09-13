#!/usr/bin/env python3
"""bucket"""
import re
import sys
import os
import urllib.request
import tarfile
from urllib.parse import urljoin
from prep import SearchForPackage
from pretty import ProgressBar
from pkg_resources import parse_version

PYPI_ENDPOINT = "https://pypi.python.org/simple/"


class DownloadPackage(object):

    def __init__(self, pkg):
        """
            Download Package class with version check logic
            -
            @pkg - package name to download
            @quiet - do not print out any output
            @dependencies - if set to True download all dependencies
        """
        self.pkg = pkg
        self.quiet = False
        self.dependencies = True

    def version_check(self, requested, pkg):
        """Returns version of package which pass
            logical requirements: >,<,<=,>=,==="""
        match = re.match('(\w+)(\W+)([\w\.\-]+)', requested)
        package, check, version = None, None, None

        if match:
            package, check, version = match.groups()

        pkg = parse_version(pkg)
        c_pkg = parse_version("{}-{}".format(package, version))
        check_version = {
            None: True,
            ">=": pkg >= c_pkg,
            "<=": pkg <= c_pkg,
            "==": pkg == c_pkg,
            ">": pkg > c_pkg,
            "<": pkg < c_pkg
        }
        return check_version.get(check, None)

    def __unpack(self, members):
        for info in members:
            # print("/".join(info.name.split("/")[1:]))
            if "/".join(info.name.split("/")[1:]) in [
                "{}.egg-info/requires.txt".format(self.pkg),
                "requirements.txt"
            ]:
                return info
        return None

    def dependencies_check(self, archive):
        """ Check package dependencies
             look for 'package_name'.egg-info/requires.txt
             or
             requirements.txt
        """
        tar = tarfile.open("repo/{}".format(archive))
        unpack = self.__unpack(tar)
        if unpack is None:
            return
        a_file = tar.extractfile(member=self.__unpack(tar))
        for dep in a_file:
            dep = dep.decode('ascii')
            if re.match("^\w", dep):
                download = DownloadPackage(dep)
                download()

        tar.close()

    def __download(self):
        package = SearchForPackage(PYPI_ENDPOINT)

        for package, extension, link in \
                package(re.findall("\w+", self.pkg)[0]):

            if self.version_check(self.pkg, package):
                link = urljoin(PYPI_ENDPOINT, link, False)
                link = link.replace("../", "")
                print("Requested: {} | Downloading: {}".format(
                    self.pkg.split()[0], package))
                urllib.request.urlretrieve(link,
                                           "repo/{}.{}".format(package,
                                                               extension),
                                           reporthook=ProgressBar.hook)
                urllib.request.urlcleanup()
                print()
                self.dependencies_check("{}.{}".format(package, extension))
                return True

    def __call__(self):
        self.__download()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Provide arg!")
        sys.exit(1)
    download = DownloadPackage(sys.argv[1])
    download()
