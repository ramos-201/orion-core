def test_create_user_success(client_api):
    mutation = """
        mutation CreateUser(
            $name: String!,
            $lastName: String!,
            $username: String!,
            $email: String!,
            $mobilePhone: String!,
            $password: String!
        ) {
            createUser(
                name: $name,
                lastName: $lastName,
                username: $username,
                email: $email,
                mobilePhone: $mobilePhone,
                password: $password
            ) {
                user {
                    id
                    username
                }
            }
        }
    """
    variables = {
        'name': 'jon',
        'lastName': 'smith',
        'username': 'jon.smith',
        'email': 'jon.smith@example.com',
        'mobilePhone': '3111111111',
        'password': 'password.example',
    }

    response = client_api.post(
        '/graphql',
        json={'query': mutation, 'variables': variables},
    )
    data_json = response.json()

    data_user = data_json['data']['createUser']['user']
    assert data_user['id'] == '1'
    assert data_user['username'] == 'jon.smith'
