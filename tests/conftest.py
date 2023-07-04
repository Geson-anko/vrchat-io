import pytest
from pytest_mock import MockerFixture
from pythonosc.udp_client import SimpleUDPClient


@pytest.fixture
def osc_client(mocker: MockerFixture):
    return mocker.MagicMock(spec=SimpleUDPClient)
