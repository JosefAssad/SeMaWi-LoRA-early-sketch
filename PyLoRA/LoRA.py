#!/usr/bin/env python

import urllib2
import json
from PyOIO.organisation import Bruger, ItSystem

class Lora(object):
    """A Lora object represents a single running instance of the LoRa service.
    """

    def __init__(self, host):
        """ Args:
        host:   string - the hostname of the LoRa instance
        """
        self.host = host

        self.brugere = self._populate_org_brugere()
        self.itsystemer = self._populate_org_systemer()

    def _populate_org_systemer(self):
        """creates the objects from /organisation/itsystem?search
        """
        systemer = []
        url = self.host + '/organisation/itsystem?search'
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        guids = data['results'][0]
        for guid in guids:
            systemer.append(ItSystem(self.host, guid))
        return systemer

    def _populate_org_brugere(self):
        """creates the objects from /organisation/bruger?search

        """
        brugere = []
        url = self.host + '/organisation/bruger?search'
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        guids = data['results'][0]
        for guid in guids:
            brugere.append(Bruger(self.host, guid))
        return brugere

    def __repr__(self):
        return 'Lora("%s")' % (self.host)

    def __str__(self):
        return 'Lora: %s' % (self.host)
