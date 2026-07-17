class AllowIframeEmbedMiddleware:
    """Allow this site to be embedded in an iframe from any origin.

    Django's XFrameOptionsMiddleware defaults to ``X-Frame-Options: DENY``,
    which blocks all framing. There is no "allow any" value for that header,
    so we strip it (in case anything else set it) and instead advertise a
    permissive Content-Security-Policy ``frame-ancestors`` directive, which
    is what modern browsers honor for framing control.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Remove the restrictive header if present.
        if response.has_header('X-Frame-Options'):
            del response['X-Frame-Options']
        # Explicitly permit framing from any origin.
        response['Content-Security-Policy'] = 'frame-ancestors *'
        return response
