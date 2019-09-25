# Filename: loan.py

"""
LendingClub2 Loan Module
"""

# Standard libraries
import json
from operator import attrgetter

# lendingclub2
from lendingclub2 import request
from lendingclub2.config import API_VERSION, DNS, ENDPOINTS
from lendingclub2.error import LCError
from lendingclub2.response import Response


# Constants
LISTING_VERSION = '1.3'

# Interface classes


class Borrower:
    """
    Information of the borrower
    """

    def __init__(self, response):
        """
        Constructor.
        :param response: dict
        """
        self._response = response

    def __repr__(self):
        """
        String representation of the borrower.
        :returns: string
        """
        return "Borrower(credit_score={}, employed={})".format(
            self.credit_score, self.employed)

    @property
    def employment_length(self):
        """
        The length of employment.
        :returns: int (-1 if not employed) - number of months being employed.
        """
        if self._response['empLength'] is None:
            return -1
        return self._response['empLength']

    @property
    def employed(self):
        """
        Check if the borrower is employed.
        :returns: boolean
        """
        return self.employment_length >= 0

    @property
    def income_verified(self):
        """
        LC had verified the income of the borrower.
        :returns: boolean
        """
        return self._response['isIncV'] == 'VERIFIED'

    @property
    def credit_score(self):
        """
        Get the credit score of the loaner.
        :returns: string
        """
        return "{}-{}".format(self._response['ficoRangeLow'],
                              self._response['ficoRangeHigh'])

    @property
    def AsOfDate(self):
        """
        Description: As of date

        :returns: String

        :nullable: No
        """
        return self._response['AsOfDate']

    @property
    def id(self):
        """
        Description: A unique LC assigned ID for the loan listing.

        :returns: Integer

        :nullable: No
        """
        return self._response['id']

    @property
    def memberId(self):
        """
        Description: A unique LC assigned Id for the borrower member.

        :returns: Integer

        :nullable: No
        """
        return self._response['memberId']

    @property
    def term(self):
        """
        Description: The Number of payments on the loan. Values are in months and
        can be either 36 or 60.

        :returns: Integer

        :nullable: No
        """
        return self._response['term']

    @property
    def intRate(self):
        """
        Description: Interest Rate on the loan

        :returns: Number

        :nullable: No
        """
        return self._response['intRate']

    @property
    def expDefaultRate(self):
        """
        Description: The expected default rate of the loan.

        :returns: Number

        :nullable: No
        """
        return self._response['expDefaultRate']

    @property
    def serviceFeeRate(self):
        """
        Description: Service fee rate paid by the investor for this loan.

        :returns: Number

        :nullable: No
        """
        return self._response['serviceFeeRate']

    @property
    def installment(self):
        """
        Description: The monthly payment owed by the borrower if the loan
        originates.

        :returns: Number

        :nullable: No
        """
        return self._response['installment']

    @property
    def grade(self):
        """
        Description: LC assigned loan grade

        :returns: String

        :nullable: No
        """
        return self._response['grade']

    @property
    def subGrade(self):
        """
        Description: LC assigned loan subgrade

        :returns: String

        :nullable: No
        """
        return self._response['subGrade']

    @property
    def empLength(self):
        """
        Description: Employment length in months. Possible values are whole
        numbers from 0 and higher. Null indicates not
        employed.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['empLength']

    @property
    def homeOwnership(self):
        """
        Description: The home ownership status provided by the borrower during
        registration or obtained from the credit report. Our
        values are: RENT, OWN, MORTGAGE, OTHER

        :returns: String

        :nullable: Yes
        """
        return self._response['homeOwnership']

    @property
    def annualInc(self):
        """
        Description: The annual income provided by the borrower during
        registration.

        :returns: Number

        :nullable: Yes
        """
        return self._response['annualInc']

    @property
    def isIncV(self):
        """
        Description: Indicates if income is verified by LC

        :returns: String

        :nullable: Yes
        """
        return self._response['isIncV']

    @property
    def acceptD(self):
        """
        Description: The date which the borrower accepted the offer

        :returns: String

        :nullable: No
        """
        return self._response['acceptD']

    @property
    def expD(self):
        """
        Description: The date the listing will expire

        :returns: String

        :nullable: No
        """
        return self._response['expD']

    @property
    def listD(self):
        """
        Description: The date which the borrower's application was listed on the
        platform.

        :returns: String

        :nullable: No
        """
        return self._response['listD']

    @property
    def creditPullD(self):
        """
        Description: The date LC pulled credit for this loan

        :returns: String

        :nullable: No
        """
        return self._response['creditPullD']

    @property
    def reviewStatusD(self):
        """
        Description: The date the loan application was reviewed by LC

        :returns: String

        :nullable: Yes
        """
        return self._response['reviewStatusD']

    @property
    def reviewStatus(self):
        """
        Description: The status of the loan during the listing period. Values:
        APPROVED, NOT_APPROVED.

        :returns: String

        :nullable: No
        """
        return self._response['reviewStatus']

    @property
    def desc(self):
        """
        Description: Loan description provided by the borrower

        :returns: String

        :nullable: Yes
        """
        return self._response['desc']

    @property
    def purpose(self):
        """
        Description: A category provided by the borrower for the loan request.
        Values are: debt_consolidation, medical,
        home_improvement, renewable_energy, small_business,
        wedding, vacation, moving, house, car,
        major_purchase, credit_card, other

        :returns: String

        :nullable: No
        """
        return self._response['purpose']

    @property
    def addrZip(self):
        """
        Description: The first 3 numbers of the ZIP code provided by the borrower
        in the loan application.

        :returns: String

        :nullable: Yes
        """
        return self._response['addrZip']

    @property
    def addrState(self):
        """
        Description: The address state provided by the borrower during loan
        application

        :returns: String

        :nullable: Yes
        """
        return self._response['addrState']

    @property
    def investorCount(self):
        """
        Description: The Number of investor members who have purchased notes from
        this loan

        :returns: Integer

        :nullable: Yes
        """
        return self._response['investorCount']

    @property
    def ilsExpD(self):
        """
        Description: The date and time when the loan will no longer be in the
        initial listing status. After this date is past, the
        initialListStatus below will not have any effect and
        the loan will be treated as a FRACTIONAL loan.

        :returns: String

        :nullable: Yes
        """
        return self._response['ilsExpD']

    @property
    def initialListStatus(self):
        """
        Description: The initial listing status of the loan. Possible values are
        W, F.

        :returns: String

        :nullable: No
        """
        return self._response['initialListStatus']

    @property
    def empTitle(self):
        """
        Description: Employment title

        :returns: String

        :nullable: Yes
        """
        return self._response['empTitle']

    @property
    def accNowDelinq(self):
        """
        Description: The Number of accounts on which the borrower is now
        delinquent.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['accNowDelinq']

    @property
    def accOpenPast24Mths(self):
        """
        Description: Number of trades opened in past 24 months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['accOpenPast24Mths']

    @property
    def bcOpenToBuy(self):
        """
        Description: Total open to buy on revolving bankcards.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['bcOpenToBuy']

    @property
    def percentBcGt75(self):
        """
        Description: Percentage of all bankcard accounts > 75% of limit.

        :returns: Number

        :nullable: Yes
        """
        return self._response['percentBcGt75']

    @property
    def bcUtil(self):
        """
        Description: Ratio of total current balance to high credit/credit limit
        for all bankcard accounts.

        :returns: Number

        :nullable: Yes
        """
        return self._response['bcUtil']

    @property
    def dti(self):
        """
        Description: The borrower's debt to income ratio, calculated using the
        monthly payments on the total debt obligations,
        excluding mortgage, divided by self-reported monthly
        income.

        :returns: Number

        :nullable: Yes
        """
        return self._response['dti']

    @property
    def delinq2Yrs(self):
        """
        Description: The Number of 30+ days past-due incidences of delinquency in
        the borrower's credit file for the past 2 years.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['delinq2Yrs']

    @property
    def delinqAmnt(self):
        """
        Description: The past-due amount owed for the accounts on which the
        borrower is now delinquent.

        :returns: Number

        :nullable: Yes
        """
        return self._response['delinqAmnt']

    @property
    def earliestCrLine(self):
        """
        Description: The date the borrower's earliest reported credit line was
        opened

        :returns: String

        :nullable: Yes
        """
        return self._response['earliestCrLine']

    @property
    def ficoRangeLow(self):
        """
        Description: The lower boundary of range the borrower's FICO belongs to.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['ficoRangeLow']

    @property
    def ficoRangeHigh(self):
        """
        Description: The upper boundary of range the borrower's FICO belongs to.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['ficoRangeHigh']

    @property
    def inqLast6Mths(self):
        """
        Description: The Number of inquiries by creditors during the past 6
        months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['inqLast6Mths']

    @property
    def mthsSinceLastDelinq(self):
        """
        Description: The Number of months since the borrower's last delinquency.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mthsSinceLastDelinq']

    @property
    def mthsSinceLastRecord(self):
        """
        Description: The Number of months since the last public record.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mthsSinceLastRecord']

    @property
    def mthsSinceRecentInq(self):
        """
        Description: Months since most recent inquiry.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mthsSinceRecentInq']

    @property
    def mthsSinceRecentRevolDelinq(self):
        """
        Description: Months since most recent revolving delinquency.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mthsSinceRecentRevolDelinq']

    @property
    def mthsSinceRecentBc(self):
        """
        Description: Months since most recent bankcard account opened.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mthsSinceRecentBc']

    @property
    def mortAcc(self):
        """
        Description: Number of mortgage accounts.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mortAcc']

    @property
    def openAcc(self):
        """
        Description: The Number of open credit lines in the borrower's credit
        file.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['openAcc']

    @property
    def pubRec(self):
        """
        Description: Number of derogatory public records.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['pubRec']

    @property
    def totalBalExMort(self):
        """
        Description: Total credit balance excluding mortgage.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totalBalExMort']

    @property
    def revolBal(self):
        """
        Description: Total credit revolving balance.

        :returns: Number

        :nullable: Yes
        """
        return self._response['revolBal']

    @property
    def revolUtil(self):
        """
        Description: Revolving line utilization rate, or the amount of credit the
        borrower is using relative to all available
        revolving credit.

        :returns: Number

        :nullable: Yes
        """
        return self._response['revolUtil']

    @property
    def totalBcLimit(self):
        """
        Description: Total bankcard high credit/credit limit.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totalBcLimit']

    @property
    def totalAcc(self):
        """
        Description: The total Number of credit lines currently in the borrower's
        credit file

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totalAcc']

    @property
    def totalIlHighCreditLimit(self):
        """
        Description: Total installment high credit/credit limit

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totalIlHighCreditLimit']

    @property
    def numRevAccts(self):
        """
        Description: Number of revolving accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numRevAccts']

    @property
    def mthsSinceRecentBcDlq(self):
        """
        Description: Months since most recent bankcard delinquency.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mthsSinceRecentBcDlq']

    @property
    def pubRecBankruptcies(self):
        """
        Description: Number of public record bankruptcies.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['pubRecBankruptcies']

    @property
    def numAcctsEver120Ppd(self):
        """
        Description: Number of accounts ever 120 or more days past due.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numAcctsEver120Ppd']

    @property
    def chargeoffWithin12Mths(self):
        """
        Description: Number of charge-offs within 12 months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['chargeoffWithin12Mths']

    @property
    def collections12MthsExMed(self):
        """
        Description: Number of collections in 12 months excluding medical
        collections.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['collections12MthsExMed']

    @property
    def taxLiens(self):
        """
        Description: Number of tax liens

        :returns: Integer

        :nullable: Yes
        """
        return self._response['taxLiens']

    @property
    def mthsSinceLastMajorDerog(self):
        """
        Description: Months since most recent 90-day or worse rating.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mthsSinceLastMajorDerog']

    @property
    def numSats(self):
        """
        Description: Number of satisfactory accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numSats']

    @property
    def numTlOpPast12m(self):
        """
        Description: Number of accounts opened in past 12 months

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numTlOpPast12m']

    @property
    def moSinRcntTl(self):
        """
        Description: Months since most recent account opened

        :returns: Integer

        :nullable: Yes
        """
        return self._response['moSinRcntTl']

    @property
    def totHiCredLim(self):
        """
        Description: Total high credit/credit limit

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totHiCredLim']

    @property
    def totCurBal(self):
        """
        Description: Total current balance of all accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totCurBal']

    @property
    def avgCurBal(self):
        """
        Description: Average current balance of all accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['avgCurBal']

    @property
    def numBcTl(self):
        """
        Description: Number of bankcard accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numBcTl']

    @property
    def numActvBcTl(self):
        """
        Description: Number of currently active bankcard accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numActvBcTl']

    @property
    def numBcSats(self):
        """
        Description: Number of satisfactory bankcard accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numBcSats']

    @property
    def pctTlNvrDlq(self):
        """
        Description: Percent of trades never delinquent

        :returns: Integer

        :nullable: Yes
        """
        return self._response['pctTlNvrDlq']

    @property
    def numTl90gDpd24m(self):
        """
        Description: Number of accounts 90 or more days past due in last 24
        months

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numTl90gDpd24m']

    @property
    def numTl30dpd(self):
        """
        Description: Number of accounts currently 30 days past due (updated in
        past 2 months)

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numTl30dpd']

    @property
    def numTl120dpd2m(self):
        """
        Description: Number of accounts currently 120 days past due (updated in
        past 2 months)

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numTl120dpd2m']

    @property
    def numIlTl(self):
        """
        Description: Number of installment accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numIlTl']

    @property
    def moSinOldIlAcct(self):
        """
        Description: Months since oldest installment account opened

        :returns: Integer

        :nullable: Yes
        """
        return self._response['moSinOldIlAcct']

    @property
    def numActvRevTl(self):
        """
        Description: Number of currently active revolving trades

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numActvRevTl']

    @property
    def moSinOldRevTlOp(self):
        """
        Description: Months since oldest revolving account opened

        :returns: Integer

        :nullable: Yes
        """
        return self._response['moSinOldRevTlOp']

    @property
    def moSinRcntRevTlOp(self):
        """
        Description: Months since most recent revolving account opened

        :returns: Integer

        :nullable: Yes
        """
        return self._response['moSinRcntRevTlOp']

    @property
    def totalRevHiLim(self):
        """
        Description: Total revolving high credit/credit limit

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totalRevHiLim']

    @property
    def numRevTlBalGt0(self):
        """
        Description: Number of revolving trades with balance > 0

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numRevTlBalGt0']

    @property
    def numOpRevTl(self):
        """
        Description: Number of open revolving accounts

        :returns: Integer

        :nullable: Yes
        """
        return self._response['numOpRevTl']

    @property
    def totCollAmt(self):
        """
        Description: Total collection amounts ever owed

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totCollAmt']

    @property
    def fundedAmount(self):
        """
        Description: The total amount funded by investors for that loan at that
        point in time.

        :returns: Number

        :nullable: No
        """
        return self._response['fundedAmount']

    @property
    def loanAmount(self):
        """
        Description: The listed amount of the loan applied for by the borrower.
        If at some point in time, the credit department
        reduces the loan amount, then it will be reflected
        in this value.

        :returns: Number

        :nullable: No
        """
        return self._response['loanAmount']

    @property
    def applicationType(self):
        """
        Description: The loan application type. Valid values are INDIVIDUAL or
        JOINT.

        :returns: String

        :nullable: Yes
        """
        return self._response['applicationType']

    @property
    def disbursementMethod(self):
        """
        Description: It will indicate the loan disbursement method. Valid values
        are DIRECT_PAY or CASH.

        :returns: String

        :nullable: No
        """
        return self._response['disbursementMethod']

    @property
    def annualIncJoint(self):
        """
        Description: The joint annual income if the applicationType is JOINT.

        :returns: Number

        :nullable: Yes
        """
        return self._response['annualIncJoint']

    @property
    def dtiJoint(self):
        """
        Description: The joint debt to joint income ratio. This field is
        populated if the applicationType is JOINT.
        Calculated using the monthly payments on the total
        debt obligations, excluding mortgage, divided by
        self-reported monthly income.

        :returns: Number

        :nullable: Yes
        """
        return self._response['dtiJoint']

    @property
    def isIncVJoint(self):
        """
        Description: Indicates if joint income is verified by LC. Valid values
        are NOT_VERIFIED,SOURCE_VERIFIED and VERIFIED.

        :returns: String

        :nullable: Yes
        """
        return self._response['isIncVJoint']

    @property
    def openAcc6m(self):
        """
        Description: Number of open trades in last 6 months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['openAcc6m']

    @property
    def openIl6m(self):
        """
        Description: Number of currently active installment trades.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['openIl6m']

    @property
    def openActIl(self):
        """
        Description: Number of currently active installment trades. This field is
        a replacement field for openIl6m

        :returns: Integer

        :nullable: Yes
        """
        return self._response['openActIl']

    @property
    def openIl12m(self):
        """
        Description: Number of installment accounts opened in past 12 months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['openIl12m']

    @property
    def openIl24m(self):
        """
        Description: Number of installment accounts opened in past 24 months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['openIl24m']

    @property
    def mthsSinceRcntIl(self):
        """
        Description: Months since most recent installment accounts opened.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['mthsSinceRcntIl']

    @property
    def totalBalIl(self):
        """
        Description: Total current balance of all installment accounts.

        :returns: Number

        :nullable: Yes
        """
        return self._response['totalBalIl']

    @property
    def iLUtil(self):
        """
        Description: Ratio of total current balance to high credit/credit limit
        on all install acct.

        :returns: Number

        :nullable: Yes
        """
        return self._response['iLUtil']

    @property
    def openRv12m(self):
        """
        Description: Number of revolving trades opened in past 12 months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['openRv12m']

    @property
    def openRv24m(self):
        """
        Description: Number of revolving trades opened in past 24 months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['openRv24m']

    @property
    def maxBalBc(self):
        """
        Description: Maximum current balance owed on all revolving accounts.

        :returns: Number

        :nullable: Yes
        """
        return self._response['maxBalBc']

    @property
    def allUtil(self):
        """
        Description: Balance to credit limit on all trades.

        :returns: Number

        :nullable: Yes
        """
        return self._response['allUtil']

    @property
    def inqFi(self):
        """
        Description: Number of personal finance inquiries.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['inqFi']

    @property
    def totalCuTl(self):
        """
        Description: Number of credit union trades.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['totalCuTl']

    @property
    def inqLast12m(self):
        """
        Description: Number of credit inquiries in past 12 months.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['inqLast12m']

    @property
    def mtgPayment(self):
        """
        Description: Monthly mortgage amount.

        :returns: Number

        :nullable: Yes
        """
        return self._response['mtgPayment']

    @property
    def housingPayment(self):
        """
        Description: Borrower stated housing payment on loan application.

        :returns: Number

        :nullable: Yes
        """
        return self._response['housingPayment']

    @property
    def revolBalJoint(self):
        """
        Description: Sum of revolving credit balance of the co-borrowers, net of
        duplicate balances.

        :returns: Number

        :nullable: Yes
        """
        return self._response['revolBalJoint']

    @property
    def secAppFicoRangeLow(self):
        """
        Description: FICO range (low) for the secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppFicoRangeLow']

    @property
    def secAppFicoRangeHigh(self):
        """
        Description: FICO range (high) for the secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppFicoRangeHigh']

    @property
    def secAppEarliestCrLine(self):
        """
        Description: Earliest credit line at time of application for the
        secondary applicant.

        :returns: String

        :nullable: Yes
        """
        return self._response['secAppEarliestCrLine']

    @property
    def secAppInqLast6Mths(self):
        """
        Description: Credit inquiries in the last 6 months at time of application
        for the secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppInqLast6Mths']

    @property
    def secAppMortAcc(self):
        """
        Description: Number of mortgage accounts at time of application for the
        secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppMortAcc']

    @property
    def secAppOpenAcc(self):
        """
        Description: Number of open trades at time of application for the
        secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppOpenAcc']

    @property
    def secAppRevolUtil(self):
        """
        Description: Ratio of total current balance to high credit/credit limit
        for all revolving accounts.

        :returns: Number

        :nullable: Yes
        """
        return self._response['secAppRevolUtil']

    @property
    def secAppOpenIl6m(self):
        """
        Description: Number of currently active installment trades at time of
        application for the secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppOpenIl6m']

    @property
    def secAppOpenActIl(self):
        """
        Description: Number of currently active installment trades at time of
        application for the secondary applicant. This field
        is a replacement field for secAppOpenIl6m

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppOpenActIl']

    @property
    def secAppNumRevAccts(self):
        """
        Description: Number of revolving accounts at time of application for the
        secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppNumRevAccts']

    @property
    def secAppChargeoffWithin12Mths(self):
        """
        Description: Number of charge-offs within last 12 months at time of
        application for the secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppChargeoffWithin12Mths']

    @property
    def secAppCollections12MthsExMed(self):
        """
        Description: Number of collections within last 12 months excluding
        medical collections at time of application for the
        secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppCollections12MthsExMed']

    @property
    def secAppMthsSinceLastMajorDerog(self):
        """
        Description: Months since most recent 90-day or worse rating at time of
        application for the secondary applicant.

        :returns: Integer

        :nullable: Yes
        """
        return self._response['secAppMthsSinceLastMajorDerog']


class Loan:
    """
    Information of each loan.
    """

    def __init__(self, response):
        """
        Constructor.
        :param response: dict
        """
        self._response = response

        self.id = response['id']
        self.amount = response['loanAmount']
        self.funded_amount = response['fundedAmount']
        self.term = response['term']
        self.subgrade = response['subGrade']

    def __repr__(self):
        """
        Get the string representation of a loan.
        :returns: string
        """
        template = "Loan(id={}, amount={:.2f}, funded={:.2f}%,\
                         term={}, grade={})".format(
            self.id, self.amount, self.percent_funded,
            self.term, self.subgrade)
        return template

    @property
    def approved(self):
        """
        Check if the loan has been approved by LendingClub.
        :returns: boolean
        """
        return self._response['reviewStatus'] == 'APPROVED'

    @property
    def borrower(self):
        """
        Get the information of the borrower.
        :returns: instance of :py:class:`~lendingclub2.loan.Borrower`.
        """
        return Borrower(self._response)

    @property
    def expected_default_rate(self):
        """
        The expected default rate of the loan.
        :returns: float
        """
        return self._response['expDefaultRate']

    @property
    def description(self):
        """
        Get the description of the loan.
        :returns: string or None
        """
        return self._response['desc']

    @property
    def grade(self):
        """
        Get the grade of the loan.
        :returns: string
        """
        return self._response['grade']

    @property
    def installment(self):
        """
        Expected monthly payment owed by borrower.
        :returns: float
        """
        return self._response['installment']

    @property
    def interest_rate(self):
        """
        Get the interest rate.
        :returns: float (0.0 - 100.0)
        """
        return self._response['intRate']

    @property
    def investor_count(self):
        """
        Get the number of investors already purchased the notes.
        :returns: int
        """
        return self._response['investorCount'] or 0

    @property
    def percent_funded(self):
        """
        Find percentage of amount funded.
        :returns: float (0.0 - 100.0)
        """
        return self.funded_amount * 100.0 / self.amount

    @property
    def purpose(self):
        """
        Get the purpose of the loan.
        :returns: string
        """
        return self._response['purpose']


class Listing:
    """
    Loan listing, which can be used for filtering, and order submission later.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.loans = list()

    def __add__(self, other):
        """
        Add two listings together.
        :param other: instance of :py:class:`~lendingclub2.loan.Listing`.
        :returns: instance of :py:class:`~lendingclub2.loan.Listing`.
        """
        new_listing = Listing()
        new_listing.loans = list(self.loans) + list(other.loans)
        return new_listing

    def __contains__(self, loan_id):
        """
        Check if the items are in the listing.
        :param loan_id: int
        :returns: boolean
        """
        for loan in self.loans:
            if loan.id == loan_id:
                return True
        return False

    def __copy__(self):
        """
        Shallow copy of the listing.
        :returns: instance of :py:class:`~lendingclub2.loan.Listing`.
        """
        new_listing = Listing()
        new_listing.loans = list(self.loans)
        return new_listing

    def __eq__(self, other):
        """
        Check if two listings are equal.
        :param other: instance of :py:class:`~lendingclub2.loan.Listing`.
        :returns: boolean
        """
        return self.loans == other.loans

    def __getitem__(self, loan_id):
        """
        Get the loan instance based on the ID.
        :param loan_id: int - loan ID.
        :raises IndexError: if the loan ID is not in the listing.
        :returns: instance of :py:class:`~lendingclub2.loan.Loan`.
        """
        for loan in self.loans:
            if loan.id == loan_id:
                return loan
        raise IndexError("loan with ID {} is not in listing".format(loan_id))

    def __iter__(self):
        """
        Get an iterable version of the listing.
        :returns: an iterable
        """
        return iter(self.loans)

    def __len__(self):
        """
        Get the length of loans in the listing.
        :returns: int
        """
        return len(self.loans)

    def copy(self):
        """
        Get a shallow copy of the listing.
        :returns: instance of :py:class:`~lendingclub2.loan.Listing`.
        """
        return self.__copy__()

    def filter(self, *filters):
        """
        Apply all filters to the search that we had found before.
        If multiple filters are specified, the loan has to meet all the
        criteria to be included in the result.
        :param filters: iterable of :py:class:`~lendingclub2.filter.Filter`.
        :returns: an instance of :py:class:`~lendingclub2.loan.Listing`.
        """
        if not filters:
            return self.copy()

        filtered = list()
        for loan in self.loans:
            meet_spec = True
            for filter_spec in filters:
                if not filter_spec.meet_requirement(loan):
                    meet_spec = False
                    break
            if meet_spec:
                filtered.append(loan)
        new_listing = Listing()
        new_listing.loans = filtered
        return new_listing

    def search(self, filter_id=None, show_all=None):
        """
        Apply filters and search for loans matching the specifications.
        """
        url = DNS + ENDPOINTS['loans'].format(version=API_VERSION)

        criteria = list()
        if filter_id is not None:
            criteria.append('filterId={}'.format(filter_id))
        if show_all is not None:
            if show_all:
                criteria.append('showAll=true')
            else:
                criteria.append('showAll=false')

        if criteria:
            url += '?' + '&'.join(criteria)

        headers = {'X-LC-LISTING-VERSION': LISTING_VERSION}
        response = Response(request.get(url, headers=headers))
        if not response.successful:
            fstr = "cannot search for any loans"
            raise LCError(fstr, details=json.dumps(response.json, indent=2))

        # Reset the stored loans whenever we search again as long as the
        # latest request was successful
        self.loans = list()
        try:
            for loan_json in response.json['loans']:
                loan = Loan(loan_json)
                self.loans.append(loan)
        except KeyError:
            pass

    def sort(self, by_grade=True, by_term=False):
        """
        Sort the listing.
        :param by_grade: boolean
        :param by_term: boolean
        """
        if not self.loans:
            return

        if by_grade:
            self.loans = sorted(self.loans, key=attrgetter('grade',
                                                           'subgrade', 'id'))
        elif by_term:
            self.loans = sorted(self.loans, key=attrgetter('term', 'id'))
        else:
            self.loans = sorted(self.loans, key=attrgetter('percent_funded'),
                                reverse=True)
