import sys
import argparse
import csv

from address_standardizer import AddressStandardizer

def standardize_batch(args):
    """
    Load the data from the provided csv file, pass each address to the
    standardizer, and write the results into a new file.
    """
    address_list = load_addresses(args)
    address_list = standardize_addresses(args, address_list)
    write_addresses(args, address_list)

    sys.stdout.write("Standardization is complete. The results can be found " +
                     "in the same directory as the input file, in a file " + 
                     "named as <input_file_name>_results.csv\n")
    return 200

def write_addresses(args, address_list):
    """
    Create a new csv file and populate it with the standardization results.
    The new file will have the same name as the initial input file followed
    by "_results".

    :param dict args: the arguments provided by the user. Must contain an
    args.file str holding a path to the inital source file
    :param address_list: a list of OrderedDicts, each containing one address
    that has been standardized.
    """
    file_path = args.file.split('/')
    file_name = file_path.pop()
    file_name = file_name[:len(file_name)-4]
    file_path.append(file_name + '_results.csv')

    with open("/".join(file_path), 'w+', newline='') as file:
        writer = csv.DictWriter(file, address_list[0].keys(), delimiter=',')
        writer.writeheader()
        writer.writerows(address_list)

def standardize_addresses(args, address_list):
    """
    Call on the AddressStandardizer to standardize the addresses with USPS.
    As the Standardizer runs, print out a status indicator showing how
    many have been processed. Then, insert the results into the list of
    addresses.

    :param dict args: the arguments provided by the user. Must contain an
    args.id str holding a USPS issued id code, a street, city, state, and zip5
    fields holding the names of those columns in the source csv file.
    args.suite and args.zip4 are optional.
    :param address_list: a list of OrderedDicts, each containing one address
    to standardize. The address must have the keys specified by in the args.

    :return: an updated address_list with the result data injected into each
    address.
    """
    stdr = AddressStandardizer(args.id)
    sys.stdout.write("standardizing addresses\n")

    for i, address in enumerate(address_list):
        suite = None if args.suite is None else address[args.suite]
        zip4 = None if args.zip4 is None else address[args.zip4]

        result, result_code = stdr.standardize(street=address[args.street],
                                               suite=suite,
                                               city=address[args.city],
                                               state=address[args.state],
                                               zip5=address[args.zip5],
                                               zip4=zip4)

        if result_code == 200 or result_code == 201:
            result_fields = ['street', 'suite', 'city',
                             'state', 'zip5', 'zip4']

            for field in result_fields:
                address["result " + field] = result[field]
        else:
            address["error"] = result[error]

        sys.stdout.write(f'''\r{str(i+1)} of {str(len(address_list))} complete''')

    sys.stdout.write("\n")
    return address_list

def load_addresses(args):
    """
    Open the provided csv file and load the data from it into a list of
    OrderedDicts.

    :param dict args: the arguments provided by the user. Must contain an
    args.file str with a file path name
    :return: a list of input from the csv, each line in its own OrderedDict.
    The list may contain extraneous data besides the address itself.
    Each address within the list is an OrderedDict where keys are the headers
    on the first line of the csv file.
    """
    address_list = []
    with open(args.file, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            address_list.append(row)

    return address_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='call on the usps-service to assist with address handling'
        )
    parser.add_argument('id',
        help='a USPS issued ID code')

    parser.add_argument('--file', '-f', '-F',
        help='A file of addresses to standardize as a batch',
        dest='file',
        required=True)
    parser.add_argument('--streetColumn', '--street',
        help='The header title of the column holding the street address',
        dest='street',
        required=True)
    parser.add_argument('--suiteColumn', '--suite',
        help='The header title of the column holding the suite, box, etc.',
        dest='suite',
        required=False)
    parser.add_argument('--cityColumn', '--city',
        help='The header title of the column holding the city name',
        dest='city',
        required=True)
    parser.add_argument('--stateColumn', '--state',
        help='The header title of the column holding the state abreviation',
        dest='state',
        required=True)
    parser.add_argument('--zip5Column', '--zip5',
        help='The header title of the column holding the zip5',
        dest='zip5',
        required=True)
    parser.add_argument('--zip4Column', '--zip4',
        help='The header title of the column holding the zip4',
        dest='zip4',
        required=False)

    args = parser.parse_args()
    
    standardize_batch(args)