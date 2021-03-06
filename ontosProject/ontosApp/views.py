from evernote.api.client import EvernoteClient

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.shortcuts import redirect

import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStoreTypes
import evernote.edam.notestore.NoteStore as NoteStore
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec

import nltk
import numpy

from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.probability import FreqDist

COUNTRIES = ['launiupoko','maui', 'cyprus', 'france', 'cabo', 'turkey', 'morocco', 'america']
SPORTS = ['football', 'baseball', 'soccer', 'tennis', 'rugby', 'basketball', 'cricket', 'swimming']

from textMining import *

#EN_CONSUMER_KEY = 'asingh12'
#EN_CONSUMER_SECRET = 'b2a9213e33d06b39'
developer_token = "S=s1:U=8f575:E=14fa60a5d52:C=1484e593048:P=1cd:A=en-devtoken:V=2:H=a265008d608004c2e80ad0670a88e067"


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
    submitToAuth(request)

# called after login and register
def submitToAuth(request):
    #call auth
    return render_to_response('')


# submission to evernote for authentication
def auth(request):
    client = get_evernote_client(token=developer_token)
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
        client = get_evernote_client(token=developer_token)
        """client.get_access_token(
            request.session['oauth_token'],
            request.session['oauth_token_secret'],
            request.GET.get('oauth_verifier', '')
        )"""
    except KeyError:
        return redirect('/')

    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()

    for notebook in notebooks:
        currGuid = notebook.guid
        notebook_filter = NoteStoreTypes.NoteFilter()
        notebook_filter.guid = currGuid
        result_spec = NotesMetadataResultSpec(includeTitle=True)
        noteList = note_store.findNotesMetadata(developer_token, notebook_filter,0 , 40000, result_spec)
        tokens = []
        print len(noteList.notes)
        i = 0
        for noteMetaData in noteList.notes:
            i+=1
            if i > 11:
                break
            print(noteMetaData.title)
            note = note_store.getNote(developer_token, noteMetaData.guid, True, True, True, True)
            currContent = note.content  # "The XHTML block that makes up the note"
            # gets all contents from all notes
            tokens = tokens + accumTokens(currContent)

        countryData = getCountryDist(tokens)
        cs = range(len(countryData))

    return render_to_response('dashboard.html', {'notebooks': notebooks, 'countryData':countryData, 'cs':cs})

