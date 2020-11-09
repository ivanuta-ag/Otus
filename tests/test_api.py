import pytest

TODOS_MAX = 200


@pytest.mark.parametrize('todos_id', [1, TODOS_MAX])
def test_getting_a_resource_positive(session, base_url, todos_id):
    res = session.get(url=f'{base_url}/{todos_id}')

    assert res.status_code == 200
    assert res.json()['id'] == todos_id


@pytest.mark.parametrize('todos_id', [-1, 0, TODOS_MAX + 1])
def test_getting_a_resource_negative(session, base_url, todos_id):
    res = session.get(url=f'{base_url}/{todos_id}')

    assert res.status_code == 404
    assert not res.json()


def test_listing_all_resources(session, base_url):
    res = session.get(url=f'{base_url}')

    assert res.status_code == 200
    assert len(res.json()) == 200


def test_creating_a_resource(session, base_url):
    title = 'theme'
    completed = True
    payload = {'title': title, 'completed': completed, 'userId': 1}
    res = session.post(url=base_url, json=payload)

    assert res.status_code == 201
    j = res.json()
    assert j['id'] == TODOS_MAX + 1
    assert j['userId'] == 1
    assert j['title'] == title
    assert j['completed'] == completed


def test_updating_a_resource_with_put_positive(session, base_url):
    todos_id = 1
    title = 'foo'
    completed = True
    payload = {
        'title': title,
        'completed': completed,
        'id': todos_id,
        'userId': 1
    }
    res = session.put(url=f'{base_url}/{todos_id}', json=payload)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['title'] == title
    assert res_json['completed'] == completed


@pytest.mark.parametrize('todos_id', [-1, 0, TODOS_MAX + 1])
def test_updating_a_resource_with_put_negative(session, base_url, todos_id):
    title = 'foo'
    completed = False
    payload = {
        'title': title,
        'completed': completed,
        'id': todos_id,
        'userId': 1
    }
    res = session.put(url=f'{base_url}/{todos_id}', json=payload)

    assert res.status_code == 500


def test_updating_a_resource_with_patch_positive(session, base_url):
    todos_id = 1
    completed = True
    payload = {'completed': completed}
    res = session.patch(url=f'{base_url}/{todos_id}', json=payload)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['completed'] == completed


@pytest.mark.parametrize('todos_id', [1, TODOS_MAX])
def test_deleting_a_resource(session, base_url, todos_id):
    res = session.delete(url=f'{base_url}/{todos_id}')

    assert res.status_code == 200
    assert not res.json()


@pytest.mark.parametrize('field, value', [
    ('userId', 1),
    ('id', 1),
    ('title', 'et porro tempora'),
    ('completed', True)
])
def test_filtering_resource_positive(session, base_url, field, value):
    str_val = str(value).lower() if isinstance(value, bool) else str(value)
    res = session.get(url=f'{base_url}?{field}={str_val}')

    assert res.status_code == 200
    res_json = res.json()
    assert len(res_json) != 0
    for r in res_json:
        assert r[field] == value


@pytest.mark.parametrize('param', [
    'userId=21',
    f'id={TODOS_MAX + 1}',
    'title=no title',
    'completed=no'
])
def test_filtering_resource_negative(session, base_url, param):
    res = session.get(url=f'{base_url}?{param}')

    assert res.status_code == 200
    assert not res.json()
