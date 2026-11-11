"""Exit nonzero if required dependencies or fixtures are missing. SKIP is not PASS."""
from pathlib import Path
import argparse,importlib,sys

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--full',action='store_true',help='require OpenCV and matplotlib as well');a=p.parse_args()
    modules=['numpy']+(['cv2','matplotlib']if a.full else [])
    good=True
    for name in modules:
        try:
            module=importlib.import_module(name);print('OK',name,getattr(module,'__version__','unknown'))
        except Exception as e:good=False;print('FAIL',name,type(e).__name__,str(e))
    base=Path(__file__).resolve().parent
    for name in ['scoring_fixture.npz','matching_fixture.npz','pose_fixture.npz','MANIFEST.json']:
        ok=(base/'data'/name).is_file();print('OK'if ok else'FAIL','data/'+name);good=good and ok
    print('This checks environment/data, not whether student TODOs are completed.')
    return 0 if good else 2
if __name__=='__main__':sys.exit(main())
