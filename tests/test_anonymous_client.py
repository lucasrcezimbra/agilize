import responses

from agilize.client import AnonymousClient


@responses.activate
def test_download(faker):
    url, file = faker.url(), b''
    responses.add(responses.GET, url, body=file)

    assert AnonymousClient.download(url) == file
