import os
import shutil


def is_installed(binary: str) -> bool:
    return shutil.which(binary) is not None

TERRA_DEPLOYMENT_ENV = os.environ.get("TERRA_DEPLOYMENT_ENV")
SFKIT_API_URL = os.environ.get("SFKIT_API_URL",
    f"https://sfkit.dsde-{TERRA_DEPLOYMENT_ENV}.broadinstitute.org/api" if TERRA_DEPLOYMENT_ENV
    else "https://sfkit-website-bhj5a4wkqa-uc.a.run.app/api")
METADATA_VM_IDENTITY_URL = (
    "http://metadata.google.internal/computeMetadata/v1/"
    "instance/service-accounts/default/identity?"
    "audience={}&format={}&licenses={}"
)
BLOCKS_MODE = "usingblocks-"
SFKIT_DIR = os.environ.get("SFKIT_DIR", os.path.join(os.path.expanduser("~"), ".config", "sfkit"))
AUTH_FILE = os.path.join(SFKIT_DIR, "auth.txt")
AUTH_KEY = os.path.join(SFKIT_DIR, "auth_key.txt")
IS_DOCKER = os.path.exists("/.dockerenv")
IS_INSTALLED_VIA_SCRIPT = (is_installed("sfgwas") and is_installed("plink2") and is_installed("GwasClient")) or TERRA_DEPLOYMENT_ENV
EXECUTABLES_PREFIX = os.path.expanduser("~") + "/.local/" if IS_INSTALLED_VIA_SCRIPT else ""
if IS_INSTALLED_VIA_SCRIPT:
    if os.environ.get("LD_LIBRARY_PATH"):
        os.environ["LD_LIBRARY_PATH"] += f":{EXECUTABLES_PREFIX}lib"
    if os.environ.get("PATH"):
        os.environ["PATH"] += f":{EXECUTABLES_PREFIX}bin:{EXECUTABLES_PREFIX}sfgwas:{EXECUTABLES_PREFIX}sf-relate:{EXECUTABLES_PREFIX}secure-gwas/code/bin"

SFKIT_PREFIX = "sfkit: "
OUT_FOLDER = os.path.join(os.environ.get("SFKIT_DIR", ""), "out")
ENCRYPTED_DATA_FOLDER = os.path.join(os.environ.get("SFKIT_DIR", ""), "encrypted_data")
SFKIT_PROXY_ON: bool = os.getenv("SFKIT_PROXY_ON",
    "true" if TERRA_DEPLOYMENT_ENV else "false").lower() == "true"

DUMMY_KEY_01 = b"\x97\xa9\xdf\x59\x51\xbc\x43\x5b\x84\x21\x42\x00\x41\xd6\x44\xf5\xa0\xd1\x14\x59\x45\x74\x04\x8f\x56\x10\x59\xf6\xfa\x75\x53\x95"
DUMMY_KEY_02 = b"\x71\x63\xec\xc9\xbd\x57\xbb\xbf\x28\x61\xec\x09\x7a\x43\x80\x1e\xd5\xac\xcd\xa2\x6e\x39\x85\xdb\x7c\x3e\x10\x19\x9e\xa8\x7b\x46"

SOCK_PATH = os.getenv("SFKIT_SOCK", os.path.join(SFKIT_DIR, "server.sock"))
SAFE_DATA_PATH = os.environ.get("SAFE_DATA_PATH", "/data")
SAFE_DATA_PATH = os.path.join(os.path.realpath(SAFE_DATA_PATH), "")

ENV = os.environ.copy()
SFKIT_PROXY_PORT = os.environ.get("SFKIT_PROXY_PORT", "7080")
if SFKIT_PROXY_ON:
    ENV["ALL_PROXY"] = "socks5://localhost:" + SFKIT_PROXY_PORT
