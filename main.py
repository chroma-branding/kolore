# Import the Flask Framework
# ----------------------------------------------------------------
from flask import (Flask, render_template, request, redirect,
                   url_for, make_response)
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# Import dependencies
# ----------------------------------------------------------------
from flask.ext.babel import Babel

# Babel Config
# ----------------------------------------------------------------
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
LANGUAGES = {
    'en': 'English',
    'es': 'Espanol',
    'eu': 'Euskera'
}


# Import Blueprints
# ----------------------------------------------------------------
from app.admin.controllers import admin_app
from app.front.controllers import front_app

# Register Blueprints
# ----------------------------------------------------------------
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(front_app, url_prefix='')


# Language selector
# ----------------------------------------------------------------
@babel.localeselector
def get_locale():
    if not request.cookies.get('lang'):
        return 'en'
    else:
        return request.cookies.get('lang')


# Global routes
# ----------------------------------------------------------------
@app.route('/ADMIN')
def admin_redirect():
    return redirect(url_for('admin.home'))


@app.errorhandler(400)  # Bad Request
@app.errorhandler(401)  # Unauthorized
@app.errorhandler(403)  # Forbidden
@app.errorhandler(404)  # Not Found
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template('404.html')


@app.errorhandler(500)
def page_not_founds(e):
    """Return a custom 500 error."""
    return render_template('500.html')


@app.route('/sitemap.xml')
def sitemap():
    response = make_response(render_template(
        'sitemap.xml',
        host_url=request.host_url[:-1]
    ))
    response.headers['Content-Type'] = 'application/xml'
    return response
