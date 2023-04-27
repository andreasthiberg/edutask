import pytest
import unittest.mock as mock
from unittest.mock import patch
from pymongo import MongoClient
from src.util.dao import DAO

# Test MongoDB fixture
@pytest.fixture
def mongo_test_collection():
    # Temporary mongo db for integration testing
    client = MongoClient('mongodb://localhost:27017/')
    test_db = client['test_db']
    yield test_db['test_collection']

    # Clean up
    test_db.drop_collection('test_collection')
    client.close()

# Sut fixture with mocked validator
@pytest.fixture
@patch('src.util.dao.getValidator', autospec=True)
def sut(mocked_get_validator):

    # Mocked example validator for use data
    mocked_get_validator.return_value = {
    '$jsonSchema': {
      "bsonType": "object",
      "required": ["name", "email"],
      "properties": {
         "name": {
            "bsonType": "string",
            "description": "must be a string and is required"
         },
         "email": {
            "bsonType": "string",
            "pattern": "^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$",
            "description": "must be a valid email address"
         }
       }
    }
    }

    dao = DAO("test_collection")
    sut = dao
    return sut

# Test adding correctly formated user to DB
@pytest.mark.integration
def test_create(sut):

    # Add new user entry to database
    user_data = {"name": "Adam", "email": "adam@email.com"}
    result = sut.create(user_data)

    # Assert that user was added correctly
    assert result["email"] == "adam@email.com"
    assert result["name"] == "Adam"
    assert result["_id"]
    