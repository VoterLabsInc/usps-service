from flask_testing import TestCase

from usps_service.address_standardizer import AddressStandardizer

class TestUSPS(TestCase):
    def setUp(self):
        self.standardizer = AddressStandardizer("XXXXX")

    def test_usps_unpack_response(self):
        """
        Test that the _unpack_response function correctly parses a
        response returned by the USPS service to form either an address
        or an error message.
        """

        not_found_response = '<AddressValidateResponse><Address ID="0"><Error><Number>-2147219401</Number><Source>clsAMS</Source><Description>Address Not Found.  </Description><HelpFile/><HelpContext/></Error></Address></AddressValidateResponse>'
        not_found_result = ('Address Not Found.', 404)
        self.assertEquals(self.standardizer._unpack_response(not_found_response),
                          not_found_result)

        found_response = '<AddressValidateResponse><Address ID="0"><Address2>19 WILLOW DR</Address2><City>COLUMBIA</City><State>SC</State><Zip5>29201</Zip5><Zip4>2008</Zip4></Address></AddressValidateResponse>'
        found_result = {'city': 'COLUMBIA',
                        'state': 'SC',
                        'street': '19 WILLOW DR',
                        'suite': None,
                        'zip': '29201-2008'}
        self.assertEquals(self.standardizer._unpack_response(found_response),
                          found_result)
