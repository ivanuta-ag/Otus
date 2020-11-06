import json
import pytest
from jsonschema import validate


def assert_valid_schema(data, schema_file):
    with open(schema_file) as f:
        schema = json.load(f)
    return validate(instance=data, schema=schema)


def test_geting_a_resource(session, base_url):
    res = session.get(url=f'{base_url}/1')
    assert_valid_schema(res.json(), 'schemas/todos_schema.json')


@pytest.mark.parametrize('schema', ['schemas/todos_schemas.json'])
def test_listing_all_resources(session, base_url, schema):
    res = session.get(url=base_url)
    assert_valid_schema(res.json(), schema)
