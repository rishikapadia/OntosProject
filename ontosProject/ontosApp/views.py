from evernote.api.client import EvernoteClient

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.shortcuts import redirect

EN_CONSUMER_KEY = 'asingh12'
EN_CONSUMER_SECRET = 'b2a9213e33d06b39'


def get_evernote_client(token=None):
    if token:
        return EvernoteClient(token=token, sandbox=True)
    else:
        return EvernoteClient(
            consumer_key=EN_CONSUMER_KEY,
            consumer_secret=EN_CONSUMER_SECRET,
            sandbox=True
        )


# Create your views here.


# main page of our website
def main(request):
    return render_to_response('main.html')

# login page of our website
def login(request):
    return render_to_response('login.html')

# register new user page
def register(request):
    return render_to_response('register.html')

# called after register form is submitted
def registerHelper(request):
    #store new User model in db
    submitToAuth(reuqest)

# called after login and register
def submitToAuth(request):
    #call auth
    return render_to_response('')


# submission to evernote for authentication
def auth(request):
    client = get_evernote_client()
    callbackUrl = 'http://%s%s' % (
        request.get_host(), reverse('evernote_callback'))
    request_token = client.get_request_token(callbackUrl)

    # Save the request token information for later
    request.session['oauth_token'] = request_token['oauth_token']
    request.session['oauth_token_secret'] = request_token['oauth_token_secret']

    # Redirect the user to the Evernote authorization URL
    return redirect(client.get_authorize_url(request_token))


# what we receive after login successful
# dashboard page of our website
def dashboard(request):
    try:
        client = get_evernote_client()
        client.get_access_token(
            request.session['oauth_token'],
            request.session['oauth_token_secret'],
            request.GET.get('oauth_verifier', '')
        )
    except KeyError:
        return redirect('/')

    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()

    for notebook in notebooks:
        currGuid = notebook.guid
        notebook_filter = NoteStoreTypes.NoteFilter()
        notebook_filter.guid = currGuid
        result_spec = NotesMetadataResultSpec(includeTitle=True)
        noteList = note_store.findNotesMetadata(evernote_auth_token, notebook_filter,0 , 40000, result_spec)
        for note in noteList.notes:
            content = note.content  # "The XHTML block that makes up the note"
            # gets all contents from all notes
            print content
            return
            """ NLKT processing here!! """


    return render_to_response('dashboard.html', {'notebooks': notebooks})

