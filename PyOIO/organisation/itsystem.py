#!/usr/bin/env python

import urllib2
import json
from PyOIO.OIOCommon import Virkning


class ItSystem(object):
    """It-system
    from: Specifikation af serviceinterface for Organisation. Version 1.1

    This class implements an object model reflecting the OIO It-system class.
    It contains two things only:
    - A GUID
    - A list of ItSystemRegistrering objects
    """

    def __init__(self, host, ID):
        """
        Arguments:
        host:   string - the hostname of the LoRA server
        ID:     string - the GUID uniquely representing the ItSystem
        """
        self.host = host
        self.ID = ID
        self.url = host + '/organisation/itsystem/' + self.ID
        response = urllib2.urlopen(self.url)
        self.json = json.loads(response.read())

        self.registreringer = []
        for registrering in self.json[self.ID][0]['registreringer']:
            self.registreringer.append(ItSystemRegistrering(registrering))

        # TODO below is a total hack and likely to break if you merely look in
        # its direction and raise an eyebrow
        # BEGIN UGLY HACK
        self.brugervendtnoegle = self.registreringer[0].\
                                 attributter['itsystemegenskaber'][0].\
                                 brugervendtnoegle
        self.navn = self.registreringer[0].\
                    attributter['itsystemegenskaber'][0].\
                    itsystemnavn
        # END UGLY HACK

    def __repr__(self):
        # TODO not ideal, but don't think more is pragmatically needed
        return "ItSystem(%s)" % self.ID

    def __str__(self):
        return "ItSystem: %s" % self.ID


class ItSystemRegistrering(object):
    """It-system registrering
    from: Specifikation af serviceinterface for Organisation. Version 1.1

    This class implements a Python object model reflecting the above for the
    It-system registreringclass. The meat of data about an It system is
    contained in these.

    The ItSystem class will contain a list of 1..N of these.

    """

    def __init__(self, data):
        """
        Arguments:
        data: OIO JSON formatted text containing one Registrering
        """

        self.json = data
        self.note = self.json['note'] if self.json['note'] else None
        self.attributter = {}
        self.attributter['itsystemegenskaber'] = self._populate_egenskaber\
                                                 (self.json['attributter']\
                                                  ['itsystemegenskaber'])
        self.tilstande = {}
        self.tilstande['itsystemgyldighed'] = \
            self._populate_gyldighed(self.json['tilstande']\
                                     ['itsystemgyldighed'])
        self.relationer = self._populate_relationer(self.json['relationer'])

    def _populate_relationer(self, data):
        relationer = {}
        types = ['tilhoerer', 'tilknyttedeorganisationer', 'tilknyttedeenheder',
                 'tilknyttedefunktioner', 'tilknyttedeinteressefaelleskaber',
                 'tilknyttedeitsystemer', 'tilknyttedebrugere',
                 'tilknyttedepersoner', 'opgaver', 'systemtyper', 'adresser']
        for type in types:
            if type in data:
                relationer[type] = []
                for relation in data[type]:
                    r = {}
                    r['uuid'] = relation['uuid']
                    r['virkning'] = Virkning(relation['virkning'])
                    relationer[type].append(r)
        return relationer


    def _populate_egenskaber(self, data):
        egenskaber = []
        for egenskab in data:
            egenskaber.append(ItSystemEgenskab(egenskab))
        return egenskaber

    def _populate_gyldighed(self, g_data):
        g_list = []
        for gyldighed in g_data:
            g_list.append(ItSystemGyldighed(gyldighed))
        return g_list

    def __repr__(self):
        # TODO probably don't use this, bound to be ugly
        return "ItSystemRegistrering(%s)" % self.json

    def __str__(self):
        # TODO find better way of identifying the registrering
        # TODO bad assummption that brugervendtnoegle is unique
        key = self.attributter['itsystemegenskaber'][0].brugervendtnoegle
        return "ItSystemRegistrering: %s" % key


class ItSystemEgenskab(object):

    def __init__(self, data):
        self.brugervendtnoegle = data['brugervendtnoegle']
        self.itsystemnavn = data['itsystemnavn']
        self.itsystemtype = data['itsystemtype']
        self.konfigurationreference = data['konfigurationreference']
        self.virkning = Virkning(data['virkning'])


class ItSystemGyldighed(object):

    def __init__(self, data):
        gyldige_tilstande = ['Aktiv', 'Inaktiv']
        if data['gyldighed'] in gyldige_tilstande:
            self.gyldighed = data['gyldighed']
        else:
            raise InvalidOIOException('Invalid gyldighed "%s"' \
                                      % data['gyldighed'])
        self.virkning = Virkning(data['virkning'])


class InvalidOIOException(Exception):

    def __init__(self, e):
        Exception.__init__(self, 'Invalid OIO: %s' % e)
