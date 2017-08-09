"""Common utility routines used by the FAST pipeline modules"""

import ConfigParser

# ConfigParser enhancements to get list of objects

def _list(s):
    return map(lambda x: x.strip(), s.strip(' []').split(','))

def _intlist(s):
    return map(int, _list(s))

def _floatlist(s):
    return map(float, _list(s))

class ListAwareMixIn(object):

    def getlist(self, section, option):
        return self._get(section, _list, option)

    def getintlist(self, section, option):
        return self._get(section, _intlist, option)

    def getfloatlist(self, section, option):
        return self._get(section, _floatlist, option)

class RawConfigParser(ConfigParser.RawConfigParser, ListAwareMixIn): pass
class ConfigParser(ConfigParser.ConfigParser, ListAwareMixIn): pass
class SafeConfigParser(ConfigParser.SafeConfigParser, ListAwareMixIn): pass

