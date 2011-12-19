#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests out python-elections

Most requests require authentication with, so you'll need to provide that in
a file called private_settings.py with AP_USERNAME and AP_PASSWORD
"""
import os
import unittest
from elections import AP
from datetime import date
from elections.ap import Candidate, Race, ReportingUnit, Result, State
from elections.ap import FileDoesNotExistError, BadCredentialsError
from private_settings import AP_USERNAME, AP_PASSWORD


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.client = AP(AP_USERNAME, AP_PASSWORD)


class APTest(BaseTest):
    
    def test_badlogin(self):
        client = AP("foo", "bar")
        self.assertRaises(BadCredentialsError, client.get_state, "IA")

    def test_badstate(self):
        self.assertRaises(FileDoesNotExistError, self.client.get_state, "XYZ")
    
    def test_getstate(self):
        # Pull state
        self.iowa = self.client.get_state("IA")
        
        # Races
        race_list = self.iowa.races
        self.assertTrue(isinstance(race_list, list))
        self.assertTrue(len(race_list) > 0)
        self.assertTrue(isinstance(race_list[0], Race))
        self.assertEqual(self.iowa.get_race(race_list[0].ap_race_number), race_list[0])
        self.assertRaises(KeyError, self.iowa.get_race, 'foo')
        self.assertEqual(
            self.iowa.filter_races(office_name='President', party='GOP')[0],
            race_list[0],
        )
#        self.assertEqual(
#            len(self.iowa.filter_races(office_name='President', party='Dem')),
#            0,
#        )
        race = self.iowa.races[0]
        self.assertTrue(isinstance(race.ap_race_number, basestring))
        self.assertTrue(isinstance(race.office_name, basestring))
        self.assertTrue(isinstance(race.office_description, basestring))
        self.assertTrue(isinstance(race.office_id, basestring))
        self.assertTrue(isinstance(race.seat_name, basestring))
        self.assertTrue(isinstance(race.seat_number, basestring))
        self.assertTrue(isinstance(race.scope, basestring))
        self.assertTrue(isinstance(race.date, date))
        self.assertTrue(isinstance(race.num_winners, int))
        self.assertTrue(isinstance(race.race_type, basestring))
        self.assertTrue(isinstance(race.party, basestring))
        self.assertTrue(isinstance(race.uncontested, bool))
        self.assertTrue(isinstance(race.name, basestring))
        self.assertTrue(isinstance(race.race_type_name, basestring))
        self.assertTrue(isinstance(race.is_primary, bool))
        self.assertTrue(isinstance(race.is_caucus, bool))
        self.assertTrue(isinstance(race.is_general, bool))
        
        # Reporting units
        ru_list = self.iowa.reporting_units
        self.assertTrue(isinstance(ru_list, list))
        self.assertTrue(len(ru_list) > 0)
        self.assertTrue(isinstance(ru_list[0], ReportingUnit))
        self.assertEqual(self.iowa.get_reporting_unit(ru_list[0].fips), ru_list[0])
        self.assertRaises(KeyError, self.iowa.get_reporting_unit, 'foo')
        self.assertTrue(isinstance(ru_list[0], ReportingUnit))
        self.assertTrue(isinstance(ru_list[0].ap_number, basestring))
        self.assertTrue(isinstance(ru_list[0].name, basestring))
        self.assertTrue(isinstance(ru_list[0].abbrev, basestring))
        self.assertTrue(isinstance(ru_list[0].fips, basestring))
        self.assertTrue(isinstance(ru_list[0].num_reg_voters, int))
        self.assertTrue(isinstance(ru_list[0].precincts_total, int))
        self.assertTrue(isinstance(ru_list[0].precincts_reporting, type(None)))
        self.assertTrue(isinstance(ru_list[0].precincts_reporting_percent, type(None)))
        ru_list = self.iowa.races[0].reporting_units
        self.assertTrue(isinstance(ru_list, list))
        self.assertTrue(len(ru_list) > 0)
        for ru in ru_list:
            self.assertTrue(isinstance(ru, ReportingUnit))
            self.assertTrue(isinstance(ru.ap_number, basestring))
            self.assertTrue(isinstance(ru.name, basestring))
            self.assertTrue(isinstance(ru.abbrev, basestring))
            self.assertTrue(isinstance(ru.fips, basestring))
            self.assertTrue(isinstance(ru.num_reg_voters, int))
            self.assertTrue(isinstance(ru.precincts_total, int))
            self.assertTrue(isinstance(ru.precincts_reporting, int))
            self.assertTrue(isinstance(ru.precincts_reporting_percent, float))
            self.assertTrue(isinstance(ru.results[0], Result))
            # Results
            for result in ru.results:
                self.assertTrue(isinstance(result, Result))
                self.assertTrue(isinstance(result.candidate, Candidate))
                self.assertEqual(result.reporting_unit, ru)
                self.assertTrue(isinstance(result.vote_total, int))
                self.assertTrue(isinstance(result.vote_total_percent, float))
        
        # Counties
        county_list = self.iowa.races[0].counties
        self.assertEqual(type(county_list), type([]))
        self.assertEqual(len(county_list) == 99, True)
        self.assertEqual(type(county_list[0]), ReportingUnit)
        self.assertEqual(county_list[0].is_state, False)
        
        # State
        state = self.iowa.races[0].state
        self.assertEqual(type(state), ReportingUnit)
        self.assertEqual(state.is_state, True)
        
        # Candidates
        cand_list = self.iowa.races[0].candidates
        self.assertTrue(isinstance(race.candidates, list))
        self.assertTrue(len(cand_list) > 0)
        for cand in cand_list:
            self.assertTrue(isinstance(cand, Candidate))
            self.assertTrue(isinstance(cand.first_name, basestring))
            self.assertTrue(isinstance(cand.middle_name, basestring))
            self.assertTrue(isinstance(cand.last_name, basestring))
            self.assertTrue(isinstance(cand.abbrev_name, basestring))
            self.assertTrue(isinstance(cand.suffix, basestring))
            self.assertTrue(isinstance(cand.use_suffix, bool))
            self.assertTrue(isinstance(cand.ap_natl_number, basestring))
            self.assertTrue(isinstance(cand.ap_polra_number, basestring))
            self.assertTrue(isinstance(cand.ap_pol_number, basestring))
            self.assertTrue(isinstance(cand.party, basestring))
            self.assertTrue(isinstance(cand.is_winner, bool))
            self.assertTrue(isinstance(cand.is_runoff, bool))
            self.assertTrue(isinstance(cand.delegates, int))
            self.assertTrue(isinstance(cand.name, basestring))
        
        # FTP hits
        self.assertEqual(self.client._ftp_hits, 1)
    
    def test_getstates(self):
        # Pull states
        self.first_two = self.client.get_states("IA", "NH")
        self.assertEqual(type(self.first_two), type([]))
        self.assertEqual(len(self.first_two), 2)
        [self.assertEqual(type(i), State) for i in self.first_two]
        
        # FTP hits
        self.assertEqual(self.client._ftp_hits, 1)


if __name__ == '__main__':
    unittest.main()

