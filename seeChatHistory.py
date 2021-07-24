import eSqlite as ES
from globalData import GlobalData
    
sObj = ES.SQLiteConnect()
sObj.setDatabase("chatDatabase.db")
sObj.setPassword(GlobalData.stringKey , pin = 123456)
sObj.setSecurityStatus(True)
sObj.printData(tableName="chatData")
