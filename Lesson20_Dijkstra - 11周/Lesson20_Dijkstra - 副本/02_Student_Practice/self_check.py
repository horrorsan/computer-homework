"""唯一检查源为checks.py，与pytest共用。"""
import checks

def main():
    count=0
    for name,fn in checks.CHECKS:
        try:fn();count+=1;print('✓',name)
        except NotImplementedError as e:print('⏳',name,str(e))
        except Exception as e:print('✗',name,str(e))
    print(f'通过 {count} / {len(checks.CHECKS)} 项')
    return 0 if count==len(checks.CHECKS) else 1
if __name__=='__main__':raise SystemExit(main())
