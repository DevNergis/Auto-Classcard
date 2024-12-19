import typer
import os
import toml
import cli
import env

app = typer.Typer()
login_session = False
chrome: None


# noinspection PyTypeChecker,PyBroadException,PyShadowingNames
@app.command()
def main():
    global chrome
    config_path = "config.toml"

    # Check if the config.toml file exists
    if not os.path.exists(config_path):
        # Create a default configuration
        default_config = {
            "account": {"ID": "", "PW": ""},
            "setting": {"loop": True, "matching_game": {"count": 10, "interval": 2}},
        }
        # Write the default configuration to config.toml
        with open(config_path, "w") as config_file:
            toml.dump(default_config, config_file)
        print(f"{config_path} created with default settings.")
    else:
        print(f"{config_path} already exists.")

    chrome = cli.chrome()

    try:
        cli.main(chrome, env.setting["loop"])
    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
    except:
        chrome.quit()


if __name__ == "__main__":
    app()
