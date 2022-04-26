# Standard Libs
import pytest
from unittest.mock import patch
from typing import List

# Internal Libs
from api.services.get_statement.get_statement import GetStatement
from tests.stubs.project_stubs.stub_data import payload_data_dummy
from tests.stubs.project_stubs.stub_get_statement import (statement_dummy_request,
                                                          dummy_statement_response)


@pytest.mark.asyncio
@patch('api.services.get_statement.')