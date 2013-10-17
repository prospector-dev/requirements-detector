"""
This module represents the various types of requirement that can be specified for
a project. It is somewhat redundant to re-implement here as we could use
`pip.req.InstallRequirement`, but that would require depending on pip which is not
easy to do since it will usually be installed by the user at a specific version.
Additionally, the pip implementation has a lot of extra features that we don't need -
we don't expect relative file paths to exist, for example.
"""
import os
import re
import urlparse
from pkg_resources import Requirement


def _is_filepath(req):
    # this is (probably) a file
    return os.path.sep in req or req.startswith('.')


def _parse_egg_name(url_fragment):
    """
    >>> _parse_egg_name('egg=fish&cake=lala')
    fish
    >>> _parse_egg_name('something_spurious')
    None
    """
    if '=' not in url_fragment:
        return None
    parts = urlparse.parse_qs(url_fragment)
    if 'egg' not in parts:
        return None
    return parts['egg'][0]  # taking the first value mimics pip's behaviour


def _strip_fragment(urlparts):
    new_urlparts = (
        urlparts.scheme,
        urlparts.netloc,
        urlparts.path,
        urlparts.params,
        urlparts.query,
        None
    )
    return urlparse.urlunparse(new_urlparts)


class DetectedRequirement(object):

    def __init__(self, name, version_specs=None, url=None):
        self.name = name
        self.version_specs = version_specs
        self.url = url

    def __str__(self):
        rep = self.name or 'Unknown'
        if self.version_specs:
            specs = ','.join(['%s%s' % (comp, version) for comp, version in self._version_specs])
            rep = '%s%s' % (rep, specs)
        if self.url:
            rep = '%s (%s)' % self.url
        return rep

    def __eq__(self, other):
        return self.name == other.name and self.url == other.url and self.version_specs == other.version_specs

    @staticmethod
    def parse(line):
        # the options for a Pip requirements file are:
        #
        # 1) <dependency_name>
        # 2) <dependency_name><version_spec>
        # 3) <vcs_url>(#egg=<dependency_name>)?
        # 4) <url_to_archive>(#egg=<dependency_name>)?
        # 5) <path_to_dir>
        # 6) (-e|--editable) <path_to_dir>(#egg=<dependency_name)?
        # 7) (-e|--editable) <vcs_url>#egg=<dependency_name>
        line = line.strip()

        if line.startswith('-e') or line.startswith('--editable'):
            # strip the editable flag
            line = re.sub('^.* ', '', line)

        url = urlparse.urlparse(line)

        if url.scheme == '' and not _is_filepath(line):
            # if we are here, it is a simple dependency
            req = Requirement.parse(line)
            return DetectedRequirement(req.key, version_specs=req.specs)

        # otherwise, this is some kind of URL
        name = _parse_egg_name(url)
        url = _strip_fragment(url)
        return DetectedRequirement(name=name, url=url)