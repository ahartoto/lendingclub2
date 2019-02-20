[![Build Status](https://travis-ci.org/ahartoto/lendingclub2.svg?branch=master)](https://travis-ci.org/ahartoto/lendingclub2)
[![Documentation Status](https://readthedocs.org/projects/lendingclub2/badge/?version=latest)](https://lendingclub2.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI release version](https://img.shields.io/pypi/v/lendingclub2.svg)](https://pypi.python.org/pypi/lendingclub2/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/lendingclub2.svg)](https://pypi.python.org/pypi/lendingclub2/)

# Lending Club API

Welcome to the unofficial Lending Club Python API. This library is inspired by
the [LendingClub](https://github.com/jgillick/LendingClub) library, but
utilizes the REST API endpoints and applies the
[best practices](https://www.lendingclub.com/developers/best-practices)
from Lending Club. For more complete information about Lending Club's REST 
API, please go to [this page](https://www.lendingclub.com/developers>).

## Requirements

This library expects that the user has pre-generated the Authentication key.
If you are unfamiliar with it, please go to Lending Club
[documentation page](https://www.lendingclub.com/developers/authentication) 
to find the instructions on how to generate one.

The authentication key can be passed to the application as an environment
variable (`$LENDING_CLUB_API_KEY`) or using the configuration file.

User is also expected to know their investor ID number. Please login to your
Lending Club account to find your investor ID number. The investor ID number
can be passed to the application as an environment variable
(`$LENDING_CLUB_INVESTOR_ID`) or using the configuration file.

## Configuration File

If user chooses to specify either the authentication key or investor ID number
using the configuration file, the configuration file has to include the
following information:

```
[access]
api_key = THIS_IS_EXAMPLE_API_KEY=

[account]
investor_id = 123456789
```

The location of the configuration file by default is `$HOME/.lendingclub`,
but user can override it by specifying the custom path using
`$LENDING_CLUB_CONFIG` environment variable.

## Examples

```python
from lendingclub2.account import InvestorAccount

# Find information about account's available balance
account = InvestorAccount()
print(account.available_balance)
```
