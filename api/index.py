"""
Vercel Serverless Function Entry Point
Exposes the Flask WSGI application callable for Vercel's Python runtime.
Includes WSGI path translation to handle Vercel rewrites and static assets seamlessly.
"""

import sys
import os
import urllib.parse

# Ensure the root project directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app

class VercelPathFix:
    """
    WSGI Middleware to fix Vercel rewrite paths.
    Resolves client requested routes from Vercel proxy headers and environment:
    1. HTTP_X_MATCHED_PATH (Vercel Edge matched route path, e.g. '/expenses')
    2. HTTP_X_FORWARDED_URL / HTTP_X_FORWARDED_URI / HTTP_X_ORIGINAL_URI / RAW_URI
    3. HTTP_X_NOW_ROUTE_MATCHES (Vercel regex capture matches)
    4. Explicit __vercel_route__ parameter in query string
    5. Native PATH_INFO
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        query_string = environ.get('QUERY_STRING', '')

        # 1. Preserve static files immediately - never rewrite static asset requests
        if path.startswith('/static/'):
            return self.wsgi_app(environ, start_response)

        resolved_path = None

        # 2. Check HTTP_X_MATCHED_PATH (Vercel's native matched route path)
        matched_path = (
            environ.get('HTTP_X_MATCHED_PATH') or 
            environ.get('HTTP_HTTP_X_MATCHED_PATH') or 
            environ.get('x-matched-path') or 
            environ.get('X-Matched-Path') or 
            environ.get('HTTP_X_VERCEL_MATCHED_PATH')
        )
        if matched_path:
            clean = matched_path.split('?')[0].strip()
            if clean.startswith('http://') or clean.startswith('https://'):
                clean = urllib.parse.urlparse(clean).path.strip()
            # Must not be the internal lambda entrypoint name
            if clean and clean not in ('/api/index.py', '/api/index', '/api', '/index.py') and not clean.startswith('/api/index'):
                resolved_path = clean if clean.startswith('/') else '/' + clean

        # 3. Check standard proxy URI / URL headers
        if not resolved_path:
            for header in (
                'HTTP_X_FORWARDED_URL', 'HTTP_HTTP_X_FORWARDED_URL',
                'HTTP_X_FORWARDED_URI', 'HTTP_HTTP_X_FORWARDED_URI',
                'HTTP_X_ORIGINAL_URI', 'HTTP_HTTP_X_ORIGINAL_URI',
                'HTTP_X_REWRITE_URL', 'RAW_URI', 'REQUEST_URI'
            ):
                raw_val = environ.get(header)
                if raw_val:
                    clean = raw_val.split('?')[0].strip()
                    if clean.startswith('http://') or clean.startswith('https://'):
                        clean = urllib.parse.urlparse(clean).path.strip()
                    if clean and clean not in ('/api/index.py', '/api/index', '/api', '/index.py') and not clean.startswith('/api/index'):
                        resolved_path = clean if clean.startswith('/') else '/' + clean
                        break

        # 4. Check HTTP_X_NOW_ROUTE_MATCHES (Vercel regex capture group, e.g. 1=expenses)
        if not resolved_path:
            route_matches = environ.get('HTTP_X_NOW_ROUTE_MATCHES') or environ.get('HTTP_HTTP_X_NOW_ROUTE_MATCHES')
            if route_matches:
                params = urllib.parse.parse_qs(route_matches)
                for key in ('1', '0', 'path', 'url'):
                    if key in params and params[key][0]:
                        val = urllib.parse.unquote(params[key][0]).strip()
                        if val and val not in ('api/index.py', 'api/index', 'api', 'index.py') and not val.startswith('api/index'):
                            resolved_path = val if val.startswith('/') else '/' + val
                            break

        # 5. Check __vercel_route__ query parameter if present
        if not resolved_path and '__vercel_route__=' in query_string:
            params = urllib.parse.parse_qs(query_string, keep_blank_values=True)
            if '__vercel_route__' in params:
                route_val = params.pop('__vercel_route__')[0].strip()
                if route_val and route_val not in ('/api/index.py', '/api/index', '/api', '/index.py') and not route_val.startswith('/api/index'):
                    resolved_path = route_val if route_val.startswith('/') else '/' + route_val
                # Clean up query string so Flask request.args stays clean
                environ['QUERY_STRING'] = urllib.parse.urlencode(params, doseq=True)

        # 6. Fallback to native PATH_INFO inspection
        if not resolved_path:
            if path.startswith('/api/index.py'):
                remainder = path[len('/api/index.py'):]
                resolved_path = remainder if (remainder and remainder != '/') else '/'
            elif path.startswith('/api/index'):
                remainder = path[len('/api/index'):]
                resolved_path = remainder if (remainder and remainder != '/') else '/'
            elif path.startswith('/api/'):
                remainder = path[len('/api'):]
                if remainder.startswith('/') and not remainder.startswith('/index'):
                    resolved_path = remainder
                else:
                    resolved_path = '/'
            elif path in ('/api', '/index.py', ''):
                resolved_path = '/'
            else:
                resolved_path = path

        # Set resolved PATH_INFO (guarantee valid root '/' if empty or internal file path)
        if not resolved_path or resolved_path in ('/api/index.py', '/api/index', '/api', '/index.py'):
            environ['PATH_INFO'] = '/'
        else:
            environ['PATH_INFO'] = resolved_path if resolved_path.startswith('/') else '/' + resolved_path

        return self.wsgi_app(environ, start_response)

# Vercel looks for the WSGI application callable named 'app'
app = VercelPathFix(flask_app)
