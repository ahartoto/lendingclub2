.. image:: https://travis-ci.org/ahartoto/lendingclub2.svg?branch=master
    :target: https://travis-ci.org/ahartoto/lendingclub2

################
Lending Club API
################

Welcome to the unofficial Lending Club Python API. This library is inspired by
the `LendingClub <https://github.com/jgillick/LendingClub>`_ library, but
utilizes the REST API endpoints and applies the `best practices
<https://www.lendingclub.com/developers/best-practices.action>`_ from Lending
Club. For more complete information about Lending Club's REST API, please go
to `this page <https://www.lendingclub.com/developers/lc-api.action>`_.

************
Requirements
************

This library expects that the user has pre-generated the Authentication key.
If you are unfamiliar with it, please go to `this page
<https://www.lendingclub.com/developers/authentication.action>`_ to find
the instructions on how to generate one.

The authentication key can be passed to the application as an environment
variable (``$LENDING_CLUB_API_KEY``) or using the configuration file.

User is also expected to know their investor ID number. Please login to your
Lending Club account to find your investor ID number. The investor ID number
can be passed to the application as an environment variable
(``$LENDING_CLUB_INVESTOR_ID``) or using the configuration file.

******************
Configuration File
******************

If user chooses to specify either the authentication key or investor ID number
using the configuration file, the configuration file has to include the
following information:

.. code-block:: cfg

    [access]
    api_key = THIS_IS_EXAMPLE_API_KEY=

    [account]
    investor_id = 123456789

The location of the configuration file by default is ``$HOME/.lendingclub``,
but user can override it by specifying the custom path using
``$LENDING_CLUB_CONFIG`` environment variable.

********
Examples
********

.. code-block:: python

    from lendingclub2.account import InvestorAccount

    # Find information about account's available balance
    account = InvestorAccount()
    print(account.available_balance)
