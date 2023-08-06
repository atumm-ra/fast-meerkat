from pathlib import Path
from typer import Typer
import os

app = Typer()

def create_module(module_path: str):
    """
    Create a new Python module at the given module path.
    """
    current_path = ''
    for module in module_path.split('/'):
        current_path = os.path.join(current_path, module)
        Path(current_path).mkdir(parents=True, exist_ok=True)
        Path(current_path, '__init__.py').touch()

@app.command()
def create_service(service_name: str):
    """
    Create a new service with the given service name.
    """
    base_path = f"atumm/services/{service_name}"

    # List of modules to be created
    modules = [
        "dataproviders/beanie",
        "domain/use_cases",
        "entrypoints",
        "infra/di",
        "infra/tests/domain/use_cases"
    ]

    # Create each module
    for module in modules:
        create_module(f"{base_path}/{module}")

if __name__ == "__main__":
    app()
