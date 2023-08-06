from pathlib import Path
import typer

app = typer.Typer()

def create_module(module_path: str, files: list = []):
    """
    Create a new Python module at the given module path.
    """
    current_path = ''
    for module in module_path.split('/'):
        current_path = os.path.join(current_path, module)
        Path(current_path).mkdir(parents=True, exist_ok=True)
        Path(current_path, '__init__.py').touch()

    # Create additional files
    for file in files:
        Path(current_path, file).touch()

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
        ("entrypoints/rest/tokens/request", []),
        ("entrypoints/rest/tokens/response", []),
        ("entrypoints/rest/users/request", []),
        ("entrypoints/rest/users/response", []),
        ("infra/di", []),
        ("infra/tests/domain/usecases", [])
    ]

    for module, files in modules:
        create_module(f"{base_path}/{module}", files)

if __name__ == "__main__":
    app()
