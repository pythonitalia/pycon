def test_root(graphql_client):
    resp = graphql_client.query('''
        {
            hello
        }
    ''')

    assert resp['data']['hello'] == "world"
