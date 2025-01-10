import getpass
import tempfile
from pathlib import Path
from textwrap import dedent

from traitlets.config import Configurable, get_config
from traitlets import Unicode, Integer


class DirectoryTrait(Unicode):
    def validate(self, obj, value):
        if not value:
            return Path.cwd()
        if Path(value).is_absolute():
            return value
        return Path.cwd() / value


class JupyterShinyProxy(Configurable):
    site_dir = DirectoryTrait(
        "",
        help="site_dir path. If not specified, use the current working directory. A relative path is relative to the current working directory.",
    ).tag(config=True)
    timeout = Integer(20, help="jupyter-server-proxy launch timeout.").tag(config=True)


def setup_shiny():
    """Manage a Shiny instance."""

    def create_directory(directory_path):
        path = Path(directory_path)
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            pass

    def _get_shiny_cmd(port):
        conf = dedent(
            """
            run_as {user};
            preserve_logs true;
            server {{
                listen {port};
                location / {{
                    site_dir {site_dir};
                    log_dir {site_dir}/logs;
                    bookmark_state_dir {site_dir}/bookmarks;
                    directory_index on;
                }}
            }}
        """
        ).format(user=getpass.getuser(), port=str(port), site_dir=shiny_config.site_dir)

        f = tempfile.NamedTemporaryFile(mode="w", delete=False)
        f.write(conf)
        f.close()
        return ["shiny-server", f.name]

    def get_icon_path():
        return Path(__file__).parent.resolve() / "icons" / "shiny.svg"

    name = "shiny"
    config = get_config()

    shiny_config = JupyterShinyProxy(config=config)

    create_directory(shiny_config.site_dir)

    return {
        "command": _get_shiny_cmd,
        "launcher_entry": {
            "title": "Shiny",
            "icon_path": get_icon_path(),
            "timeout": shiny_config.timeout,
        },
    }
