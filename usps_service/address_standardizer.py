import xmltodict


class AddressStandardizer():
    """
    AddressStandardizer uses the services provided by the United States
    Postal Service to verify that a given address exists and to standardize
    the address into a format that complies with their standards.
    """

    def standardize(self,
                    street: str,
                    suite='',
                    city='',
                    state='',
                    zip5='',
                    zip4=''):
        """
        Creates an query from the address included in the arguments. It must
        have either a zip5 or both a city and a state. Sends the query to
        be standardized and returns the result.

        :param street: a string address, including a street name and number.
                       e.g. 12 Cherry Lane
        :param suite: an apartment or suite number, if applicable. e.g. Unit 5
        :param city: the name of a US city or town. Required if zip5 is not
                     provided. e.g. Chicago
        :param state: the abreviation of a US state or territory. Required if
                      zip5 is not provided. e.g. NY
        :param zip5: a string representation of a 5-digit zip code. Required
                     if city and state are not both provided. e.g. 03253
        :param zip4: a string representation of a 4-digit zip code extension,
                     if applicable. e.g. 8245
        :return dict: if the query was successful and returned a standardized
                      address, then the dictionary will hold the new address
                      with the same keys as the parameters. If the query was
                      unsuccessful, then the dictionary will contain an error
                      message.
        """
        if self.user_id is None:
            raise exception("No user_id set")

        address = {
            'street': street,
            'suite': suite,
            'city': city,
            'state': state,
            'zip5': zip5,
            'zip4': zip4 }

        url = ('https://secure.shippingapis.com/' +
               'ShippingAPI.dll?API=Verify&XML=' + 
               self._build_query(address, self.user_id))

        response = requests.post(url).content.decode("utf-8")
        return self._unpack_response(response)

    def _build_query(self, address: dict, user_id: str):
        """
        build an xml query in the required format for the USPS service from
        the address.
        :param address: the address to build into a query
        :return string: the xml query to submit to USPS service.
        """
        query = f'''<AddressValidateRequest USERID="{user_id}">
                    <Address ID="0">
                        <FirmName/>
                        <Address1>{address.suite}</Address1>
                        <Address2>{address.street}</Address2>
                        <City>{address.city}</City>
                        <State>{address.state}</State>
                        <Zip5>{address.zip5}</Zip5>
                        <Zip4>{address.zip4}</Zip4>
                    </Address>
                </AddressValidateRequest>'''
        query = query.split('\n')
        query = map(str.strip, query)
        query = ''.join(query)

        return query

    def _unpack_response(self, response: str):
        """
        Parse the xml response returned by the USPS service.

        :return dict: if the query was successful and returned a standardized
                      address, then the dictionary will hold the new address
                      with the same keys as the parameters. If the query was
                      unsuccessful, then the dictionary will contain an error
                      message.
        """
        response = xmltodict.parse(response)
        response = response["AddressValidateResponse"]["Address"]

        if 'Error' in response:
            if 'Description' in response['Error']:
                return {'error': response['Error']['Description']}, 404
            if 'Return Text' in response['Error']:
                return {'error': response['Error']['Return Text']}, 404
            return {'error': response['Error']}, 404


        suite = response["Address1"] if "Address1" in response else None
        street = response["Address2"]
        city = response["City"]
        state = response["State"]
        zip_code = response["Zip5"]
        zip_code = zip_code + "-" + response["Zip4"]

        return {
            'street': response['Address2'],
            'suite': suite,
            'city': response['City'],
            'state': response['State'],
            'zip5': response['Zip5'],
            'zip4': response['Zip4'] }, 200

    def __init__(self, user_id: str):
        """
        USPS requires a user id that is acquired by registering for their
        services. To get a USPS id, visit
        https://registration.shippingapis.com/

        :param user_id: a USPS issued id string which allows the user to
        utilize USPS shipping apis.
        """
        self.user_id = user_id
