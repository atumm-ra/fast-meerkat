from atumm.app.infra.app.base import TestWebApp
from atumm.app.infra.config import get_config

app = TestWebApp(get_config()).app
