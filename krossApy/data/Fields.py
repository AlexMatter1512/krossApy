from enum import StrEnum

class Fields(StrEnum):
    """Enum for reservation fields"""
    CODE = "cod_reservation"
    LABEL = "label"
    ARRIVAL = "arrival"
    NIGHTS = "nights"
    DEPARTURE = "departure"
    N_ROOMS = "n_rooms"
    ROOMS = "rooms"
    OWNER = "owner"
    GUEST_PORTAL_LINK = "guest_portal"
    N_BEDS = "n_beds"
    DATE_RESERVATION = "date_reservation"
    LAST_UPDATE = "last_update"
    CHANNEL = "channel"
    DATE_EXPIRATION = "date_expiration"
    DATE_CANCELATION = "date_cancelation"
    STATUS = "name_reservation_status"
    TOTAL_CHARGE = "tot_charge"
    ID_CONVENZIONE = "id_convenzione"
    ID_PACKAGE = "id_package"
    ID_PREVENTIVO = "id_preventivo"
    COUNTRY_CODE = "country_code"
    ID_PARTITARIO = "id_partitario"
    ORIGINE_LEAD = "origine_lead"
    METODO_ACQUISIZIONE = "metodo_acquisizione"
    ID_MOTIVO_VIAGGIO = "id_motivo_viaggio"
    OPERATORE = "operatore"
    LONG_STAY = "long_stay"
    ID_AGENCY = "id_agency"
    EMAIL = "email"
    TELEPHONE = "tel"
    COD_USER = "cod_user"
    ARRIVAL_TIME = "arrival_time"
    DEPARTURE_TIME = "departure_time"
    CHECK_OUT_ANTICIPATO = "check_out_anticipato"
    TOTAL_CHARGE_NO_TAX = "tot_charge_no_tax"
    TOTAL_CHARGE_TAX = "tot_charge_tax"
    TOTAL_CHARGE_BED = "tot_charge_bed"
    TOTAL_CHARGE_SERV = "tot_charge_serv"
    TOTAL_CHARGE_CLEANING = "tot_charge_cleaning"
    COMMISSION_AMOUNT = "commissionamount"
    COMMISSION_AMOUNT_CHANNEL = "commissionamount_channel"
    TOTAL_CHARGE_SERV_NO_VAT = "tot_charge_serv_no_vat"
    TOTAL_CHARGE_CLEANING_NO_VAT = "tot_charge_cleaning_no_vat"
    TOTAL_CHARGE_NO_VAT = "tot_charge_no_vat"
    TOTAL_CHARGE_BED_NO_VAT = "tot_charge_bed_no_vat"
    CITY_TAX_TO_PAY = "city_tax_to_pay"
    TOTAL_BED_TO_PAY = "tot_bed_to_pay"
    TOTAL_CHARGE_BED_CLEANING = "tot_charge_bed_cleaning"
    TOTAL_CHARGE_EXTRA = "tot_charge_extra"
    TOTAL_PAID = "tot_paid"
    AMOUNT_TO_PAY = "amount_to_pay"
    ADVANCE_PAYMENT = "advance_payment"
    PAYMENT_METHOD = "metodo_pagamento"
    IMPORTO_FATTURATO = "importo_fatturato"
    IMPORTO_DA_FATTURARE = "importo_da_fatturare"
    DATA_SCADENZA_VERIFICA_CC = "data_scadenza_verifica_cc"
    DATA_SCADENZA_ATTESA_CC = "data_scadenza_attesa_cc"
    TOTAL_DEPOSIT = "tot_deposit"
    TOTAL_PAID_WITH_DEPOSIT = "tot_paid_with_deposit"
    EXPECTED_PAYOUT = "expected_payout"
    CURRENCY = "currency"
    TO_PAY_GUEST = "to_pay_guest"
    TO_PAY_OTA = "to_pay_ota"

class DataFields(StrEnum):
    """
    Enum for data fields
    Since krossbooking uses different names for the same field, this enum is used to map the fields to the correct name
    """
    CODE = "Code"
    LABEL = "Reference"
    ARRIVAL = "Arrival"
    NIGHTS = "Nights"
    DEPARTURE = "Departure"
    N_ROOMS = "N. Rooms"
    ROOMS = "Rooms"
    OWNER = "Owner"
    GUEST_PORTAL_LINK = "Guest Portal"
    N_BEDS = "Guests"
    DATE_RESERVATION = "Reservation Date"
    LAST_UPDATE = "Last operation"
    CHANNEL = "Channel"
    DATE_EXPIRATION = "Reservation Date"
    DATE_CANCELATION = "Cancelation date"
    STATUS = "Status"
    TOTAL_CHARGE = "Charges"
    ID_CONVENZIONE = "Convenzione"
    ID_PACKAGE = "Pacchetto"
    ID_PREVENTIVO = "Preventivo"
    COUNTRY_CODE = "Paese"
    ID_PARTITARIO = "Partitario"
    ORIGINE_LEAD = "Origine lead"
    METODO_ACQUISIZIONE = "Metodo acquisizione"
    ID_MOTIVO_VIAGGIO = "Motivo del viaggio"
    OPERATORE = "Operatore"
    LONG_STAY = "Long stay"
    ID_AGENCY = "Agenzia"
    EMAIL = "Email"
    TELEPHONE = "Telefono"
    COD_USER = "Pagante"
    ARRIVAL_TIME = "Orario arrivo previsto"
    DEPARTURE_TIME = "Orario partenza prevista"
    CHECK_OUT_ANTICIPATO = "Check out anticipato"
    TOTAL_CHARGE_NO_TAX = "Totale senza tasse"
    TOTAL_CHARGE_TAX = "Totale tasse"
    TOTAL_CHARGE_BED = "Totale pernottamento"
    TOTAL_CHARGE_SERV = "Totale servizi"
    TOTAL_CHARGE_CLEANING = "Totale pulizie"
    COMMISSION_AMOUNT = "Commissioni riscosse"
    COMMISSION_AMOUNT_CHANNEL = "Commissioni trattenute"
    TOTAL_CHARGE_SERV_NO_VAT = "Totale servizi senza iva"
    TOTAL_CHARGE_CLEANING_NO_VAT = "Totale pulizie senza iva"
    TOTAL_CHARGE_NO_VAT = "Totale senza iva"
    TOTAL_CHARGE_BED_NO_VAT = "Totale pernottamento senza iva"
    CITY_TAX_TO_PAY = "Tassa di soggiorno da pagare"
    TOTAL_BED_TO_PAY = "Totale pernottamento da pagare"
    TOTAL_CHARGE_BED_CLEANING = "Totale pernottamento con pulizie"
    TOTAL_CHARGE_EXTRA = "Costi extra"
    TOTAL_PAID = "Importo pagato"
    AMOUNT_TO_PAY = "Da pagare"
    ADVANCE_PAYMENT = "Acconto"
    PAYMENT_METHOD = "Metodo pagamento"
    IMPORTO_FATTURATO = "Importo fatturato"
    IMPORTO_DA_FATTURARE = "Importo da fatturare"
    DATA_SCADENZA_VERIFICA_CC = "Data scadenza verifica cc"
    DATA_SCADENZA_ATTESA_CC = "Data scadenza attesa cc"
    TOTAL_DEPOSIT = "Deposito cauzionale"
    TOTAL_PAID_WITH_DEPOSIT = "Totale pagato con deposito"
    EXPECTED_PAYOUT = "Saldo previsto"
    CURRENCY = "Valuta"
    TO_PAY_GUEST = "To pay guest"
    TO_PAY_OTA = "Da pagare al canale"
