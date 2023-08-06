# Fast Meerkat [WIP]


In a nutshell, the structure of a service within this application should follow the following example of directory tree:
```
atumm/services/user

├── dataproviders		# concrete data providers
│   └── beanie
│       ├── common
│       │   └── mixins.py
│       ├── models.py
│       └── repositories.py

├── domain			# the innermost layer (domain logic)
│   ├── models.py
│   ├── repositories.py
│   ├── exceptions.py
│   └── use_cases
│       ├── get_user.py
│       ├── login.py
│       ├── register.py
│       └── user_list.py

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
            └── use_cases
                ├── test_get_user_info.py
                ├── test_get_user_list.py
                ├── test_login.py
                └── test_register.py

```



