# Created By: Virgil Dupras
# Created On: 2008-06-13
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from hsutil.currency import USD, CAD

from .base import TestCase, TestQIFExportImportMixin
from ..model.account import INCOME

class OneEmptyAccount(TestCase):
    def setUp(self):
        self.create_instances()
        self.add_account('Checking')
    
    def test_add_entry_check_splits(self):
        """A newly added entry has its splits set"""
        # Previously, split_count() would be zero until a save_entry()
        self.etable.add()
        self.tpanel.load()
        self.assertEqual(len(self.stable), 2)
        self.assertEqual(self.stable[0].account, 'Checking')
        self.assertEqual(self.stable[0].debit, '')
        self.assertEqual(self.stable[0].credit, '')
        self.assertEqual(self.stable[1].account, '')
        self.assertEqual(self.stable[1].debit, '')
        self.assertEqual(self.stable[1].credit, '')
    
    def test_add_entry_save_split(self):
        """Saving a split in a newly added entry doesn't make it disappear"""
        # Previously, saving splits to a newly created entry would make it disappear because the
        # cooking would be made before the transaction could be added
        self.etable.add()
        self.tpanel.load()
        self.stable.add()
        self.stable.save_edits()
        self.tpanel.save()
        self.assertEqual(len(self.etable), 1)
    

class OneEntry(TestCase):
    def setUp(self):
        self.create_instances()
        self.add_account('Checking')
        self.add_entry('10/10/2007', 'Deposit', transfer='Salary', increase='42.00')
    
    def test_save_split_on_second_row(self):
        """save_split() doesn't change the selected row"""
        self.tpanel.load()
        self.stable.select([1])
        row = self.stable.selected_row
        row.account = 'foobar'
        self.stable.save_edits()
        self.assertEqual(self.stable.selected_index, 1)
    
    def test_split(self):
        """There are two splits and the attributes are correct"""
        self.tpanel.load()
        self.assertEqual(len(self.stable), 2)
        self.assertEqual(self.stable[0].account, 'Checking')
        self.assertEqual(self.stable[0].debit, '42.00')
        self.assertEqual(self.stable[1].account, 'Salary')
        self.assertEqual(self.stable[1].credit, '42.00')

    def test_set_split_credit(self):
        """Setting the split credit changes the split credit, the entry amount and the balance"""
        self.tpanel.load()
        row = self.stable.selected_row
        row.credit = '100.00'
        self.stable.save_edits()
        self.tpanel.save()
        self.assertEqual(self.stable[0].credit, '100.00')
        self.assertEqual(self.stable[1].debit, '')
        self.assertEqual(self.etable[0].decrease, '100.00')
        self.assertEqual(self.etable[0].balance, '-100.00')
    
    def test_set_split_debit(self):
        """Setting the split debit changes the split debit, the entry amount and the balance"""
        self.tpanel.load()
        row = self.stable.selected_row
        row.debit = '100.00'
        self.stable.save_edits()
        self.tpanel.save()
        self.assertEqual(self.stable[0].debit, '100.00')
        self.assertEqual(self.etable[0].increase, '100.00')
        self.assertEqual(self.etable[0].balance, '100.00')
    
    def test_set_split_account(self):
        """Setting the split account changes both the split and the entry.
        If the current entry's account is changed, the account selection
        changes too."""
        self.tpanel.load()
        row = self.stable.selected_row
        row.account = 'foo'
        self.stable.save_edits()
        self.tpanel.save()
        self.mainwindow.select_balance_sheet()
        self.assertEqual(self.bsheet.assets[1].name, 'foo') # The foo account was autocreated
        self.bsheet.selected = self.bsheet.assets[1]
        self.bsheet.show_selected_account()
        self.tpanel.load()
        self.stable.select([1])
        row = self.stable.selected_row
        row.account = 'bar'
        self.stable.save_edits()
        self.tpanel.save()
        self.assertEqual(self.stable[1].account, 'bar')
        self.assertEqual(self.etable[0].transfer, 'bar')
        self.mainwindow.select_income_statement()
        self.assertEqual(self.istatement.income[0].name, 'bar') # The bar account was autocreated
    

class EntryWithoutTransfer(TestCase):
    """An entry without a transfer account set"""
    def setUp(self):
        self.create_instances()
        self.add_account()
        self.add_entry(description='foobar', decrease='130.00')
    
    def test_split(self):
        """There are two splits and their amounts and accounts are correct"""
        self.tpanel.load()
        self.assertEqual(len(self.stable), 2)
        self.assertEqual(self.stable[0].account, 'New account')
        self.assertEqual(self.stable[0].credit, '130.00')
        self.assertEqual(self.stable[1].account, '')
        self.assertEqual(self.stable[1].debit, '130.00')
    

class _SplitTransaction(TestCase):
    def setUp(self):
        # New Account   0 100
        # expense1    100   0
        # expense2     10   0
        # income        0   1
        # Unassigned    0   9
        self.create_instances()
        self.add_account()
        self.add_entry(date='2/1/2007', description='Split', transfer='expense1', decrease='100')
        self.add_entry(date='3/1/2007')   # That's to make sur the selection doesn't change on edits
        self.etable.select([0])
        self.tpanel.load()
        self.stable.add()
        row = self.stable.selected_row
        row.account = 'expense2'
        row.memo = 'some memo'
        row.debit = '10'
        self.stable.save_edits()
        self.stable.select([3])
        row = self.stable.selected_row
        row.account = 'income'
        row.credit = '1'
        self.stable.save_edits()
        self.tpanel.save()
    

class SplitTransaction(_SplitTransaction):
    def test_amounts(self):
        """All split amounts are right"""
        self.tpanel.load()
        self.assertEqual(self.stable[0].credit, '100.00')
        self.assertEqual(self.stable[1].debit, '100.00')
        self.assertEqual(self.stable[2].debit, '10.00')
        self.assertEqual(self.stable[3].credit, '1.00')
        self.assertEqual(self.stable[4].credit, '9.00')
        self.assertEqual(self.etable[0].decrease, '100.00')
    
    def test_delete_split(self):
        """Deleting a split works"""
        self.tpanel.load()
        self.stable.select([2])
        self.stable.delete()
        self.assertEqual(len(self.stable), 4)
        self.assertEqual(self.stable[2].account, 'income')
        self.assertEqual(self.stable[2].credit, '1.00')
        self.assertEqual(self.stable[3].debit, '1.00')

    def test_revert_split(self):
        """Reverting the edits works"""
        self.tpanel.load()
        row = self.stable.selected_row
        row.account = 'changed'
        row.debit = '2'
        self.stable.cancel_edits()
        self.assertEqual(self.stable[3].account, 'income')
        self.assertEqual(self.stable[3].credit, '1.00')

    def test_save_entry(self):
        """Saving an entry doesn't change the amounts"""
        row = self.etable.selected_row
        row.description = 'Another description'
        self.etable.save_edits()
        self.tpanel.load()
        self.assertEqual(len(self.stable), 5)
        self.assertEqual(self.stable[0].credit, '100.00')
        self.assertEqual(self.stable[1].debit, '100.00')
        self.assertEqual(self.stable[2].debit, '10.00')
        self.assertEqual(self.stable[3].credit, '1.00')
        self.assertEqual(self.stable[4].credit, '9.00')

    def test_select_another_entry(self):
        """Selecting another entry resets the split index to 0"""
        self.etable.select([1])
        self.tpanel.load()
        self.assertEqual(self.stable.selected_index, 0)
    
    def test_set_unassigned_amount(self):
        """When seeting the amount of an Unnasigned split, that amount is not touched by balance()
        when needed, create a new Unassigned split."""
        self.tpanel.load()
        self.stable.select([4])
        row = self.stable.selected_row
        row.credit = '10'
        self.stable.save_edits()
        self.assertEqual(self.stable[4].credit, '10.00')
        self.assertEqual(len(self.stable), 6)
        self.assertEqual(self.stable[5].debit, '1.00')
    
    def test_split_count(self):
        """All splits are shown"""
        self.tpanel.load()
        self.assertEqual(len(self.stable), 5)

    def test_transfer_read_only(self):
        """The transfer column shows a list of affecter *other* accounts and is read-only"""
        self.assertEqual(self.etable[0].transfer, 'expense1, expense2, income')
        self.assertFalse(self.etable.can_edit_column('transfer'))


class SplitWithNoAccount(TestCase):
    """A split transaction containing a split that has a None account"""
    def setUp(self):
        self.create_instances()
        self.add_account()
        self.add_entry(date='2/1/2007', description='Split', transfer='expense1', decrease='100')
        self.tpanel.load()
        self.stable.add()
        row = self.stable.selected_row
        row.credit = '10'
        self.stable.save_edits()
        self.tpanel.save()
    
    def test_transfer(self):
        """The transfer column don't include splits with no account"""
        self.assertEqual(self.etable[0].transfer, 'expense1')
    

class CADAssetAndUSDIncome(TestCase):
    def setUp(self):
        self.create_instances()
        self.add_account('CAD Account', CAD)
        self.add_account('USD Income', USD, account_type=INCOME)
        self.add_entry(transfer='CAD Account', increase='42')
    
    def test_set_split_amount(self):
        """When setting an amount through the split interface, currencies can be set at will."""
        # USD Income: credit 42 USD
        # CAD Account: debit 42 USD
        self.tpanel.load()
        self.stable.select([1])
        row = self.stable.selected_row
        row.debit = '40'
        self.stable.save_edits()
        self.tpanel.save()
        self.assertEqual(self.etable[0].increase, '42.00')
    

class SplitWithZeroAmounts(TestCase, TestQIFExportImportMixin):
    def setUp(self):
        self.create_instances()
        self.add_account('foo')
        self.add_entry(date='2/1/2007', description='Split', transfer='bar')
        self.tpanel.load()
        self.stable.add()
        row = self.stable.selected_row
        row.account = 'baz'
        self.stable.save_edits()
        self.tpanel.save()
    