"""Test module for nested_dict."""
from __future__ import print_function


import unittest
import sys
import os


# make sure which nested_dict we are testing
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)


class Test_nested_dict_constructor(unittest.TestCase):
    """Test nested_dict constructor parameters."""

    def test_default(self):
        """Test constructor without parameters."""
        from nested_dict import nested_dict
        nd = nested_dict()
        nd['new jersey']['mercer county']['plumbers'] = 3
        nd['new jersey']['mercer county']['programmers'] = 81
        nd['new jersey']['middlesex county']['programmers'] = 81
        nd['new jersey']['middlesex county']['salesmen'] = 62
        nd['new york']['queens county']['plumbers'] = 9
        nd['new york']['queens county']['salesmen'] = 36

        expected_result = sorted([
            (('new jersey', 'mercer county', 'plumbers'), 3),
            (('new jersey', 'mercer county', 'programmers'), 81),
            (('new jersey', 'middlesex county', 'programmers'), 81),
            (('new jersey', 'middlesex county', 'salesmen'), 62),
            (('new york', 'queens county', 'plumbers'), 9),
            (('new york', 'queens county', 'salesmen'), 36),
        ])
        all = sorted(tup for tup in nd.iteritems_flat())
        self.assertEqual(all, expected_result)
        all = sorted(tup for tup in nd.items_flat())
        self.assertEqual(all, expected_result)

    def test_bad_init(self):
        """Test with invalid constructor parameters."""
        #
        #   Maximum of four levels
        #
        import nested_dict
        try:
            nd3 = nested_dict.nested_dict(1, 2, 3)
            self.assertTrue("Should have throw assertion before getting here")
            # just so flake8 stops complaining!
            nd3[1][2][3] = "b"
        except Exception:
            pass
        #
        #   levels not int
        #
        import nested_dict
        try:
            nd2 = nested_dict.nested_dict("a", "b")
            self.assertTrue("Should have throw assertion before getting here")
            # just so flake8 stops complaining!
            nd2[1][2] = "b"
        except Exception:
            pass

    def test_fixed_nesting(self):
        """Fixed levels of nesting, no type specified."""
        #
        #   Maximum of four levels
        #
        import nested_dict
        nd4 = nested_dict.nested_dict(4)
        # OK: Assign to "string"
        nd4[1][2][3][4] = "a"

        # Bad: Five levels is one too many
        try:
            nd4[1][2][3]["four"][5] = "b"
            self.assertTrue("Should have throw assertion before getting here")
        except KeyError:
            pass

        nd2 = nested_dict.nested_dict(2)
        # OK: Assign to "string"
        nd2[1][2] = "a"

        # Bad: Five levels is one too many
        try:
            nd2[1]["two"][3] = "b"
            self.assertTrue("Should have throw assertion before getting here")
        except KeyError:
            pass

    def test_list(self):
        """Test with nested type of `list`."""
        import nested_dict
        nd = nested_dict.nested_dict(2, list)
        nd['new jersey']['mercer county'].append('plumbers')
        nd['new jersey']['mercer county'].append('programmers')
        nd['new jersey']['middlesex county'].append('salesmen')
        nd['new jersey']['middlesex county'].append('staff')
        nd['new york']['queens county'].append('cricketers')
        all = sorted(tup for tup in nd.iteritems_flat())
        self.assertEqual(all, [(('new jersey', 'mercer county'), ['plumbers', 'programmers']),
                               (('new jersey', 'middlesex county'), ['salesmen', 'staff']),
                               (('new york', 'queens county'), ['cricketers']),
                               ])
        all = sorted(tup for tup in nd.itervalues_flat())
        self.assertEqual(all, [['cricketers'],
                               ['plumbers', 'programmers'],
                               ['salesmen', 'staff']])
        all = sorted(tup for tup in nd.values_flat())
        self.assertEqual(all, [['cricketers'],
                               ['plumbers', 'programmers'],
                               ['salesmen', 'staff']])
        all = sorted(tup for tup in nd.iterkeys_flat())
        self.assertEqual(all, [('new jersey', 'mercer county'),
                               ('new jersey', 'middlesex county'),
                               ('new york', 'queens county')])
        all = sorted(tup for tup in nd.keys_flat())
        self.assertEqual(all, [('new jersey', 'mercer county'),
                               ('new jersey', 'middlesex county'),
                               ('new york', 'queens county')])

        self.assertEqual(nd, {"new jersey": {"mercer county": ["plumbers",
                                                               "programmers"],
                                             "middlesex county": ["salesmen",
                                                                  "staff"]},
                              "new york": {"queens county": ["cricketers"]}})


class Test_nested_dict_methods(unittest.TestCase):
    """Test methods of nested_dict."""

    def test_iteritems_flat(self):
        """Test iteritems_flat method."""
        import nested_dict
        a = nested_dict.nested_dict()
        a['1']['2']['3'] = 3
        a['A']['B'] = 15
        self.assertEqual(sorted(a.iteritems_flat()), [(('1', '2', '3'), 3), (('A', 'B'), 15)])

    def test_iterkeys_flat(self):
        """Test iterkeys_flat method."""
        import nested_dict
        a = nested_dict.nested_dict()
        a['1']['2']['3'] = 3
        a['A']['B'] = 15
        self.assertEqual(sorted(a.iterkeys_flat()), [('1', '2', '3'), ('A', 'B')])

    def test_itervalues_flat(self):
        """Test itervalues_flat method."""
        import nested_dict
        a = nested_dict.nested_dict()
        a['1']['2']['3'] = 3
        a['A']['B'] = 15
        self.assertEqual(sorted(a.itervalues_flat()), [3, 15])

    def test_to_dict(self):
        """Test to_dict method."""
        import nested_dict
        a = nested_dict.nested_dict()
        a['1']['2']['3'] = 3
        a['A']['B'] = 15

        normal_dict = a.to_dict()
        self.assertEqual(normal_dict, {'1': {'2': {'3': 3}}, 'A': {'B': 15}})

        b = nested_dict.nested_dict(normal_dict)
        self.assertEqual(b, {'1': {'2': {'3': 3}}, 'A': {'B': 15}})

    def test_str(self):
        """Test __str__ method."""
        import nested_dict
        import json
        a = nested_dict.nested_dict()
        a['1']['2']['3'] = 3
        a['A']['B'] = 15
        self.assertEqual(json.loads(str(a)), {'1': {'2': {'3': 3}}, 'A': {'B': 15}})

    def test_update(self):
        """Test update method."""
        import nested_dict

        #
        #   nested dictionary updates
        #
        d1 = nested_dict.nested_dict()
        d2 = nested_dict.nested_dict()
        d1[1][2][3] = 4
        d2[1][2][4] = 5
        d1.update(d2)
        d1.to_dict()
        self.assertEqual(d1.to_dict(), {1: {2: {3: 4, 4: 5}}})

        #
        #   dictionary updates
        #
        d1 = nested_dict.nested_dict()
        d2 = {1: {2: {4: 5}}}
        d1[1][2][3] = 4
        d2[1][2][4] = 5
        d1.update(d2)
        d1.to_dict()
        self.assertEqual(d1.to_dict(), {1: {2: {3: 4, 4: 5}}})

        #
        #   scalar overwrites
        #
        d1 = nested_dict.nested_dict()
        d2 = nested_dict.nested_dict()
        d1[1][2][3] = 4
        d2[1][2] = 5
        d1.update(d2)
        d1.to_dict()
        self.assertEqual(d1.to_dict(), {1: {2: 5}})

        #
        #   updates try to preserve the sort of nested_dict
        #
        d1 = nested_dict.nested_dict(3, int)
        d2 = nested_dict.nested_dict()
        d1[1][2][3] = 4
        d1[1][2][4] = 5
        d2[2][3][4][5] = 6
        d1.update(d2)
        d1.to_dict()
        self.assertEqual(d1.to_dict(), {1: {2: {3: 4, 4: 5}}, 2: {3: {4: {5: 6}}}})
        # d1[2][3][4][5] = 6 but d1[2][3][4] should still be a default dict of int
        self.assertEqual(d1[2][3][5], 0)

        #
        #   updates try to preserve the sort of nested_dict
        #
        d1 = nested_dict.nested_dict(3, list)
        d2 = {2: {3: {4: {5: 6}}}}
        d1[1][2][3].append(4)
        d1[1][2][4].append(4)
        d1.update(d2)
        d1.to_dict()
        self.assertEqual(d1.to_dict(), {1: {2: {3: [4], 4: [4]}}, 2: {3: {4: {5: 6}}}})
        # d1[2][3][4][5] = 6 but d1[2][3][5] should still be a default dict of list
        d1[2][3][5].append(4)
        self.assertEqual(d1.to_dict(), {1: {2: {3: [4], 4: [4]}}, 2: {3: {4: {5: 6}, 5: [4]}}})

    def test_update_with_combine_policies(self):
        """Test update with combine_policies"""
        import nested_dict

        #
        # uniquely_extend_list
        #
        nd1 = nested_dict.nested_dict({'a':1,'f':[1,3,3]})
        nd2 = nested_dict.nested_dict({'a':1,'f':[1,2]})
        nd1.update(nd2, combine_policies=['uniquely_extend_list'])
        self.assertEqual(nd1.to_dict(), {'a':1,'f':[1,3,3,2]})

        #
        # list_of_union
        #
        nd1 = nested_dict.nested_dict({'a':1,'f':[1,3,3]})
        nd2 = nested_dict.nested_dict({'a':1,'f':[1,2]})
        nd1.update(nd2, combine_policies=['sorted_list_of_union'])
        self.assertEqual(nd1.to_dict(), {'a':1,'f':[1,2,3]})

        #
        # custom_combine_policy
        #
        combine_policy_options=[
                  {'name': 'rabbits', 'signature': (list,list), 
                   'combiner': lambda x,y: 'look rabbits' }
                ]
        nd1 = nested_dict.nested_dict({'a':1,'f':[1,3,3]})
        nd2 = nested_dict.nested_dict({'a':1,'f':[1,2]})
        nd1.update(nd2, combine_policies=['rabbits'], combine_policy_options=combine_policy_options)
        self.assertEqual(nd1.to_dict(), {'a':1,'f':'look rabbits'})