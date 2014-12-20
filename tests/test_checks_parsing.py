
# Simple unit/functional tests
#
# Released under AGPLv3+ license, see LICENSE

from desktop_security_assistant.main import load_configuration_files


def test_load_checks_configuration_files():
    conf = load_configuration_files()
    assert conf
    assert len(conf) > 8
