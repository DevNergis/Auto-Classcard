import typer
import os
import toml
from src import app, env, utility

cli = typer.Typer()
login_session = False
chrome: None


# noinspection PyTypeChecker,PyBroadException,PyShadowingNames
@cli.command()
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
        if utility.check_id(env.account["ID"], env.account["PW"]):
            print("확인 완료!")
        else:
            print("아이디 또는 비밀번호가 잘못되었습니다.\n")

    chrome = app.chrome()

    try:
        app.main(chrome, env.setting["loop"])
    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
    except:
        chrome.quit()


if __name__ == "__main__":
    cli()
