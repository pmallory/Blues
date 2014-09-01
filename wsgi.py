import Blues.BluesSite

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return Blues.BluesSite.hello()

