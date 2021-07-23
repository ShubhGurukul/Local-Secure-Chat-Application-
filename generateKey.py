from cryptography.fernet import Fernet


stringKey = Fernet.generate_key().decode("utf-8")


print("new key = {}".format(stringKey))
print("add this key to globalData")
