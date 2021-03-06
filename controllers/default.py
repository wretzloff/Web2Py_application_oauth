#Todo: comprehensive error handling
#Todo: logging to file: https://docs.python.org/2/howto/logging.html#logging-basic-tutorial
#Todo: upgrade the 'sendGetToUrl' API endpoint. For instance, needs to handle re-authentication with a refresh token. Also, needs to use the parameters it receives in the HTTP POST and put them in the query string of the HTTP GET that it generates.
#Various query string formats that 'sendGetToUrl' needs to handle:
    #1. https://api.spotify.com/v1/me
    #2. https://api.spotify.com/v1/artists/{id} . Example: https://api.spotify.com/v1/artists/0OdUWJ0sBjDrqHygGUXeCF
    #3. https://api.spotify.com/v1/albums/{id}/tracks . Example: https://api.spotify.com/v1/albums/6akEvsycLGftJxYudPjmqK/tracks
import customFunctions
import contextSensitiveFunctions
def index():
    customFunctions.printToLog('------------------------------------------------', 0)
    customFunctions.printToLog('index()', 0)
    ##############################
    #If we have a parameter 'code', that means we've been redirected to this page from the "authorize" endpoint.
    parameterCode = request.vars['code']
    parameterError = request.vars['error']
    if parameterError is not None:
        customFunctions.printToLog('URL parameter \'error\': ' + parameterError, 1)
    elif parameterCode is not None:
        #Generate an HTTP POST to the "token" endpoint and save the results to the session.
        customFunctions.printToLog('URL parameter \'code\': ' + parameterCode, 1)
        responseDataInArray = contextSensitiveFunctions.callPostToTokenEndpointAuthorizationCode('Spotify', parameterCode)
        #Store data to session
        contextSensitiveFunctions.addOauthSessionVariable(session, 'access_token', responseDataInArray['access_token'], 'Spotify')
        contextSensitiveFunctions.addOauthSessionVariable(session, 'token_type', responseDataInArray['token_type'], 'Spotify')
        contextSensitiveFunctions.addOauthSessionVariable(session, 'expires_in', responseDataInArray['expires_in'], 'Spotify')
        contextSensitiveFunctions.addOauthSessionVariable(session, 'refresh_token', responseDataInArray['refresh_token'], 'Spotify')
        #Now that the Access Token has been saved to session, redirect the the landing page for this resource.
        redirect(URL('spotify', 'index'))
    ##############################
    #Build "authorize" URL that, when the user is redirected there, will begin the OAuth handshake
    full_url_spotify = contextSensitiveFunctions.callBuildUrlToInitiateAuthorization('Spotify')
    ##############################
    #response.flash = T("Welcome to the Spotify app!")
    return dict(message=T('Hello World'), authenticate_url_spotify=full_url_spotify)
