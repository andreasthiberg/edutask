import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

# Check results when a a matching user is not found in the system.
@pytest.mark.unit
def test_getUserByEmail_userNotFound():
    mockedDAO = mock.MagicMock()
    mockedDAO.find.return_value = []

    sut = UserController(dao=mockedDAO)

    userResult = sut.get_user_by_email(email="testname@email.com")

    assert userResult == None