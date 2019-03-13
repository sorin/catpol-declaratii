import datetime

from moonsheep import verifiers
from moonsheep.decorators import register

import project_template.models as models
import project_template.forms as forms
from project_template.task_templates import DigitalizationTask, CountTableRowsTask

# @register()
class TaskGetInitialInformation(DigitalizationTask):
    task_form = forms.TranscribeInitialInformation
    template_name = 'tasks/general_information_task.html'

    def save_verified_data(self, verified_data):
        politician, created = models.Politician.objects.get_or_create(
            name=verified_data['name'],
            surname=verified_data['surname'],
            initials=verified_data['initials'],
            previous_name=verified_data['previous_name']
        )

        politician.add_position(verified_data['position'])

        processed_declaration, created = models.Declaration.objects.get_or_create(
            politician=politician,
            date=verified_data['date'],
            position=verified_data['position'],
            institution=verified_data['institution'],
            declaration_type=verified_data['declaration_type']
        )


class TaskOwnedLandRowEntry(DigitalizationTask):
    task_form = forms.TranscribeOwnedLandSingleRowEntry
    template_name = "tasks/owned_land.html"

    def save_verified_data(self, verified_data):
        owned_land, created = models.OwnedLandTableEntry.objects.get_or_create(
            address="Judet: {}, Localitate: {}, Comuna: {}".format(verified_data['judet'], verified_data['localitate'], verified_data['comuna']),
            category=verified_data['categorie'],
            acquisition_year=verified_data['an_dobandire'],
            surface=verified_data['suprafata'],
            share_ratio=verified_data['cota_parte'],
            attainment_type=verified_data['mod_dobandire'],
            owner="{} {}".format(verified_data['nume_proprietar'], verified_data['prenume_proprietar']),
            observations=""
        )


class TaskOwnedLandTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedLandTable
    storage_model = models.OwnedLandTable
    child_class = TaskOwnedLandRowEntry


class TaskOwnedAutomobileRowEntry(DigitalizationTask):
    task_form = forms.TranscribeOwnedAutomobileSingleRowEntry
    template_name = "tasks/owned_automobile.html"
    
    def save_verified_data(self, verified_data):
        owned_automobile, created = models.OwnedAutomobileTableEntry.objects.get_or_create(
            car_type=verified_data['tip'],
            brand=verified_data['marca'],
            no_owned=verified_data['numar_bucati'],
            fabrication_year=verified_data['an_fabricatie'],
            attainment_type=verified_data['mod_dobandire'],
        )


class TaskOwnedAutomobileTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedAutomobile
    storage_model = models.OwnedAutomobileTable
    child_class = TaskOwnedAutomobileRowEntry


class TaskOwnedBankAccountsRowEntry(DigitalizationTask):
    task_form = forms.TranscribeOwnedBankAccountsRowEntry
    template_name = "tasks/owned_bank_accounts.html"

    def save_verified_data(self, verified_data):
        owned_bank_accounts, created = models.OwnedBankAccountsTableEntry.objects.get_or_create(
            institution=verified_data['institutia_administrativa'],
            account_type=verified_data['tip_cont'],
            currency=verified_data['valuta'],
            opening_year=verified_data['anul_deschiderii'],
            account_balance=verified_data['sold'],
        )


class TaskOwnedBankAccountsTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedBankAccountsTable
    storage_model = models.OwnedBankAccountsTable
    child_class = TaskOwnedBankAccountsRowEntry


class TaskOwnedIncomeFromAgriculturalActivitiesRowEntry(DigitalizationTask):
    task_form = forms.TranscribeOwnedIncomeFromAgriculturalActivitiesRowEntry
    template_name = "tasks/agricultural_activity.html"

    def save_verified_data(self, verified_data):
        # Check if option is person or institution
        optiune=int(verified_data['optiune'])

        income_declaration, created = models.OwnedIncomeFromAgriculturalActivitiesTableEntry.objects.get_or_create(
            name_source_of_goods=verified_data['sursa'],
            holder_relationship=verified_data['relatie_titular'],
            address_source_of_goods="Judet: {}, Localitate: {}, Comuna: {}".format(verified_data['judet'], verified_data['localitate'], verified_data['comuna']),
            goods_name=verified_data['serviciul_prestat'],
            annual_income=verified_data['venit_anual_incasat'],
            annual_income_currency=verified_data['valuta']
        )


class TaskOwnedIncomeFromAgriculturalActivitiesTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedIncomeFromAgriculturalActivitiesTable
    storage_model = models.OwnedIncomeFromAgriculturalActivitiesTable
    child_class = TaskOwnedIncomeFromAgriculturalActivitiesRowEntry


class TaskOwnedDebtsRowEntry(DigitalizationTask):
    task_form = forms.TranscribeOwnedDebtsSingleRowEntry
    template_name = "tasks/owned_debts.html"
        
    def save_verified_data(self, verified_data):
        if verified_data['nume_creditor'] and verified_data['prenume_creditor']:
            lender_identity = "Nume: {}, Prenume: {}".format(verified_data['nume_creditor'], verified_data['prenume_creditor'])
        else: 
            lender_identity = "Institutie: {}".format(verified_data['institutie'])
            
        owned_debts, created = models.OwnedDebtsTableEntry.objects.get_or_create(
                lender=lender_identity,
                debt_type=verified_data['tip_datorie'],
                acquirement_year=verified_data['an_contractare'],
                due_date=verified_data['scadenta'],
                value=verified_data['valoare'],
                currency=verified_data['moneda']
                )


class TaskOwnedDebtsTable(CountTableRowsTask):
    task_form = forms.TranscribeDebtsTableRowsCount
    storage_model = models.OwnedDebtsTable
    child_class = TaskOwnedDebtsRowEntry


class TaskOwnedIncomeFromPensionsRowEntry(DigitalizationTask):
    task_form = forms.TranscribeOwnedIncomeFromPensionsSingleRowEntry
    template_name = "tasks/owned_income_from_pensions.html"
    
    def save_verified_data(self, verified_data):
        owned_income_from_pensions, created = models.OwnedIncomeFromPensionsTableEntry.objects.get_or_create(
                income_provider_type=verified_data['beneficiar_pensie'],
                provider_name="Nume:{}, Prenume:{}".format(verified_data['nume_beneficiar'], verified_data['prenume_beneficiar']),
                name_source_of_goods=verified_data['sursa_venit'],
                address_source_of_goods="Judet: {}, Localitate: {}, Comuna: {}, Strainatate: {}".format(verified_data['judet'], verified_data['localitate'], verified_data['comuna'], verified_data['strainatate']),
                goods_name=verified_data['serviciu_prestat'],
                ex_position=verified_data['functie'],
                annual_income=verified_data['venit'],
                annual_income_currency=verified_data['moneda'])


class TaskOwnedIncomeFromPensionsTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedIncomeFromPensionsTable
    storage_model = models.OwnedIncomeFromPensionsTable
    child_class = TaskOwnedIncomeFromPensionsRowEntry


class TaskOwnedGoodsOrServicesPerSpouseTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedGoodsOrServicesPerSpouse
    storage_model = models.OwnedGoodsOrServicesPerSpouseTable
    # TODO - add child class
    child_class = None

class TaskTranscribeOwnedInvestmentsRowEntry(DigitalizationTask):
    task_form = forms.TranscribeOwnedInvestmentsRowEntry
    template_name = "tasks/owned_investments.html"

    def save_verified_data(self, verified_data):
        issuer_name = ''
        if verified_data['commercial_entity']:
            issuer_name = verified_data['commercial_entity']
        elif verified_data['limited_resp_com_entity']:
            issuer_name = verified_data['limited_resp_com_entity']
        elif verified_data['name_investment'] and verified_data['surname_investment']:
            issuer_name = "{} {}".format(verified_data['name_investment'], verified_data['surname_investment'])

        owned_investments, created = models.OwnedInvestmentsTableEntry.objects.get_or_create(
            investment_issuer_name = issuer_name,
            type_of_investment = verified_data['investment_type'],
            number_of_stocks = verified_data['number_of_shares'],
            share_ratio = verified_data['participation_quota'],
            total_value = verified_data['total_value'],
            currency = verified_data['currency']
        )

@register()
class TaskTranscribeOwnedInvestmentsTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedInvestmentsTable
    storage_model = models.OwnedInvestmentsTable
    child_class = TaskTranscribeOwnedInvestmentsRowEntry

class TaskTranscribeOwnedIncomeFromOtherSourcesTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedIncomeFromOtherSourcesTable
    storage_model = models.OwnedIncomeFromOtherSourcesTable
    # TODO - add child_class
    child_class = None

class TaskOwnedJewelryRowEntry(DigitalizationTask):
    task_form = forms.TranscribeOwnedJewelrySingleRowEntry
    template_name = "tasks/owned_jewelry.html"

    def save_verified_data(self, verified_data):
        owned_jewelry, created = models.OwnedJewelryTableEntry.objects.get_or_create(
        summary_description = verified_data['description'],
        acquisition_year = verified_data['ownership_start_year'],
        goods_value = verified_data['estimated_value'],
        currency = verified_data['currency']
    )

class TaskOwnedJewelryTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedJewelry
    storage_model = models.OwnedJewelryTable
    # TODO - add child_class
    child_class = TaskOwnedJewelryRowEntry

class TaskExtraValuableRowEntry(DigitalizationTask):
    task_form = forms.TranscribeExtraValuableRowEntry
    template_name = "tasks/owned_extra_valuable.html"

    def save_verified_data(self, verified_data):
        owned_extra_valuable, created = models.OwnedExtraValuableTableEntry.objects.get_or_create(
            estrangement_goods_type = verified_data['estranged_goods_type'],
            estragement_goods_address = "{}, {}, {}".format(verified_data['goods_county'], verified_data['goods_town'], verified_data['goods_commune']),
            estrangement_date = verified_data['estranged_date'],
            receiver_of_goods = "{} {}".format(verified_data['owner_name'], verified_data['owner_surname']),
            goods_separation_type = verified_data['estranged_goods_separation'],
            value = verified_data['estimated_value'],
            currency = verified_data['currency']
        )

class TaskExtraValuableTable(CountTableRowsTask):
    task_form = forms.TranscribeExtraValuable
    storage_model = models.OwnedExtraValuableTable
    # TODO - add child_class
    child_class = TaskExtraValuableRowEntry


class TaskOwnedIncomeFromDeferredUseOfGoodsTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedIncomeFromDeferredUseOfGoods
    storage_model = models.OwnedIncomeFromDeferredUseOfGoodsTable
    # TODO - add child_class
    child_class = None


class TaskOwnedIncomeFromIndependentActivitiesTable(CountTableRowsTask):
    task_form = forms.TranscribeIndependentActivities
    storage_model = models.OwnedIncomeFromIndependentActivitiesTable
    # TODO - add child_class
    child_class = None


class TaskOwnedIncomeFromGamblingTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedIncomeFromGamblingTable
    storage_model = models.OwnedIncomeFromGamblingTable
    # TODO - add child_class
    child_class = None


class TaskOwnedIncomeFromSalariesTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedIncomeFromSalaries
    storage_model = models.OwnedIncomeFromSalariesTable
    # TODO - add child_class
    child_class = None


class TaskOwnedGoodsOrServicesPerChildTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedGoodsOrServicesPerChildTable
    storage_model = models.OwnedGoodsOrServicesPerChildTable
    # TODO - add child_class
    child_class = None


class TaskOwnedGoodsOrServicesPerOwnerTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedGoodsOrServicesPerOwnerTable
    storage_model = models.OwnedGoodsOrServicesPerOwnerTable
    # TODO - add child_class
    child_class = None


class TaskOwnedBuildingsTable(CountTableRowsTask):
    task_form = forms.TranscribeOwnedBuildingsTable
    storage_model = models.OwnedBuildingsTable
    # TODO - add child_class
    child_class = None
