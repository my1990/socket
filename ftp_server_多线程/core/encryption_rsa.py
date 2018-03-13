
# 加密文件生成
import rsa,base64,os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #该程序所在目录
sys.path.append(BASE_DIR)  #动态添加环境变量
rsa_path = BASE_DIR + '\\conf\\'


def rsa_jia():
    if os.path.exists(rsa_path + 'public.pem'):
        pass
    else:
        # 生成密钥
        (pubkey, privkey) = rsa.newkeys(1024)
        #保存密钥
        with open(rsa_path + 'public.pem','w+') as f:
            f.write(pubkey.save_pkcs1().decode())

        with open(rsa_path + 'private.pem','w+') as f:
            f.write(privkey.save_pkcs1().decode())

