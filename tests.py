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
from elections.ap import Candidate, Race, ReportingUnit, Result, State
from elections.ap import FileDoesNotExistError
from private_settings import AP_USERNAME, AP_PASSWORD


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.client = AP(AP_USERNAME, AP_PASSWORD)


class StateTest(BaseTest):
    
    def test_badstate(self):
        self.assertRaises(FileDoesNotExistError, self.client.get_state, "XYZ")
    
    def test_getstate(self):
        # Pull state
        self.iowa = self.client.get_state("IA")
        
        # Races
        race_list = self.iowa.races
        self.assertEqual(type(race_list), type([]))
        self.assertEqual(len(race_list) > 0, True)
        self.assertEqual(type(race_list[0]), Race)
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
        
        # Reporting units
        ru_list = self.iowa.reporting_units
        self.assertEqual(type(ru_list), type([]))
        self.assertEqual(len(ru_list) > 0, True)
        self.assertEqual(type(ru_list[0]), ReportingUnit)
        self.assertEqual(self.iowa.get_reporting_unit(ru_list[0].fips), ru_list[0])
        self.assertRaises(KeyError, self.iowa.get_reporting_unit, 'foo')
        
        # Candidates
        cand_list = self.iowa.races[0].candidates
        self.assertEqual(type(cand_list), type([]))
        self.assertEqual(len(cand_list) > 0, True)
        self.assertEqual(type(cand_list[0]), Candidate)
        
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

