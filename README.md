# Fast Meerkat [WIP]

This is how the dependencies are linked, from the innermost layer (domain logic) to the infrastructure layer 

![dependency-graph](./docs/dependency-graph.png)



A typical service within this application should follow the following directory structure:
```
atumm/services/user

├── domain			# the innermost layer (domain logic)
│   ├── models.py
│   ├── repositories.py
│   ├── exceptions.py
│   └── usecases
│       ├── get_user.py
│       ├── login.py
│       ├── register.py
│       └── user_list.py

├── dataproviders		# concrete data providers
│   └── beanie
│       ├── models.py
│       └── repositories.py

├── entrypoints		 # entrypoints of the service, such as RESTful API endpoints, cli...etc
│   └── rest
│       ├── tokens
│       │   ├── request
│       │   │   └── auth.py
│       │   ├── response
│       │   │   └── auth.py
│       │   └── tokens.py	# controller, presenters and router
│       └── users
│           ├── request
│           │   └── user.py
│           ├── response
│           │   └── user.py
│           └── users.py

└── infra		# Contains infrastructure code including authentication, dependency injection, and testing.
    ├── di
    │   └── providers.py
    └── tests
        ├── conftest.py
        └── domain
            ├── test_user_model.py
            └── usecases
                ├── test_get_user_info.py
                ├── test_get_user_list.py
                ├── test_login.py
                └── test_register.py

```

To create the previous structure we can use the following command:
```bash
make new-svc <service-name>
```

