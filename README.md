# Fast Meerkat - Overview

- [Fast Meerkat - Overview](#fast-meerkat---overview)
    - [Packages in use (dependencies)](#packages-in-use-dependencies)
    - [Atumm Packages](#atumm-packages)
  - [Tutorial: A Simple Notes Service in Clean Architecture](#tutorial-a-simple-notes-service-in-clean-architecture)
    - [Part 1: Domain](#part-1-domain)
      - [1. Define the UseCases](#1-define-the-usecases)
      - [2. Define the Domain Model](#2-define-the-domain-model)
      - [3. Define the data provider interface](#3-define-the-data-provider-interface)
      - [4. Test the UseCase](#4-test-the-usecase)
    - [Part 2: Implementing a Data Provider (SQLAlchemy)](#part-2-implementing-a-data-provider-sqlalchemy)
    - [Part 3: Implementing a RESTful Interface](#part-3-implementing-a-restful-interface)
      - [REST Directory Structure:](#rest-directory-structure)
      - [Implementing the REST interface with FastAPI:](#implementing-the-rest-interface-with-fastapi)
    - [Part 4: Configurations](#part-4-configurations)
      - [Dependency Injection for the Note Service:](#dependency-injection-for-the-note-service)


This is just a pool of ideas, feel free to fork and add your own, tweak as needed.

### Packages in use (dependencies)
|     |     |
| --- | --- |
| **Name** | **Purpose** |
| injector | Dependency Injection |
| pydantic | Object validation |
| pydantic-settings | Configuration Management |
| fastapi | ASGI Framework |
| fastapi-rest | Class-Based Views for FastAPI |
| beanie | MongoDB ODM |
|  motor   | coroutine-based API for non-blocking access to MongoDB    |
|  PyJWT   |   encode and decode JSON Web Tokens (JWT)  |
|   pyseto  |   encode and decode PASETO Tokens  |
|   buti  |  A Service Registry and Bootloader for the app   |

* * *
### Atumm Packages
|     |     |
| --- | --- |
| Name | Purpose |
|  atumm-core   |  Interfaces/Protocols definitions for clean architecture  |
|  atumm-extensions   | Any code that extends other packages from the mentioned above, as well as infrastructure related code that is shared among all services    |
|  atumm-services-health   | A small health-check service (REST)    |
|  atumm-services-user   | Auth and User management    |
|  ...   | Your service here    |



This is how the dependencies are linked, from the outermost (infrastructure) to the innermost (domain)

![dependency-graph](./docs/dependency-graph.png)



We follow this directory structure, later in this document, a detailed tutorial about how to implement a notes service as an example, explaining each aspect with granular details...
```
thisapp/services/notes

├── domain			    # the innermost layer (domain logic)
│   ├── entities.py
│   ├── interfaces.py   # defines the contracts which the other layers develop adapters for, example UserRepositoryInterface -> dataproviders.orm.UserRepository
│   ├── exceptions.py
│   └── usecases
│       ├── add_new_note.py
│       └── find_notes.py

├── dataproviders		# concrete data providers
│   └── alchemy
│       ├── entities.py
│       └── repositories.py

├── entrypoints		    # entrypoints of the service, such as RESTful API endpoints, cli...etc
│   └── rest
│       ├── controllers.py
│       ├── presenters.py
│       ├── responses.py
│       └── routers.py

└── infra		        # Contains infrastructure code (dependency injection, configuration requirements and testing.)
    ├── config.py
    ├── di
    │   └── providers.py
    └── tests
        ├── conftest.py
        └── domain
            └── usecases
                ├── test_add_new_note.py
                └── test_find_notes.py

```

To create the previous structure we can use the following command:
```bash
make new-svc <service-name>
```


## Tutorial: A Simple Notes Service in Clean Architecture

**Content Overview:**

1. **Domain:** This section explains the core business logic, including defining use cases, domain models, data provider interfaces, and testing the use cases.
2. **Implementing a Data Provider (SQLAlchemy):** This part provides a step-by-step guide on how to implement a data provider using SQLAlchemy.
3. **Implementing a RESTful Interface:** This section dives into the entry points of the system, explaining how to set up routers, controllers, presenters, requests, and responses.
4. **Configurations:** The final part ties everything together, discussing dependency injection, configurations specific to the Note service, and how to integrate the Note service into the main app.


### Part 1: Domain

First, let's focus on the inner circle which is encompasses the domain, and we will go from inner to outer layers as this tutorial progresses

#### 1. Define the UseCases

We'll start by defining the use cases
1. Add a new note
2. find notes

The Command/Query Separation is just for further clarity (later to build/integrate a message bus)

```python
# thisapp/services/notes/domain/usecases/add_new_note.py
from atumm.core.types import Query, QueryUseCase

from thisapp.services.notes.domain.interfaces import NotesRepositoryInterface
from thisapp.services.notes.domain.models import Note

class AddNewNoteCommand(Command):
    title: str
    content: str

class AddNewNoteUseCase(CommandUseCase[AddNewNoteCommand]):

    @inject
    def __init__(self, notes_repo: NotesRepositoryInterface):
        self.notes_repo = notes_repo

    async def execute(self, command: AddNewNoteCommand) -> Not:
        note = Note(title=command.title, content=command.content)
        return await self.notes_repo.create(note)


# thisapp/services/notes/domain/usecases/find_notes.py
from typing import List, Optional

class FindNotesQuery(Query):
    search_term: Optional[str]

class FindNotesUseCase(QueryUseCase[FindNotesQuery]):
    @inject
    def __init__(self, note_repo: AbstractNoteRepo):
        self.note_repo = note_repo

    async def execute(self, query: FindNotesQuery) -> List[Note]:
        return await self.note_repo.find(query.search_term)

```

#### 2. Define the Domain Model

Define the domain model that represents the core business object in your application.

```python
# thisapp/services/notes/domain/entities.py
from pydantic import BaseModel

class Note(BaseModel):
    id: int
    title: str
    content: str
```

#### 3. Define the data provider interface

Here we define the interface that represents the operations you can perform on this repository

```python
# thisapp/services/notes/domain/interfaces.py
from abc import ABC, abstractmethod
from typing import Optional, Protocol

class NotesRepositoryInterface(Protocol):

    async def create(self, note: Note) -> Note:
        ...

    async def find(self, query: str) -> List[Note]:
        ...

```

#### 4. Test the UseCase

Before implementing the data storage, write tests for the use case, mocking the repository to simulate the behavior of the data storage.

```python
# thisapp/services/notes/infra/tests/domain/usecases/test_add_new_note.py

import asyncio
from unittest.mock import Mock, AsyncMock
from thisapp.services.notes.domain.interfaces import NotesRepositoryInterface
from thisapp.services.notes.domain.models import Note
from thisapp.services.notes.domain.usecases.add_new_note import AddNewNoteUseCase, AddNewNoteCommand

def test_add_new_note_use_case():
    mock_repo = Mock(spec=NotesRepositoryInterface)
    mock_repo.create = AsyncMock(return_value=Note(id=1, title="Test", content="Test content"))

    use_case = AddNewNoteUseCase(mock_repo)
    command = AddNewNoteCommand(title="Test", content="Test content")

    result = asyncio.run(use_case.execute(command))

    assert result.id == 1
    assert result.title == "Test"

```


```python
# thisapp/services/notes/infra/tests/domain/usecases/test_find_notes.py
from unittest.mock import Mock, AsyncMock
import asyncio
from thisapp.services.notes.domain.interfaces import NotesRepositoryInterface
from thisapp.services.notes.domain.models import Note
from thisapp.services.notes.domain.usecases.find_notes import FindNotesUseCase, FindNotesQuery

def test_find_notes_use_case_no_search_term():
    mock_repo = Mock(spec=NotesRepositoryInterface)
    mock_repo.find = AsyncMock(return_value=[Note(id=1, title="Test", content="Test content")])

    use_case = FindNotesUseCase(mock_repo)
    query = FindNotesQuery(search_term=None)

    result = asyncio.run(use_case.execute(query))

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].title == "Test"

def test_find_notes_use_case_with_search_term():
    mock_repo = Mock(spec=NotesRepositoryInterface)
    mock_repo.find = AsyncMock(return_value=[Note(id=2, title="Very Long Note", content="Content of a Very Long Note")])

    use_case = FindNotesUseCase(mock_repo)
    query = FindNotesQuery(search_term="Very Long")

    result = asyncio.run(use_case.execute(query))

    assert len(result) == 1
    assert result[0].id == 2
    assert result[0].title == "Very Long Note"

```



### Part 2: Implementing a Data Provider (SQLAlchemy) 


```python
# thisapp/services/notes/dataproviders/alchemy/entities.py

from atumm.extensions.alchemy import Base
from sqlalchemy import Column, Integer, String

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

# thisapp/services/notes/dataproviders/alchemy/repositories.py

from thisapp.services.notes.domain.interfaces import NotesRepositoryInterface
from thisapp.services.notes.domain.models import NoteModel
from thisapp.services.notes.dataproviders.alchemy.models import Note
from atumm.extensions.alchemy import AsyncSessionFactory
from injector import inject
from typing import Optional

# todo review
def map_note_to_domain_model(orm_note: Note) -> NoteModel:
    return NoteModel(
        id=orm_note.id,
        title=orm_note.title,
        content=orm_note.content,
    )

class NoteRepo(NotesRepositoryInterface):

    @inject
    def __init__(self, session_factory: AsyncSessionFactory):
        self.session_factory = session_factory

    async def create(self, note: NoteModel) -> NoteModel:
        async with self.session_factory.new_session() as session:
            new_note = Note(**note.dict())
            session.add(new_note)
            await session.commit()
            await session.refresh(new_note)
            return map_note_to_domain_model(new_note)

    async def find(self, query: str) -> List[NoteModel]:
        async with self.session_factory.new_session() as session:
            orm_notes = await session.query(Note).filter(
                or_(Note.title.ilike(f"%{query}%"), Note.content.ilike(f"%{query}%"))
            ).all()
            return [map_note_to_domain_model(orm_note) for orm_note in orm_notes]
```

---

### Part 3: Implementing a RESTful Interface

Let's zoom in on the entrypoints part of the system, as you may know, these entrypoints, expose the applications' features through interfaces, whether rest, cli, workers ...etc.

#### REST Directory Structure:

```
thisapp/services/notes/entrypoints/rest
│                                   ├── controllers.py
│                                   ├── presenters.py
│                                   ├── responses.py
│                                   └── routers.py
```

This structure represents a service with a REST resource for notes.

#### Implementing the REST interface with FastAPI:

1. **Router**: This will define the REST routes and delegate the actual work to the controller.

```python
# thisapp/services/notes/entrypoints/rest/routers.py
from injector import inject

from thisapp.services.notes.entrypoints.rest.notes.controllers import NotesController
from thisapp.services.notes.entrypoints.rest.notes.responses import NoteResponse
from fastapi_restful.cbv import cbv
# todo import here
# AddNewNoteCommand

router = APIRouter(prefix="/notes")


@cbv(router)
class NotesRouter:
    @inject
    def __init__(self, controller: NotesController):
        self.controller = controller

    @router.post(
        "/",
        responses={
            "200": {"model": NoteResponse},
            "400": {"model": RuntimeExceptionResponse},
        },
    )
    async def add_new_note(self, command: AddNewNoteCommand) -> NoteResponse:
        return await self.controller.add_new_note(command)

    #todo add notes action

notes_router = router

```

2. **Controller**: Handles business logic and returns a final representation for the router calls.

```python
# thisapp/services/notes/entrypoints/rest/controllers.py
from injector import inject

from thisapp.services.notes.domain.usecases.create_note import AddNewNoteCommand, AddNewNoteUseCase
from thisapp.services.notes.domain.usecases.get_note import GetNoteCommand, FindNotesUseCase
from thisapp.services.notes.entrypoints.rest.notes.presenters import NotePresenter
from thisapp.services.notes.entrypoints.rest.notes.requests import CreateNoteRequest
from thisapp.services.notes.entrypoints.rest.notes.responses import NoteResponse

class NotesController:
    @inject
    def __init__(
        self,
        presenter: NotePresenter,
        create_note_use_case: AddNewNoteUseCase,
        find_notes_use_case: FindNotesUseCase,
    ):
        self.presenter = presenter
        self.create_note_use_case = create_note_use_case
        self.find_notes_use_case = find_notes_use_case

    async def add_new_note(self, command: AddNewNoteCommand) -> NoteResponse:
        note = await self.create_note_use_case.execute(command)
        return self.presenter.present(note)

    async def find_notes(self, query: FindNotesQuery) -> List[NoteResponse]:
        notes = await self.find_notes_use_case.execute(query)
        return self.presenter.present_list(notes)

```

3. **Presenter**: Present Business Objects.

```python
# thisapp/services/notes/entrypoints/rest/presenters.py
from atumm.core.types import AbstractPresenter
from thisapp.services.notes.entrypoints.rest.notes.responses import NoteResponse

class NotePresenter(AbstractPresenter[NoteModel, NoteResponse]):
    def present(self, note: NoteModel) -> NoteResponse:
        return NoteResponse(id=note.id, title=note.title, content=note.content)
```

1. **Responses**: Response models, based on Pydantic

```python
# thisapp/services/notes/entrypoints/rest/responses.py
from pydantic import BaseModel, Field

class NoteViewModel(BaseModel):
    id: int = Field(..., description="Note ID")
    title: str = Field(..., description="Note Title")
    content: str = Field(..., description="Note Content")
```


### Part 4: Configurations

In this part we'll glue everything together, using injector and buti, defining configurations like DB URL...etc

#### Dependency Injection for the Note Service:

1. **Providers for the Note Service**:

```python
# thisapp/services/note/infra/di/providers.py
from atumm.core.infra.config import Config
from thisapp.services.notes.dataproviders.beanie.repositories import NoteRepo
from thisapp.services.notes.domain.repositories import AbstractNoteRepo
from injector import Binder, Module, singleton

class NoteRepoProvider(Module):
    def configure(self, binder: Binder):
        binder.bind(
            interface=AbstractNoteRepo,
            to=NoteRepo(),
            scope=singleton,
        )

note_providers = [NoteRepoProvider]
```

2. **Note Service Configuration**:

```python
# thisapp/services/note/__init__.py
from atumm.core.infra.config import Config, configure
from pydantic.fields import Field

@configure
class NoteConfig(Config):
    # Add any configuration specific to the Note service here.
    pass
```

3. **Note Service Component for Buti**:

Here we register this service in the app, providing any boot procedures we need, in this case we need to register the 
REST router to the FastAPI app

```python
# thisapp/services/note/infra/buti/__init__.py
from atumm.extensions.buti.keys import AtummContainerKeys
from thisapp.services.notes.entrypoints.rest.notes import notes_router
from buti import BootableComponent, ButiStore
from fastapi import APIRouter, FastAPI
from injector import Injector

class NoteServiceComponent(BootableComponent):
    def boot(self, object_store: ButiStore):
        app: FastAPI = object_store.get(AtummContainerKeys.app)

        notes_api_router = APIRouter()
        notes_api_router.include_router(
            notes_router, prefix="/api/v1", tags=["Notes"]
        )
        app.include_router(note_api_router)
```

4. **Register the NoteServiceComponent into the app bootloader**:

In `thisapp/main.py`, make sure to add the `NoteServiceComponent` to the `app_components` list.

Also import the `NoteConfig` if the service has configurations 

```python
# thisapp/main.py
from thisapp.services.notes import NoteConfig
from thisapp.services.notes.infra.buti import NoteServiceComponent

# ... [rest of the imports] ...

app_components.extend([NoteServiceComponent()])
```

This setup ensures that the notes service is integrated into the main app