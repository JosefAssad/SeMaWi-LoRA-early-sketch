#!/usr/bin/env python

import urllib2
import json
from PyOIO.OIOCommon import Virkning


class Bruger(object):
    """Represents the OIO information model 1.1 Bruger
    https://digitaliser.dk/resource/991439

    """

    def __init__(self, host, ID):
        """ Args:
        host:   string - the hostname of the LoRA server
        ID:     string - the GUID uniquely representing the Bruger
        """
        self.host = host
        self.ID = ID
        self.url = host + '/organisation/bruger/' + self.ID

        response = urllib2.urlopen(self.url)
        self.json = json.loads(response.read())

        self.registreringer = self._populate_registreringer()

    def _populate_registreringer(self):
        registreringer = []
        registrering_number = 0 # in lieu of unique identifiers
        for registrering in self.json[self.ID][0]['registreringer']:
            registreringer.append(BrugerRegistrering(self.ID,
                                                     registrering_number,
                                                     registrering))
            registrering_number += 1
        return registreringer

    def __repr__(self):
        return 'Bruger("%s", "%s"")' % (self.host, self.ID)

    def __str__(self):
        return 'Bruger: %s' % self.ID


class BrugerRegistrering(object):

    def __init__(self, ID, registrering_number, json):
        # TODO fratidspunkt
        # TODO Relationer
        self.ID = ID # which user is this registrering about
        self.json = json
        self.registrering_number = registrering_number
        self.attributter = self._populate_attributter(self.json['attributter'])
        self.livscykluskode = self.json['livscykluskode']
        self.note = self.json['note']
        self.tilstande = self._populate_brugergyldighed(self.json['tilstande'])

    def _populate_brugergyldighed(self, json):
        brugergyldigheder = []
        for brugergyldighed in json['brugergyldighed']:
            brugergyldigheder.append(BrugerGyldighed(self.ID, brugergyldighed))
        return brugergyldigheder
        
    def _populate_attributter(self, json):
        attributter = BrugerAttributListe(self.ID, json)
        return attributter

    def __repr__(self):
        return 'BrugerRegistrering("%s", %s)' % (self.ID,
                                                 self.registrering_number)

    def __str__(self):
        return 'BrugerRegistrering: Bruger "%s", Nr. %s' % (self.ID,
                                                 self.registrering_number)


class BrugerAttributListe(object):
    """ Container for a list of 1..* BrugerEgenskaber objects.
    There should be exactly one of these objects per BrugerRegistrering

    Args:
    ID: string - Bruger GUID
    json: the relevant json data

    """

    def __init__(self, ID, json):
        self.ID = ID
        self.json = json
        self.brugeregenskaber = self._populate_brugeregenskaber(self.json)

    def _populate_brugeregenskaber(self, json):
        # TODO must be minimum 1 brugeregenskab; 1..*
        brugeregenskaber = []
        for brugeregenskab in json['brugeregenskaber']:
            brugeregenskaber.append(BrugerEgenskaber(brugeregenskab))
        return brugeregenskaber

    def __repr__(self):
        return 'BrugerAttributListe("%s")' % (self.ID)

    def __str__(self):
        return 'BrugerAttributListe: Bruger "%s"' % (self.ID)


class BrugerGyldighed(object):
    """ Glorified dictionary with two elements: a Virkning object and
    a Status limited to Aktiv and Inaktiv

    Args:
    ID: string - Bruger GUID
    json: the relevant json data
    """

    def __init__(self, ID, json):
        self.ID = ID
        self.json = json
        if self.json['gyldighed'] in ['Aktiv', 'Inaktiv']:
            self.gyldighed = self.json['gyldighed']
        else:
            # TODO throw a descriptive error
            self.gyldighed = "ERROR"
        self.virkning = Virkning(self.json['virkning'])


class BrugerEgenskaber(object):
    """Direct properties of the Bruger in question.

    """

    def __init__(self, json):
        """Args:

        json: the dictionary directly under the 'attributter' entry
        """
        self.brugernavn = json['brugernavn'] # 0..1
        self.brugervendtnoegle = json['brugervendtnoegle'] # 0..1
        self.virkning = Virkning(json['virkning'])

        if 'brugertype' in json.keys():
            self.brugertype = json['brugertype']
        else:
            self.brugertype = None

    def __repr__(self):
        return 'BrugerEgenskaber("%s", "%s")' % (self.brugernavn,
                                                 self.brugervendtnoegle)

    def __str__(self):
        return 'BrugerEgenskaber: Bruger "%s" - "%s"' % (self.brugernavn,
                                                         self.brugervendtnoegle)

