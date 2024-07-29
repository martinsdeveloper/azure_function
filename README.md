Maybe some of the functions are too long, but to be honest - I do not yet know what code culture is in the company.
Everything that can crash, has been wrapped into try catch block(python version), at the moment some static values are in the same file - I normally would carry them out into constants.py file.
When I asked about how the joke should be cut in order to fit the giphy query - there were no right way defiened - The Jokes are cut to 7 words and added "Chuck Norris" as a relevancy string, but only if the phrase is not present yet.

Maybe url generation should be done differently, but this is not the approach one would not see in production.

The demo is available at:
https://gifer.azurewebsites.net/api/random_joke
