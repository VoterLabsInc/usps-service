from unittest import TestCase

from usps_service.address_standardizer import AddressStandardizer


class TestUSPS(TestCase):
    """
    Test the USPS Address Standardizer
    run using python -m nose path/to/test_address_standardization.py
    """
    def setUp(self):
        self.standardizer = AddressStandardizer("XXXXX")

    def test_usps_unpack_response(self):
        """
        Test that the _unpack_response function correctly parses a
        response returned by the USPS service to form either an address
        or an error message.
        """

        not_found_response = ('<AddressValidateResponse><Address ID="0"><Er' +
                              'ror><Number>-2147219401</Number><Source>clsA' +
                              'MS</Source><Description>Address Not Found.  ' +
                              '</Description><HelpFile/><HelpContext/></Err' +
                              'or></Address></AddressValidateResponse>')
        not_found_result = ({'error': 'Address Not Found.'}, 404)
        self.assertEquals(
            self.standardizer._unpack_response(not_found_response),
            not_found_result)

        found_response = ('<AddressValidateResponse><Address ID="0"><Addres' +
                          's2>19 WILLOW DR</Address2><City>COLUMBIA</City><' +
                          'State>SC</State><Zip5>29201</Zip5><Zip4>2008</Zi' +
                          'p4></Address></AddressValidateResponse>')
        found_result = ({'city': 'COLUMBIA',
                         'state': 'SC',
                         'street': '19 WILLOW DR',
                         'suite': None,
                         'zip5': '29201',
                         'zip4': '2008'}, 200)
        self.assertEquals(self.standardizer._unpack_response(found_response),
                          found_result)
