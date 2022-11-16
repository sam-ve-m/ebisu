from enum import Enum


class PersephoneSchema(Enum):
    REGISTER_CLIENT_BANK_ACCOUNT = "register_client_bank_account"
    UPDATE_CLIENT_BANK_ACCOUNT = "update_client_bank_account"
    DELETE_CLIENT_BANK_ACCOUNT = "delete_client_bank_account"
    CASH_FLOW_WITHDRAWAL_TO_EXTERNAL_BANK = "cash_flow_withdrawal_to_external_bank"
    EXCHANGE_PROPOSAL_SIMULATION = "exchange_proposal_simulation"
