import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from helpers import * 

class CdcmainlibPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cdcmainlib')


    def get_helpers(self):
        # define in the helpers.py
        return { 'getLangLabel' : getLangLabel, \
                 'getLen' : getLen, \
                 'strReplace' : strReplace, \
                 'checkChineseTag' : checkChineseTag, \
                 'checkLangTag' : checkLangTag, \
                 'getLicenseLabel' : getLicenseLabel, \
                 'parsePostRequestBodyAsList' : parsePostRequestBodyAsList, \
                 'getPostRequestParamValue' : getPostRequestParamValue, \
                 'getAccInfo' : getAccInfo, \
                 'getReq2OrgList' : getReq2OrgList, \
                 'getUserState' : getUserState, \
                 'setUserState' : setUserState, \
                 'getUserOrgan' : getUserOrgan, \
                 'getSysTime' : getSysTime, \
                 'transTime' : transTime, \
                 'retGroupList' : retGroupList, \
                 'getGroupStr' : getGroupStr, \
                 'getOrganizationStr' : getOrganizationStr, \
                 'getGroupOrOrganizationLangStr' : getGroupOrOrganizationLangStr, \
                 'getPSQLInfo' : getPSQLInfo \
               }





