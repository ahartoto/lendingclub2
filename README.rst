.. image:: https://travis-ci.org/ahartoto/lendingclub2.svg?branch=master
    :target: https://travis-ci.org/ahartoto/lendingclub2

################
Lending Club API
################

Welcome to the unofficial Lending Club Python API. This library is inspired by
the `LendingClub <https://github.com/jgillick/LendingClub>`_ library, but
utilizes the REST API endpoints from Lending Club. For more complete
information about Lending Club's REST API, please go to `this page
<https://www.lendingclub.com/developers/lc-api.action>`_.

************
Requirements
************

This library expects that the user has pre-generated the Authentication key.
If you are unfamiliar with it, please go to `this page
<https://www.lendingclub.com/developers/authentication.action>`_ to find
the instructions on how to generate one.

********
Examples
********

.. code-block:: python

    from lendingclub2.account import InvestorAccount

    # Find information about account's available balance
    account = InvestorAccount()
    print(account.available_balance)
