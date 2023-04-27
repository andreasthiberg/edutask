import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

@pytest.fixture
def dao_mock():
    dao_mock = mock.MagicMock()
    yield dao_mock


# Check results when a a matching user is not found in the system.
@pytest.mark.unit
def test_getUserByEmail_userNotFound(dao_mock):
    dao_mock.find.return_value = []

    sut = UserController(dao=dao_mock)

    userResult = sut.get_user_by_email(email="testname@email.com")

    assert userResult == None

# Check a registered and valid email
@pytest.mark.unit
def test_getUserByEmail_userFound(dao_mock): 
    dao_mock.find.return_value = [{'id': 1, 'name': 'Jane Doe', 'email' : 'test@test.test'}]

    sut = UserController(dao=dao_mock)

    res = sut.get_user_by_email(email='test@test.test')

    assert res['email'] == 'test@test.test'

# Check multiple users with the same email
@pytest.mark.unit
def test_getUserByEmail_multipleUsersFound(dao_mock):
    dao_mock.find.return_value = [{'id': 1, 'name': 'Jane Doe', 'email' : 'test@test.test'}, {'id': 2, 'name': 'John Doe', 'email': 'test@test.test'}]

    sut = UserController(dao=dao_mock)

    res = sut.get_user_by_email(email='test@test.test')

    assert res['id'] == 1

# Test handling of database exception when retrieving user info
@pytest.mark.unit
def test_get_user_by_email_exception(dao_mock):
    # Mock DAO's find method to raise an exception
    dao_mock.find = mock.MagicMock(side_effect=Exception('Database error'))

    sut = UserController(dao=dao_mock)

    with pytest.raises(Exception) as exec:
        sut.get_user_by_email(email='testname@email.com')
    
    assert str(exec.value) == "Database error"

# Test handling of invalid email
@pytest.mark.unit
def test_getUserByEmail_invalidEmail(dao_mock):
    sut = UserController(dao=dao_mock)

    with pytest.raises(ValueError) as exec:
        sut.get_user_by_email(email='test_invalid_email')

    assert str(exec.value) == 'Error: invalid email address'



     