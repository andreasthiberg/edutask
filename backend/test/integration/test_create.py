import pytest
import unittest.mock as mock
from unittest.mock import patch
from pymongo import MongoClient
import pymongo.errors as pymongo_errors
from src.util.dao import DAO
from bson.objectid import ObjectId

# Test MongoDB fixture
@pytest.fixture
def mongo_test_collection():

    # Mocked example validator for use data
    validator = { 
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
            "pattern": r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$",
            "description": "must be a valid email address"
         }
       }
    }
    }

    # Temporary mongo db for integration testing
    client = MongoClient('mongodb://localhost:27017/')
    test_db = client['edutask']
    test_db.create_collection("test_collection", validator=validator)
    test_collection = test_db['test_collection']
    yield test_collection

    # Clean up
    test_collection.drop()
    client.close()

# Sut fixture with mocked MongoDB collection
@pytest.fixture
def sut(mongo_test_collection):

    class MockedDAO(DAO):
        def __init__(self, collection):
            self.collection = collection

    sut = MockedDAO(mongo_test_collection)
    return sut

# Test adding correctly formated user to DB, expect success
@pytest.mark.integration
def test_create_correct_format(sut):

    # Add new user entry to database
    user_data = {"name": "Adam", "email": "adam@email.com"}
    result = sut.create(user_data)

    # Assert that user was added correctly
    assert result["email"] == "adam@email.com"
    assert result["name"] == "Adam"
    assert result["_id"]
    
# Test adding incorrectly formated user to DB, expect WriteError
@pytest.mark.integration
def test_create_incorrect_format(sut):

    # Attempt adding incorrectly formmated user data to database
    user_data = {"firstname": "Adam", "email": "adam@email.com"}
    with pytest.raises(pymongo_errors.WriteError):
      sut.create(user_data)
    
# Test adding a user with missing required fields
@pytest.mark.integration
def test_create_missing_field(sut):
    # Add new user with missing data to the database
    user_data = {'name': 'Ada Lovelace', 'age': '36'}

    with pytest.raises(Exception) as exc:
        sut.create(user_data)
    
    assert 'email' in str(exc.value)

# Test adding a user with non-compliant data types
@pytest.mark.integration
def test_create_non_compliant_type(sut):
    user_data = {'name': 'Ada Lovelace', 'age': '36', 'email': []}

    with pytest.raises(pymongo_errors.WriteError):
        sut.create(user_data)

# Test creating two users with the same unique data
@pytest.mark.integration
def test_create_non_unique_value(sut): 
    user_data = {'name': 'Ada Lovelace', '_id': ObjectId(), 'email': 'test@test.test'}
    sut.create(user_data)

    with pytest.raises(pymongo_errors.WriteError):
        sut.create(user_data)