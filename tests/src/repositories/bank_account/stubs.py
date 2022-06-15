# stubs
account_repository_id_stub = "40db7fee-6d60-4d73-824f-1bf87edc4491"
bank_account_repository_stub = {"bank_account": "648498574893"}

bank_codes_valid_stub = [{"code": "070", "description": "BANCO REGIONAL DE BRASILIA"},
    {"code": "097", "description": "BEP - BANCO DO ESTADO DO PARANA S/A"}]

create_bank_account_stub = {"bank": "070", "account_type": "090948747654", "agency": "8776262563",
    "account_number": "9938373-2", "account_name": "corrente", "cpf":"58038116020"}

create_bank_account_invalid_stub = {"bank": "77265353572973", "account_type": "090948747654", "agency": "8776262563",
    "account_number": "9938373-2", "account_name": "corrente", "cpf":"58038116020"}


bank_code_normalized_stub = [{'code': '070', 'description': 'BANCO REGIONAL DE BRASILIA'},
 {'code': '070', 'description': 'BANCO REGIONAL DE BRASILIA'}]
