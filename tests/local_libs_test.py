import pytest
import os

parent_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture(scope='session')
def requirements_file():
    reqs={}
    with open(os.path.join(parent_dir,'requirements.txt'),'r') as req_file:
        for line in req_file:
            line=line.strip()
            if "#" in line: #skip comments
                continue

            if "==" in line:  
                name, version = line.split("==")
                reqs[name.lower()] = f'{version}'
            elif ">=" in line:
                name, version = line.split(">=")
                reqs[name.lower()] = f'{version}'
            else:
                reqs[line.lower()] = None
    return reqs

import scipy,numpy

libs_to_test=['scipy','numpy']

@pytest.mark.parametrize('lib',libs_to_test)
def test_lib_compatibility(requirements_file,lib):
    try:
        lib_version=__import__(lib).__version__
        assert requirements_file[lib]
        
        lib_v_list=lib_version.split('.')
        ref_v_list=requirements_file[lib].split('.')

        for loc_version,ref_version in zip(lib_v_list,ref_v_list):
            assert int(loc_version) >= int(ref_version)

    except ImportError:
        pytest.fail(f"Biblioteka {lib} nie jest zainstalowana!")




if __name__=="__main__":
    print(f'Scipy version: {scipy.__version__}')
    print(f'Numpy version: {numpy.__version__}')
    print(f'Pytest version: {pytest.__version__}')
    print(type(scipy.__version__))