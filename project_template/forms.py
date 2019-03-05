from django import forms
from django.utils.translation import ugettext_lazy as _

from project_template import constants
from project_template.datamodels.attainment_type import AttainmentType
from project_template.datamodels.financial_institution import FinancialInstitution
from project_template.datamodels.account_type import AccountType
from project_template.datamodels.currency import Currency
from project_template.datamodels.counties import Counties
from project_template.datamodels.real_estate_type import RealEstateType

import datetime
start_date = 2008
end_date = datetime.datetime.now().year
YEAR_CHOICES = tuple(map(str, range(start_date, end_date + 1)))

class TranscribeInitialInformation(forms.Form):
    name = forms.CharField(label=_("What is the name of the current politician?"))
    surname = forms.CharField(label=_("What is the surname of the current politician?"))
    position = forms.CharField(label=_("What is the position of the current politician?"))
    date = forms.DateField(label=_("Date"), widget=forms.SelectDateWidget(years=YEAR_CHOICES), input_formats=['%Y-%m-%d'])


class TranscribeDebtsTableRowsCount(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['debts']))


class TranscribeOwnedGoodsOrServicesPerSpouse(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['gifts_spouse']))


class TranscribeOwnedIncomeFromOtherSourcesTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['other_sources']))


class TranscribeOwnedInvestmentsTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['bank_accounts']))


class TranscribeOwnedJewelry(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['jewelry']))


class TranscribeOwnedAutomobile(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['automobiles']))


class TranscribeOwnedIncomeFromSalaries(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['salaries']))


class TranscribeOwnedIncomeFromGamblingTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['gambling']))


class TranscribeOwnedIncomeFromAgriculturalActivitiesTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['agriculture']))


class TranscribeIndependentActivities(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['independent_activities']))


class TranscribeOwnedIncomeFromDeferredUseOfGoods(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['deferred_use']))


class TranscribeOwnedIncomeFromPensionsTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['pensions']))


class TranscribeOwnedIncomeFromInvestmentsTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['income_investments']))


class TranscribeOwnedGoodsOrServicesPerChildTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['gifts_kids']))


class TranscribeOwnedGoodsOrServicesPerOwnerTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['goods']))


class TranscribeOwnedLandTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['land']))


class TranscribeOwnedBuildingsTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}".format(constants.DECLARATION_TABLES['buildings']))


class TranscribeOwnedBankAccountsTable(forms.Form):
    count = forms.IntegerField(label="How many filled rows are there in the table {}?".format(constants.DECLARATION_TABLES['bank_accounts']))


class TranscribeOwnedLandSingleRowEntry(forms.Form):
    judet = forms.ChoiceField(label="Care este judetul in care se gaseste terenul detinut?", choices=Counties.return_counties())
    localitate = forms.CharField(label="Care este localitatea in care se gaseste terenul detinut?")
    comuna = forms.CharField(label="Care este comuna in care se gaseste terenul detinut?")
    categorie = forms.ChoiceField(label="Care este categoria de teren?", choices=RealEstateType.return_as_iterable())
    an_dobandire = forms.DateField(label="Care este anul cand terenul a fost dobandit?", widget=forms.SelectDateWidget(years=YEAR_CHOICES), input_formats=['%Y-%m-%d'])
    mod_dobandire = forms.ChoiceField(label="Care este modul in care terenul a fost dobandit?", choices=AttainmentType.return_as_iterable())
    suprafata = forms.CharField(label="Care este suprafata terenului? (mp)")
    cota_parte = forms.IntegerField(label="Care este cota parte din acest teren? (in procente)", max_value=100, min_value=0)
    nume_proprietar = forms.CharField(label="Care este numele proprietarului?")
    prenume_proprietar = forms.CharField(label="Care este prenumele proprietarului")

class TranscribeOwnedBankAccountsRowEntry(forms.Form):
    institutia_administrativa = forms.ChoiceField(label="Care este institutia financiara?", choices=FinancialInstitution.return_as_iterable())
    tip_cont = forms.ChoiceField(label="Care este tipul contului?", choices=AccountType.return_as_iterable())
    valuta = forms.ChoiceField(label="Care este valuta?", choices=Currency.return_as_iterable())
    # TODO might need to increase the range of YEAR_CHOICES since the account could have been opened in 1989 for all we know
    anul_deschiderii = forms.DateField(label="Care este anul deschiderii contului?", widget=forms.SelectDateWidget(years=YEAR_CHOICES), input_formats=['%Y-%m-%d'])
    sold = forms.DecimalField(label="Care este valoarea soldului?", decimal_places=2, max_digits=10)

