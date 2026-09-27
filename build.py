"""Configure + build under the MSVC environment clang-cl needs.

PS3RECOMP_DIR points at the ps3recomp checkout (default G:/recomp/ps3)."""
import os, subprocess, sys
ps3 = os.environ.get("PS3RECOMP_DIR", r"G:\recomp\ps3")
sys.path.insert(0, os.path.join(ps3, "tools"))
from msvc_env import environ
env = environ()
if not os.path.exists("build/build.ninja"):
    subprocess.run(["cmake", "-S", ".", "-B", "build", "-G", "Ninja",
                    "-DCMAKE_C_COMPILER=clang-cl", "-DCMAKE_CXX_COMPILER=clang-cl",
                    f"-DPS3RECOMP_DIR={ps3}"], env=env, check=True)
sys.exit(subprocess.run(["cmake", "--build", "build"] + sys.argv[1:], env=env).returncode)
