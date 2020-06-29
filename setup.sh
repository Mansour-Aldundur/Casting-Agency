export ENV='production'

export FLASK_APP='app'

export FLASK_DEBUG=True

export DATABASE_URL=''

export AUTH0_DOMAIN='auth-mansour.us.auth0.com'

export ALGORITHMS=['RS256']

export API_AUDIENCE='casting-agency'

flask db upgrade
