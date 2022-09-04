from azbankgateways.bankfactories import BankFactory
from azbankgateways.models import BankType
from .banks import MyBaseBank

import logging


class MyBankFactory(BankFactory):

    def __init__(self):
        BankFactory.__init__(self)

    def create(self, bank_type: BankType = None, identifier: str = '1') -> MyBaseBank:
        """Build bank class"""
        if not bank_type:
            bank_type = self._secret_value_reader.default(identifier)
        logging.debug('Request create bank', extra={'bank_type': bank_type})

        bank_klass, bank_settings = self._import_bank(bank_type, identifier)
        bank = bank_klass(**bank_settings, identifier=identifier)
        bank.set_currency(self._secret_value_reader.currency(identifier))

        logging.debug('Create bank')
        return bank