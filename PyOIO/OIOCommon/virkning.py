#!/usr/bin/env python

class Virkning(object):
    """ Virkning is a fairly broadly used class. Its purpose when attached to
    metadata is to lend the metadata bitemporality.
    """

    def __init__(self, json):
        """Args:

        json: (dictionary) data containing the attributes of the Virkning object
        """
        # TODO below might need to live with missing elements?
        self.aktoerref = json['aktoerref']
        if 'aktoertypekode' in json:
            self.aktoertypekode = json['aktoertypekode']
        else:
            self.aktoertypekode = None
        self.virkning_from = json['from']
        if 'from_included' in json:
            self.virkning_from_included = json['from_included']
        else:
            self.virkning_from_included = None
        self.virkning_to = json['to']
        if 'to_included' in json:
            self.virkning_to_included = json['to_included']
        else:
            self.virkning_to_included = None
        if 'notetekst' in json:
            self.notetekst = json['notetekst']
        else:
            self.notetekst = None
        # TODO timestamps for virkning_from and virkning_to

    def __repr__(self):
        return 'Virkning(%s, %s)' % (self.virkning_from, self.virkning_to)

    def __str__(self):
        return 'Virkning: %s - %s' % (self.virkning_from, self.virkning_to)
