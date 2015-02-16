#@auth.requires_login()
def index():
    import json
    print '------------------'
    print getTimestamp() + '\t index()'
    ##############################
    #If the resource owner redirected the user back to this page, then capture the URL parameter
    parameterCode = request.vars['code']
    if parameterCode is not None:
        print 'URL parameter \'code\': ' + parameterCode
    parameterError = request.vars['error']
    if parameterError is not None:
        print 'URL parameter \'error\': ' + parameterError
    ##############################
    #If we have a parameter 'code', that means we've been redirected to this page from the "authorize" endpoint.
    #Generate an HTTP POST to the "token" endpoint.
    if parameterCode is not None:
        postUrl = getConfigValue('spotify_token_endpoint')
        postValues = {'grant_type' : 'authorization_code',
                  'code' : parameterCode,
                  'redirect_uri' : getConfigValue('spotify_authorization_redirect_uri'),
                  'client_id' : getConfigValue('spotify_client_id'),
                  'client_secret' : getConfigValue('spotify_client_secret')}
        responseFromPost = postRequest(postUrl, postValues)
        responseDataInJson = responseFromPost.read()
        responseDataInArray = json.loads(responseDataInJson)
    ##############################
    #Build "authorize" URL to send to the web page
    full_url = buildUrlToInitiateAuthorization()
    ##############################
    #response.flash = T("Welcome to the Spotify app!")
    return dict(message=T('Hello World'), authenticate_url=full_url)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)

#Helper function to build and return the URL that will be used to initiate the authorization process
def buildUrlToInitiateAuthorization() :
    url = getConfigValue('spotify_authorization_endpoint')
    #Define parameters
    data = {}
    data['client_id'] = getConfigValue('spotify_client_id')
    data['response_type'] = getConfigValue('spotify_response_type')
    data['redirect_uri'] = getConfigValue('spotify_authorization_redirect_uri')
    data['scope'] = getConfigValue('spotify_scopes')
    data['show_dialog'] = getConfigValue('spotify_show_dialog')
    #Build full URL
    full_url = buildFullUrl(url, data)
    return full_url


#Private function to fetch the config value specified by configValue
def getConfigValue(configValue) :
    configValueQueryResults = db(db.config.config_setting == configValue).select()
    configValueFirstResult = configValueQueryResults[0]
    configValue = configValueFirstResult.config_value
    print getTimestamp() + '\t getConfigValue: ' + configValue
    return configValue

def buildFullUrl(path, parametersArray) :
    import urllib
    url_values = urllib.urlencode(parametersArray)
    full_url = path + '?' + url_values
    print getTimestamp() + '\t buildFullUrl: ' + full_url
    return full_url

def getTimestamp() :
    import time
    return time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")

def getRequest(url, parametersArray) :
    import urllib2
    import urllib
    full_url = buildFullUrl(url, parametersArray)
    #Send GET request and print results
    data = urllib2.urlopen(full_url)
    responseData = data.read()
    print getTimestamp() + '\t getRequest: ' + responseData
    return responseData

def postRequest(url, parametersArray) :
    import urllib2
    import urllib
    data = urllib.urlencode(parametersArray)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    print getTimestamp() + '\t postRequest: to do: log POST response body here'
    return response
