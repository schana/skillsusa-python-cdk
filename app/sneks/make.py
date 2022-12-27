import pathlib
import shutil
import subprocess

import sneks


def main():
    sneks_path = str(pathlib.Path(sneks.__file__).resolve().parent)
    shutil.rmtree("modules", ignore_errors=True)
    subprocess.run(
        [
            "sphinx-apidoc",
            "--separate",
            "--module-first",
            "--force",
            "--no-toc",
            "--implicit-namespaces",
            "-o",
            "modules",
            sneks_path,
            f"{sneks_path}/engine",
            f"{sneks_path}/gui",
            f"{sneks_path}/validator",
            f"{sneks_path}/config",
            f"{sneks_path}/template",
        ]
    )
    subprocess.run(["sphinx-build", "-b", "html", ".", "build/docs"])


if __name__ == "__main__":
    main()
