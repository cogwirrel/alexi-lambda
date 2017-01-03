
def build_speechlet_response(output, title="Alexi", reprompt_text=None, should_end_session=True):

    reprompt_text = reprompt_text or output

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(output, title="Alexi", reprompt_text=None, should_end_session=True, session_attributes=None):
    speechlet_response = build_speechlet_response(output, title, reprompt_text, should_end_session)
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes or {},
        'response': speechlet_response
    }
