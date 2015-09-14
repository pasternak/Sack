#!/usr/bin/env python3
"""bucket"""
import re
import sys
import os
import urllib.request
import tarfile
from urllib.parse import urljoin
from prep import SearchForPackage
from pretty import ProgressBar, Color
from pkg_resources import parse_version

PYPI_ENDPOINT = "https://pypi.python.org/simple/"


class DownloadPackage(object):

    def __init__(self, pkg, quiet=False, dependencies=False):
        """
            Download Package class with version check logic
            -
            @pkg - package name to download
            @quiet - do not print out any output
            @dependencies - indicator if current downloaded package is a dep
        """
        self.pkg = pkg
        self.quiet = quiet
        self.dependencies = dependencies

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
        pkg = re.findall("\w+", self.pkg)[0]
        for info in members:
            # print("/".join(info.name.split("/")[1:]))
            # print(self.pkg)
            if "/".join(info.name.split("/")[1:]) in [
                "{}.egg-info/requires.txt".format(pkg),
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
                download = DownloadPackage(dep, quiet=True, dependencies=True)
                download()

        tar.close()

    def __download(self):
        package = SearchForPackage(PYPI_ENDPOINT)

        for package, extension, link in \
                package(re.findall("\w+", self.pkg)[0]):

            if self.version_check(self.pkg, package):
                link = urljoin(PYPI_ENDPOINT, link, False)
                link = link.replace("../", "")
                if self.dependencies:
                    info = "  Downloading dependency: {}".format(
                        self.pkg.split()[0], **Color)
                    ProgressBar.set_tab = 0

                else:
                    info = "Requested: {} | Downloading: {}".format(
                        self.pkg.split()[0], package, **Color)
                    ProgressBar.set_tab = 0

                # print(info)
                ProgressBar.text = info
                d_file = "repo/{}.{}".format(package, extension)
                if os.path.exists(d_file) is False:
                    urllib.request.urlretrieve(link, d_file,
                                               reporthook=ProgressBar.hook)
                    print()
                else:
                    print("{Red}File {} exists...ignoring".format(d_file,
                                                                  **Color))
                urllib.request.urlcleanup()
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
