import os
from pathlib import Path

from typer import Typer

app = Typer()


def create_module(module_path: str, files: list = []):
    """
    Create a new Python module at the given module path.
    """
    current_path = ""
    for module in module_path.split("/"):
        current_path = os.path.join(current_path, module)
        Path(current_path).mkdir(parents=True, exist_ok=True)
        Path(current_path, "__init__.py").touch()

    for file in files:
        Path(current_path, file).touch()


def create_resource(service_name: str, resource_name: str):
    """
    Create a new REST resource with the given service and resource names.
    """
    base_path = f"atumm/services/{service_name}/entrypoints/rest/{resource_name}"

    modules = [
        (
            "",
            [
                "controllers.py",
                "presenters.py",
                "requests.py",
                "responses.py",
                "routers.py",
            ],
        ),
    ]

    for module, files in modules:
        create_module(f"{base_path}/{module}", files)


@app.command()
def create_service(service_name: str):
    """
    Create a new service with the given service name.
    """
    base_path = f"atumm/services/{service_name}"

    modules = [
        ("dataproviders/beanie", ["models.py", "repositories.py"]),
        ("domain", ["models.py", "repositories.py", "exceptions.py"]),
        ("domain/usecases", []),
        ("entrypoints", []),
        ("infra/di", []),
        ("infra/tests/domain/usecases", []),
    ]

    for module, files in modules:
        create_module(f"{base_path}/{module}", files)


@app.command()
def create_rest_resource(service_name: str, resource_name: str):
    """
    Create a new REST resource with the given service and resource name.
    """
    create_resource(service_name, resource_name)


if __name__ == "__main__":
    app()
