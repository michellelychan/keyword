
export PYTHONPATH=.
export FLASK_APP=web
apt-get update -qy
apt-get install -y python3-dev python3-pip
pip3 install Flask gunicorn pytest pytest-cov
pip3 install -r requirements

gunicorn --bind=0.0.0.0:9060 --daemon reload:app
gunicorn --bind 0.0.0.0:9061 --reload app:app --limit-request-field_size 0 --limit-request-line 0