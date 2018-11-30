# usps-service

This tool provides an easy way to use the United States Postal Service shipping API to validate or standardize mailing addresses within the United States and its territories. It can be used directly through the command line to standardize addresses stored in a csv file or can be called from your program as part of a larger address intake process.


### Using as an installed package
One way to use the service is to install it as a package and then call it from your source code.

##### Installing and importing
If you are calling the package in your source code, you will need to install and import it.
To install the package, use pip and the github repository.
`pip install git+https://github.com/VoterLabsInc/usps-service.git@master`
Make sure that you are using Python3 and Pip3 here. You may need to use `pip3` instead of just `pip`. Alternatively, you can add `git+https://github.com/VoterLabsInc/usps-service.git@master` to a `requirements` file.

In the file that will call the service, you should import the service itself and then the address standardizer.
```
import usps_service
from usps_service.address_standardizer import AddressStandardizer
```

##### Setup
To use the USPS Shipping API, you will first need to register with the United States Postal Service and recieve an identification code. [This link will take you to the registration page](https://registration.shippingapis.com/ "USPS Registration")

In the same file where you imported the service, you can set up the standardizer. Its constructor takes in the identification code from USPS, and prepares the tool to be used.
`address_standardizer = AddressStandardizer(yourUSPSidcode)`

##### Utilizing
When you have an address that you want to standardize, calling the tool is easy. Call its `standardize` function and pass in any information that you have. You must provide a street (with name and number) and either a 5-digit zip code or else both a city and state. The other information is optional. The standardize function returns a response dictionary and a response_code which will be 201 if the call was successful.
```
response, response_code = address_standardizer.standardize(
    street=address.street,
    suite=address.suite,
    city=address.city,
    state=address.state,
    zip5=address.zip5,
    zip4=address.zip4)
```

### Using directly from the command line
The other way to use the tool is from the command line, without writing other code, to process batches of addresses directly. In that case, you will need to download this repository.

##### Preparing the input file
Using this method will require a batch of addresses to be stored in a csv file. The first row should be column headers, and then each following line should have exactly one address. Your file must have separate columns for street, city, state, and zip code. These columns can have arbitrary names, but they need to be unique from the names of any other columns in the file. It can have separate columns for suite/box number or 4-digit zip code extension, however those are optional. It is permitted to have any number of arbitrary additional columns which the service will ignore. Below is an example of an acceptable input file.
```
address,city,state,zip,zip4
471 S WILLIAMS PL,CHANDLER,AZ,85225
1285 SE UNIVERSITY AVE APT 202,WAUKEE,IA,50263
9414 W HARVEST LN,WICHITA,KS,67212
706 E MAIN ST,WATERFORD,WI,53185
902 WEST MAIN,COMO,TX,75431
9804 SW BUNKER TRAIL,VASHON,WA,98070
108 W HARRISON ST,MAUMEE,OH,43537
21 NEWCASTLE  LANE,LAGUNA NIGUEL,CA,92677
1730 CAMINO RUSTICA  SW,LOS LUNAS,NM,87031
265 KIRKWOOD CT SW APT10,CEDAR RAPIDS,IA,52404
9125 COPPER AVE NE APT 415,ALBUQUERQUE,NM,87123,1004
609 PARKSIDE VILLAGE WAY NW,MARIETTA,GA,30060
5321 HIGHWAY 145 SOUTH,SHUBUTA,MS,39360
```

##### Invoking the service
Once you have a file prepared you are ready to call the service. Navigate into the usps-service directory (this repository). You will need to be sure you are using Python3 as you do so. You can test that everything is ready to go by pulling up the help text with
`python usps_service -h`
It will give you a brief description and the list of possible arguments. The arguments are as follows:
* __USPS Identification Code__ An id issued by the United States Postal Service. If you do not yet have one, [you can register and receive one](https://registration.shippingapis.com/ "USPS Registration"). This must be the first argument.
* __input__ The path to a csv file containing addresses. (See previous section). Required.
* __output__ The path to a csv file (pre-existing or not) to receive the processed data. Optional.
* __column names__ A set of arguments that contain the mapped column names as they appear in your input file. `street`,`city`,`state`, and `zip5` are required, while `suite` and `zip4` are optional. In the example csv above, these would be shown as:
```
--street="address" --city="city" --state="state" --zip5="zip" --zip4="zip4"
```

An example run command might appear as follows:
```
python usps_service 123IDCODE0000 --input="../data/sample.csv" --output="../data/sample_results.csv" --street="address" --city="city" --state="state" --zip5="zip" --zip4="zip4"
```
