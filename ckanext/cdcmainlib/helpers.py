from pylons import config
import ckan.plugins as plugins
import ckan.lib.helpers as h
from py2psql import *
import datetime
import ckan.model as model

# customized function
# desc : return a string based on current language selected, english or chinese
# para : a english string and a chinese string
def getLangLabel(en,tw):
    if h.lang() == "en":
        return en
    elif h.lang() == "zh_TW":
        return tw

# customized function
# desc : return the length of a list
# para : a list
def getLen(getObj):
    return len(getObj)

# customized function
# desc : return a replaced string
# para : a string content, a target substring, a replaced string for target substring
def strReplace(getStr,getTarget,getReplace):
    return getStr.replace(getTarget,getReplace)

# customized function
# desc : get chinese and english title
# return : specific title in chinese and english
def getLicenseLabel(getLicense, getColumn):
    register = model.Package.get_license_register()
    sorted_licenses = sorted(register.values(), key=lambda x: x.title)
    getTitle = ""
    for i in range(0, len(sorted_licenses), 1):
        if sorted_licenses[i].title == getLicense[getColumn]:
            getTitle = getLangLabel(sorted_licenses[i].etitle, sorted_licenses[i].title)
            break
    return getTitle

#
# desc : detect chinese or not
# usage : in dataset page
#
def checkChineseTag(getStr):
    for i in range(0,len(getStr),1):
        if u'\u4e00' <= getStr[i] <= u'\u9fff':
            return True
    return False

#
# desc : show the tags in the same lang environment
# usage : in dataset page
#
def checkLangTag(getStr):
    if h.lang() == "en" and not checkChineseTag(getStr):
        return True
    elif h.lang() == "zh_TW" and checkChineseTag(getStr):
        return True
    else:
        return False    

#
# desc : parse request body
# retn : dict as key => value (&key=value in URL)
#
def parsePostRequestBodyAsList(getStr):
    bodyDict = {}
    parsePair = []
    for pair in getStr.split("&"):
        parsePair = pair.split("=")
        bodyDict.setdefault(parsePair[0],parsePair[1])
    return bodyDict

#
# desc : get value of key in request body
#
def getPostRequestParamValue(getStr, getParaKey):
    getDict = parsePostRequestBodyAsList(getStr)
    if getParaKey in getDict.keys():
        return getDict[getParaKey]
    else:
        return ''

#
# desc : get psql configuration from production.ini
#
def getPSQLInfo(configName):
    url = config.get(configName)
    pattern = re.compile('\S+://(\S+):(\S+)@(\S+):(\d+)/(\S+)')
    match = pattern.match(url)
    if match:
        link = pattern.findall(url)[0]
        return {\
            'dbhost':link[2], 'dbport':str(link[3]), \
            'dbname':link[4], 'dbtable':"download_summary", \
            'dbuser':link[0], 'dbpass':link[1]\
        }
    else:
        pattern = re.compile('\S+://(\S+):(\S+)@(\S+)/(\S+)')
        link = pattern.findall(url)[0]
        return {\
            'dbhost':link[2], 'dbport':str("5432"), \
            'dbname':link[3], 'dbtable':"download_summary", \
            'dbuser':link[0], 'dbpass':link[1]\
        }

#
# desc : get account info for account application
#
def getAccInfo(option, getReq):
    psqlInfo = getPSQLInfo('ckan.cdcmainlib.psqlUrl')
    if option == "fullName":
        p2l = py2psql(psqlInfo['dbhost'], psqlInfo['dbport'], psqlInfo['dbname'], psqlInfo['dbtable'], psqlInfo['dbuser'], psqlInfo['dbpass'])
        data = p2l.select({"name" : getReq}, ["fullname"], asdict=True)
        return unicode(data[0]["fullname"], 'utf-8')
    elif option == "getDate":
        return str(datetime.datetime.now())[0:10]
    elif option == "email":
        p2l = py2psql(psqlInfo['dbhost'], psqlInfo['dbport'], psqlInfo['dbname'], psqlInfo['dbtable'], psqlInfo['dbuser'], psqlInfo['dbpass'])
        data = p2l.select({"name" : getReq}, ["email"], asdict=True)
        return unicode(data[0]["email"], 'utf-8')
    elif option == "org":
        p2l = py2psql(psqlInfo['dbhost'], psqlInfo['dbport'], psqlInfo['dbname'], psqlInfo['dbtable'], psqlInfo['dbuser'], psqlInfo['dbpass'])
        data = p2l.select({"name": getReq},["title"],asdict=True)
        return unicode(data[0]["title"], 'utf-8')

#
# desc : get user list for requesting to organization
# retn : list contains tuple
#
def getReq2OrgList(getOrg, getCrtUser):
    psqlInfo = getPSQLInfo('ckan.cdcmainlib.psqlUrl')
    p2l = py2psql(psqlInfo['dbhost'], psqlInfo['dbport'], psqlInfo['dbname'], psqlInfo['dbtable'], psqlInfo['dbuser'], psqlInfo['dbpass'])
    data = p2l.select({"organ":getOrg["name"]},["id","name","fullname","email"],asdict=True)

    if len(data) < 1:
        return []
    else:
        retList = []
        crtList = [item[0] for item in getCrtUser]
        for item in data:
            if item["id"] not in crtList:
                tmpTuple = (item["name"], item["fullname"], item["email"])
                retList.append(tmpTuple)
        return retList

#
# desc : get current user state
#
def getUserState(getID):
    psqlInfo = getPSQLInfo('ckan.cdcmainlib.psqlUrl')
    p2l = py2psql(psqlInfo['dbhost'], psqlInfo['dbport'], psqlInfo['dbname'], psqlInfo['dbtable'], psqlInfo['dbuser'], psqlInfo['dbpass'])
    data = p2l.select({"id":getID},["state"],asdict=True)
    return data[0]["state"]

#
# desc : set current user state
#
def setUserState(getID,setState):
    psqlInfo = getPSQLInfo('ckan.cdcmainlib.psqlUrl')
    p2l = py2psql(psqlInfo['dbhost'], psqlInfo['dbport'], psqlInfo['dbname'], psqlInfo['dbtable'], psqlInfo['dbuser'], psqlInfo['dbpass'])
    return p2l.update({"state":setState},{"id":getID})

#
# desc : get user organ
#
def getUserOrgan(getID):
    psqlInfo = getPSQLInfo('ckan.cdcmainlib.psqlUrl')
    p2l = py2psql(psqlInfo['dbhost'], psqlInfo['dbport'], psqlInfo['dbname'], psqlInfo['dbtable'], psqlInfo['dbuser'], psqlInfo['dbpass'])
    data = p2l.select({"id":getID},["organ"],asdict=True)
    return data[0]["organ"]

#
# desc : system current time
# retn : return time string
#
def getSysTime(option):
    if option == "date":
        return str(datetime.datetime.now())[0:10]
    elif option == "minute":
        return str(datetime.datetime.now())[11:19]
    else:
        return str(datetime.datetime.now())[0:19]

#
# desc : transform time format
# retn : return time string
#
def transTime(option, getDatetime):
    if option == "date":
        return str(getDatetime)[0:10]
    elif option == "minute":
        return str(getDatetime)[11:19]
    else:
        return str(getDatetime)[0:19]


def retGroupList(dictGroupList, dictGroupList2, getKey):
    getName = []
    retName = []
    for groupItem in dictGroupList:
        getName.append(groupItem[getKey])
    for groupItem in dictGroupList2:
        if groupItem[getKey] in getName:
            retName.append(groupItem)
    return retName

def getGroupStr(getItem):
    check = ""
    for group in get_featured_groups(30):
        if group["title"] == getItem["display_name"]:
            check = getLangLabel(group["etitle"],group["title"])
            break
    return check

def getOrganizationStr(getItem):
    check = ""
    for org in get_featured_organizations(count=30):
        if org["title"] == getItem["display_name"]:
            check = getLangLabel(org["etitle"],org["title"])
            break
    return check

def getGroupOrOrganizationLangStr(getTitle, getItem):
    check = ""
    if getTitle == "Organizations" or getTitle == u"組織":
        check = getOrganizationStr(getItem)
    elif getTitle == "Groups" or getTitle == u"群組":
        check = getGroupStr(getItem)
    else:
        check = "N"
    return check



