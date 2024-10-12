import toml

# TOML 파일 읽기
with open('config.toml', 'r') as file:
    config = toml.load(file)

if config['account']['ID'] == '' or config['account']['PW'] == '':
    account = None
else:
    account = config['account']

setting = config['setting']
setting_matching_game = setting['matching_game']


# noinspection PyTypeChecker,PyShadowingBuiltins
def save_account(id: str, pw: str):
    config['account'] = {'ID': id, 'PW': pw}
    with open('config.toml', 'w') as f:
        toml.dump(config, f)
