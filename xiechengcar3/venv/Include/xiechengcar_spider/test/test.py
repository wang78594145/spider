import time
import execjs
from os import path
from os import getcwd
#print(datetime.datetime.strptime(string,'%Y-%m-%d %H:%M:%S'))
#print(time.localtime())

# print("当前时间： ",time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time())))
# print("当前时间： ",time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()+24*60*60)))
# print(time.time())
# print(int(time.time() * 1000))
# current_milli_time = lambda: int(round(time.time() * 1000))
# print(current_milli_time)
sign = ''
key = "9102iosd8431ytl9"
ptime2 = time.strftime('%Y/%m/%d %H:30:00 ', time.localtime(time.time() + 24 * 60 * 60))
dtime2 = time.strftime('%Y/%m/%d %H:30:00 ', time.localtime(time.time() + 24 * 60 * 60 * 3))
pcid = "2"
dcid = "2"
# a = "" + ptime2 + dtime2 + pcid + dcid
# i = []
# # o = Oe
# cipher = AES.new('aes-128-cbc', key, "")
# cipher.update()
# sign += cipher.update(src, 'utf8', 'hex')
# sign += cipher.final('hex')
#
# BS = AES.block_size
# def padding_pkcs5(value):
#     '''padding with pkcs5'''
#     return str.encode(value + (BS - len(value) % BS) * chr(BS - len(value) % BS))
#
#
# def padding_zero(value):
#     '''padding with \0'''
#     while len(value) % 16 != 0:
#         value += '\0'
#     return str.encode(value)
#
#
# def getaespwd(key, value, iv):
#     # key = hashlib.sha256(key.encode()).digest()
#     # key = padding_zero(key)
#     key = padding_pkcs5(key)
#     print("key:", key)
#     # iv = padding_pkcs5(iv)
#     cryptor = AES.new(key, AES.MODE_ECB)
#     # cryptor = AES.new(add_to_16(key), AES.MODE_CBC, iv=add_to_16(iv))
#
#     padding_value = padding_pkcs5(value)
#     # padding_value = padding_zero(value)
#     # padding_value = hashlib.sha256(value.encode()).digest()
#     ciphertext = cryptor.encrypt(padding_value)
#
#     print(binascii.b2a_hex(ciphertext))  # hexstring
#     return str(encodebytes(ciphertext), encoding='utf-8').replace('\n', '')  # base64
#
#
# key = "9102iosd8431ytl9"  # 秘钥
# value = "" + ptime2 + dtime2 + pcid + dcid  # 被加密字符
# iv = ""
# aes128string = getaespwd(key, value, iv)
# print(aes128string)
ctx2 = execjs.compile("""
    function add(x, y) {
        return x + y;
    }
""")
print(ctx2.call("add", 1, 2))
def getsign():
    ctx = execjs.compile("""
        const crypto = require('crypto');
        function cmd5(e,t,n,r){
            var a = "" + n + t + r +e,
            i = [],
            o = crypto.createCipher('aes-128-ecb', "9102iosd8431ytl9", "");
            return i.push(o.update(a,"utf8","hex")),
            i.push(o.final("hex")),
            crypto.createHash("md5").update(i.join("") + n).digest("hex");
        }
    """)
    return ctx.call("cmd5", "2019/09/24 15:30:00", "2019/09/26 15:30:00", "2", "2")
d = path.dirname(__file__)
parent_path = path.dirname(d) #获得d所在的目录,即d的父级目录
# print(parent_path+'\docs\ip.txt')
parent_path  = path.dirname(parent_path) ##获得parent_path所在的目录即parent_path的父级目录
abspath = path.abspath(d) #返回d所在目录规范的绝对路径
def test():
    print(abspath)
    print(__file__)
    print(getcwd())
    test2()

def test2():
    print(path.abspath(path.dirname(getcwd())))
    slog_path = path.dirname(path.dirname(__file__)) + '/logs/spider.log'
    print(slog_path)
    exit(0)