# sourcery skip: no-wildcard-imports, require-parameter-annotation, require-return-annotation

from sfkit.utils import pca_protocol
from tests.helper_functions_and_constants import *


def test_run_pca_protocol(mocker):
    mocker.patch("sfkit.utils.pca_protocol.install_sfgwas")
    mocker.patch("sfkit.utils.pca_protocol.generate_shared_keys")
    mocker.patch("sfkit.utils.pca_protocol.update_config_local")
    mocker.patch("sfkit.utils.pca_protocol.update_config_global")
    mocker.patch("sfkit.utils.pca_protocol.update_sfgwas_go")
    mocker.patch("sfkit.utils.pca_protocol.build_sfgwas")
    mocker.patch("sfkit.utils.pca_protocol.start_sfgwas")

    pca_protocol.run_pca_protocol("1")


def test_update_config_local(mocker):
    mocker.patch("sfkit.utils.pca_protocol.toml.load")
    mocker.patch("sfkit.utils.pca_protocol.shutil.copyfile")
    mocker.patch("sfkit.utils.pca_protocol.open")
    mocker.patch("sfkit.utils.pca_protocol.toml.dump")

    pca_protocol.update_config_local("0")

    mocker.patch("sfkit.utils.pca_protocol.toml.load", side_effect=[FileNotFoundError, {}])
    pca_protocol.update_config_local("1")
