import pytest

@pytest.fixture(scope="session")
def test_settings():
    ## load from TestSetting class in future
    return {
        "jwt-secret":"test-secret",
        "jwt-algorithm":"HS256",
    }