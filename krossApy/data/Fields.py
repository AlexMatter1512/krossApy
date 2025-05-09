from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass(frozen=True)
class Field:
    REQUEST: str
    RESPONSES: Tuple[str, ...]
    FILTER: Optional[str] = None

    @property
    def RESPONSE(self) -> str:
        """Return the first response"""
        return self.RESPONSES[0]


class Fields:
    """Container of Field constants with Field(request, [response fallback(s)], filter)"""

    # CUSTOM
    CHECK_IN_INFO = Field("_check_in_info", ("Check-in Info",))

    # STANDARD FIELDS
    CODE = Field("cod_reservation", ("Code",))
    LABEL = Field("label", ("Reference",))
    ARRIVAL = Field("arrival", ("Arrival",), FILTER="arrival")
    NIGHTS = Field("nights", ("Nights",))
    DEPARTURE = Field("departure", ("Departure",))
    N_ROOMS = Field("n_rooms", ("N. Rooms",))
    ROOMS = Field("rooms", ("Rooms",))
    OWNER = Field("owner", ("Owner",))
    GUEST_PORTAL_LINK = Field("guest_portal", ("Guest Portal",))
    N_BEDS = Field("n_beds", ("Guest", "Guests"))  # Added fallback directly
    DATE_RESERVATION = Field("date_reservation", ("Reservation Date",))
    LAST_UPDATE = Field("last_update", ("Last operation",))
    CHANNEL = Field("channel", ("Channel",))
    DATE_EXPIRATION = Field("date_expiration", ("Reservation Date",))
    DATE_CANCELATION = Field("date_cancelation", ("Cancelation date",))
    STATUS = Field("name_reservation_status", ("State", "Status"), FILTER="cod_reservation_status")
    TOTAL_CHARGE = Field("tot_charge", ("Charges",))
    ID_CONVENZIONE = Field("id_convenzione", ("Convenzione",))
    ID_PACKAGE = Field("id_package", ("Pacchetto",))
    ID_PREVENTIVO = Field("id_preventivo", ("Preventivo",))
    COUNTRY_CODE = Field("country_code", ("Paese",))
    ID_PARTITARIO = Field("id_partitario", ("Partitario",))
    ORIGINE_LEAD = Field("origine_lead", ("Origine lead",))
    METODO_ACQUISIZIONE = Field("metodo_acquisizione", ("Metodo acquisizione",))
    ID_MOTIVO_VIAGGIO = Field("id_motivo_viaggio", ("Motivo del viaggio",))
    OPERATORE = Field("operatore", ("Operatore",))
    LONG_STAY = Field("long_stay", ("Long stay",))
    ID_AGENCY = Field("id_agency", ("Agenzia",))
    EMAIL = Field("email", ("Email",))
    TELEPHONE = Field("tel", ("Telefono",))
    COD_USER = Field("cod_user", ("Pagante",))
    ARRIVAL_TIME = Field("arrival_time", ("Orario arrivo previsto",))
    DEPARTURE_TIME = Field("departure_time", ("Orario partenza prevista",))
    CHECK_OUT_ANTICIPATO = Field("check_out_anticipato", ("Check out anticipato",))
    TOTAL_CHARGE_NO_TAX = Field("tot_charge_no_tax", ("Totale senza tasse",))
    TOTAL_CHARGE_TAX = Field("tot_charge_tax", ("Totale tasse",))
    TOTAL_CHARGE_BED = Field("tot_charge_bed", ("Totale pernottamento",))
    TOTAL_CHARGE_SERV = Field("tot_charge_serv", ("Totale servizi",))
    TOTAL_CHARGE_CLEANING = Field("tot_charge_cleaning", ("Totale pulizie",))
    COMMISSION_AMOUNT = Field("commissionamount", ("Commissioni riscosse",))
    COMMISSION_AMOUNT_CHANNEL = Field("commissionamount_channel", ("Commissioni trattenute",))
    TOTAL_CHARGE_SERV_NO_VAT = Field("tot_charge_serv_no_vat", ("Totale servizi senza iva",))
    TOTAL_CHARGE_CLEANING_NO_VAT = Field("tot_charge_cleaning_no_vat", ("Totale pulizie senza iva",))
    TOTAL_CHARGE_NO_VAT = Field("tot_charge_no_vat", ("Totale senza iva",))
    TOTAL_CHARGE_BED_NO_VAT = Field("tot_charge_bed_no_vat", ("Totale pernottamento senza iva",))
    CITY_TAX_TO_PAY = Field("city_tax_to_pay", ("Tassa di soggiorno da pagare",))
    TOTAL_BED_TO_PAY = Field("tot_bed_to_pay", ("Totale pernottamento da pagare",))
    TOTAL_CHARGE_BED_CLEANING = Field("tot_charge_bed_cleaning", ("Totale pernottamento con pulizie",))
    TOTAL_CHARGE_EXTRA = Field("tot_charge_extra", ("Costi extra",))
    TOTAL_PAID = Field("tot_paid", ("Importo pagato",))
    AMOUNT_TO_PAY = Field("amount_to_pay", ("Da pagare",))
    ADVANCE_PAYMENT = Field("advance_payment", ("Acconto",))
    PAYMENT_METHOD = Field("metodo_pagamento", ("Metodo pagamento",))
    IMPORTO_FATTURATO = Field("importo_fatturato", ("Importo fatturato",))
    IMPORTO_DA_FATTURARE = Field("importo_da_fatturare", ("Importo da fatturare",))
    DATA_SCADENZA_VERIFICA_CC = Field("data_scadenza_verifica_cc", ("Data scadenza verifica cc",))
    DATA_SCADENZA_ATTESA_CC = Field("data_scadenza_attesa_cc", ("Data scadenza attesa cc",))
    TOTAL_DEPOSIT = Field("tot_deposit", ("Deposito cauzionale",))
    TOTAL_PAID_WITH_DEPOSIT = Field("tot_paid_with_deposit", ("Totale pagato con deposito",))
    EXPECTED_PAYOUT = Field("expected_payout", ("Saldo previsto",))
    CURRENCY = Field("currency", ("Valuta",))
    TO_PAY_GUEST = Field("to_pay_guest", ("To pay guest",))
    TO_PAY_OTA = Field("to_pay_ota", ("Da pagare al canale",))


class CustomFields(Enum):
    """Class containing custom reservation fields"""
    CHECK_IN_INFO = Fields.CHECK_IN_INFO
