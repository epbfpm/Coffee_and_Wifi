from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields import *
from wtforms.validators import *
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('URL', validators=[DataRequired(), URL()])
    open = TimeField('Open Time', validators=[DataRequired()])
    close = TimeField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕'])
    wifi_rating = SelectField('Wifi Rating', validators=[DataRequired()], choices=['💪', '💪💪', '💪💪💪', '💪💪💪💪'])
    power_rating = SelectField('Power Rating', validators=[DataRequired()], choices=['✘', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding="utf8") as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route('/cafes', methods=['GET', 'POST'])
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
