#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rawda@localhost/fyyur'
# TODO: connect to a local postgresql database
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(50))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)

    def __repr__(self):
        return self.name


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)

    def __repr__(self):
        return self.name


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Show {self.artist_id}{self.venue_id}>'


migrate = Migrate(app, db)
db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.all()
    # print(venues)
    data = []
    for venue in venues:
        dict_obj = {}
        dict_obj["city"] = venue.city
        dict_obj["state"] = venue.state
        dict_obj["venues"] = []
        venues_qry = Venue.query\
            .filter(Venue.city == venue.city)\
            .filter(Venue.state == venue.state).all()
        for v in venues_qry:
            num_upcoming_shows = len(Show.query.filter(Show.venue_id == v.id).filter(
                Show.start_time > datetime.now()).all())
            venue_dict = {"id": v.id, "name": v.name,
                          "num_upcoming_shows": num_upcoming_shows}
            dict_obj["venues"].append(venue_dict)
        data.append(dict_obj)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    search_term = request.form['search_term']
    all_data = Artist.query.filter(
        Artist.name.ilike(f"%{search_term}%")).all()
    data = []
    for artist in all_data:
        num_upcoming_shows = len(Show.query.filter(Show.artist_id == artist.id).filter(
            Show.start_time > datetime.now()).all())
        obj = {
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": num_upcoming_shows
            }
        data.append(obj)
    response = {"count": len(data), "data": data}
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if venue is None:
        abort(404)
    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    image_link = request.form['image_link']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    website = request.form['website_link']
    seeking_talent = True if 'seeking_talent' in request.form else False
    seeking_description = request.form['seeking_description']
    venue = Venue(name=name,
                  city=city,
                  state=state,
                  address=address,
                  phone=phone,
                  image_link=image_link,
                  genres=genres,
                  facebook_link=facebook_link,
                  website=website,
                  seeking_talent=seeking_talent,
                  seeking_description=seeking_description
                  )
    try:
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('Venue ' + request.form['name'] + ' couldn\'t be listed!')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
    except:
        abort(404)
    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = db.session.query().with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    search_term = request.form.get('search_term', '')
    response = {}
    artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
    response['count'] = len(artists)
    response['data'] = []
    for artist in artists:
        num_upcoming_shows = len(Show.query.filter(Show.artist_id == artist.id).filter(
            Show.start_time > datetime.now()).all())
        obj = {"id": artist.id, "name": artist.name,
               "num_upcoming_shows": num_upcoming_shows}
        response["data"].append(obj)
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    past_shows = Show.query.filter(Show.venue_id == artist_id).filter(
        Show.start_time < datetime.now()).all()
    upcoming_shows = Show.query.filter(Show.venue_id == artist_id).filter(
        Show.start_time > datetime.now()).all()
    artist_obj = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "phone": artist.phone,
        "seeking_venue": artist.seeking_venue,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    if artist is None:
        abort(404)

    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.website_link.data = artist.website
    form.facebook_link.data = artist.facebook_link
    form.seeking_description.data = artist.seeking_description
    form.image_link.data = artist.image_link
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.website = request.form['website_link']
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.seeking_venue = True if "seeking_venue" in request.form else False
    artist.seeking_description = request.form['seeking_description']
    db.session.commit()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    form.name.data = venue.name
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.website_link.data = venue.website
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website_link']
    venue.seeking_talent = True if 'seeking_talent' in request.form else False
    venue.seeking_description = request.form['seeking_description']
    try:
        db.session.commit()
    except:
        flash("Sorry there's an error.. try again :)")
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    seeking_venue = True if 'seeking_venue' in request.form else False
    seeking_description = request.form['seeking_description']
    artist = Artist(
        name=name,
        city=city,
        state=state,
        phone=phone,
        genres=genres,
        image_link=image_link,
        facebook_link=facebook_link,
        seeking_venue=seeking_venue,
        seeking_description=seeking_description
    )
    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('An error occurred. Artist ' + artist.name + ' could not be listed.')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = []
    all_shows = Show.query.all()
    for show in all_shows:
        venue = Venue.query.get(show.venue_id)
        artist = Artist.query.get(show.artist_id)

        show_obj = {
            "venue_id": show.venue_id,
            "venue_name": venue.name,
            "artist_id": show.artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        shows.append(show_obj)
    return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    show = Show(
        artist_id=artist_id,
        venue_id=venue_id,
        start_time=start_time
    )
    try:
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        flash('Sorry, there was an error. Try again :)')
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
