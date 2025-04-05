from enum import IntEnum, Enum
import typing
import datetime

class _Field_Idx(IntEnum):
    REQUEST = 0
    RESPONSE = 1
    FILTER = 2


class Fields(Enum):
    """Enum for reservation fields with [API name, Display name]"""

    # CUSTOM
    CHECK_IN_INFO = ["_check_in_info", "Check-in Info"]

    # STANDARD FIELDS
    CODE = ["cod_reservation", "Code"]
    LABEL = ["label", "Reference"]
    ARRIVAL = ["arrival", "Arrival", "arrival"]
    NIGHTS = ["nights", "Nights"]
    DEPARTURE = ["departure", "Departure"]
    N_ROOMS = ["n_rooms", "N. Rooms"]
    ROOMS = ["rooms", "Rooms"]
    OWNER = ["owner", "Owner"]
    GUEST_PORTAL_LINK = ["guest_portal", "Guest Portal"]
    # N_BEDS = ["n_beds", "Guests"] renamed by krossbooking
    N_BEDS = ["n_beds", "Guest"]
    DATE_RESERVATION = ["date_reservation", "Reservation Date"]
    LAST_UPDATE = ["last_update", "Last operation"]
    CHANNEL = ["channel", "Channel"]
    DATE_EXPIRATION = ["date_expiration", "Reservation Date"]
    DATE_CANCELATION = ["date_cancelation", "Cancelation date"]
    # STATUS = ["name_reservation_status", "Status", "cod_reservation_status"] renamed by krossbooking
    STATUS = ["name_reservation_status", "State", "cod_reservation_status"]
    TOTAL_CHARGE = ["tot_charge", "Charges"]
    ID_CONVENZIONE = ["id_convenzione", "Convenzione"]
    ID_PACKAGE = ["id_package", "Pacchetto"]
    ID_PREVENTIVO = ["id_preventivo", "Preventivo"]
    COUNTRY_CODE = ["country_code", "Paese"]
    ID_PARTITARIO = ["id_partitario", "Partitario"]
    ORIGINE_LEAD = ["origine_lead", "Origine lead"]
    METODO_ACQUISIZIONE = ["metodo_acquisizione", "Metodo acquisizione"]
    ID_MOTIVO_VIAGGIO = ["id_motivo_viaggio", "Motivo del viaggio"]
    OPERATORE = ["operatore", "Operatore"]
    LONG_STAY = ["long_stay", "Long stay"]
    ID_AGENCY = ["id_agency", "Agenzia"]
    EMAIL = ["email", "Email"]
    TELEPHONE = ["tel", "Telefono"]
    COD_USER = ["cod_user", "Pagante"]
    ARRIVAL_TIME = ["arrival_time", "Orario arrivo previsto"]
    DEPARTURE_TIME = ["departure_time", "Orario partenza prevista"]
    CHECK_OUT_ANTICIPATO = ["check_out_anticipato", "Check out anticipato"]
    TOTAL_CHARGE_NO_TAX = ["tot_charge_no_tax", "Totale senza tasse"]
    TOTAL_CHARGE_TAX = ["tot_charge_tax", "Totale tasse"]
    TOTAL_CHARGE_BED = ["tot_charge_bed", "Totale pernottamento"]
    TOTAL_CHARGE_SERV = ["tot_charge_serv", "Totale servizi"]
    TOTAL_CHARGE_CLEANING = ["tot_charge_cleaning", "Totale pulizie"]
    COMMISSION_AMOUNT = ["commissionamount", "Commissioni riscosse"]
    COMMISSION_AMOUNT_CHANNEL = ["commissionamount_channel", "Commissioni trattenute"]
    TOTAL_CHARGE_SERV_NO_VAT = ["tot_charge_serv_no_vat", "Totale servizi senza iva"]
    TOTAL_CHARGE_CLEANING_NO_VAT = [
        "tot_charge_cleaning_no_vat",
        "Totale pulizie senza iva",
    ]
    TOTAL_CHARGE_NO_VAT = ["tot_charge_no_vat", "Totale senza iva"]
    TOTAL_CHARGE_BED_NO_VAT = [
        "tot_charge_bed_no_vat",
        "Totale pernottamento senza iva",
    ]
    CITY_TAX_TO_PAY = ["city_tax_to_pay", "Tassa di soggiorno da pagare"]
    TOTAL_BED_TO_PAY = ["tot_bed_to_pay", "Totale pernottamento da pagare"]
    TOTAL_CHARGE_BED_CLEANING = [
        "tot_charge_bed_cleaning",
        "Totale pernottamento con pulizie",
    ]
    TOTAL_CHARGE_EXTRA = ["tot_charge_extra", "Costi extra"]
    TOTAL_PAID = ["tot_paid", "Importo pagato"]
    AMOUNT_TO_PAY = ["amount_to_pay", "Da pagare"]
    ADVANCE_PAYMENT = ["advance_payment", "Acconto"]
    PAYMENT_METHOD = ["metodo_pagamento", "Metodo pagamento"]
    IMPORTO_FATTURATO = ["importo_fatturato", "Importo fatturato"]
    IMPORTO_DA_FATTURARE = ["importo_da_fatturare", "Importo da fatturare"]
    DATA_SCADENZA_VERIFICA_CC = [
        "data_scadenza_verifica_cc",
        "Data scadenza verifica cc",
    ]
    DATA_SCADENZA_ATTESA_CC = ["data_scadenza_attesa_cc", "Data scadenza attesa cc"]
    TOTAL_DEPOSIT = ["tot_deposit", "Deposito cauzionale"]
    TOTAL_PAID_WITH_DEPOSIT = ["tot_paid_with_deposit", "Totale pagato con deposito"]
    EXPECTED_PAYOUT = ["expected_payout", "Saldo previsto"]
    CURRENCY = ["currency", "Valuta"]
    TO_PAY_GUEST = ["to_pay_guest", "To pay guest"]
    TO_PAY_OTA = ["to_pay_ota", "Da pagare al canale"]

    
class CustomFields(Enum):
    """Class containing custom reservation fields"""
    CHECK_IN_INFO = Fields.CHECK_IN_INFO
