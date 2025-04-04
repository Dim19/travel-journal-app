from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from .models import Country, Entry
from . import db
import os
import csv
from datetime import datetime

travel_bp = Blueprint("travel", __name__, template_folder="../templates")

@travel_bp.route("/")
def index():
    # Query all countries for map display
    countries = Country.query.all()
    # Prepare data for JS: mapping country name to its ID and travel status
    country_data = {country.name: {"id": country.id, "travel_status": country.travel_status} for country in countries}
    return render_template("index.html", country_data=country_data)

@travel_bp.route("/country/<int:country_id>", methods=["GET", "POST"])
def country_detail(country_id):
    country = Country.query.get_or_404(country_id)
    if request.method == "POST":
        # Handle new travel entry submission
        city = request.form.get("city")
        notes = request.form.get("notes")
        rating = request.form.get("rating")
        travel_date_str = request.form.get("travel_date")
        travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d") if travel_date_str else None
        # Handle photo upload
        photo = request.files.get("photo")
        photo_filename = None
        if photo:
            upload_folder = os.path.join(current_app.root_path, "static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            photo_filename = os.path.join("uploads", photo.filename)
            photo.save(os.path.join(upload_folder, photo.filename))

        new_entry = Entry(
            country_id=country.id,
            city=city,
            notes=notes,
            rating=int(rating) if rating else None,
            travel_date=travel_date,
            photo_filename=photo_filename
        )
        db.session.add(new_entry)
        db.session.commit()
        flash("New travel entry added!", "success")
        return redirect(url_for("travel.country_detail", country_id=country.id))
    # Get all entries for the country
    entries = Entry.query.filter_by(country_id=country.id).all()
    return render_template("country.html", country=country, entries=entries)

@travel_bp.route("/dashboard")
def dashboard():
    # Compute travel statistics
    total_countries = Country.query.filter(Country.travel_status=="Visited").count()
    # Most visited continent: count visited countries by continent.
    visited_countries = Country.query.filter(Country.travel_status=="Visited").all()
    continent_count = {}
    for c in visited_countries:
        continent_count[c.continent] = continent_count.get(c.continent, 0) + 1
    most_visited_continent = max(continent_count, key=continent_count.get) if continent_count else None
    # Earliest travel date among entries
    earliest_entry = Entry.query.filter(Entry.travel_date != None).order_by(Entry.travel_date).first()
    return render_template("dashboard.html",
                           total_countries=total_countries,
                           most_visited_continent=most_visited_continent,
                           earliest_entry=earliest_entry)

@travel_bp.route("/export_csv")
def export_csv():
    # Export visited locations as CSV
    visited_entries = Entry.query.join(Country).filter(Country.travel_status=="Visited").all()
    # Create CSV file
    csv_file_path = os.path.join(current_app.root_path, "data", "visited_locations.csv")
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Country", "City", "Travel Date", "Rating", "Notes"])
        for entry in visited_entries:
            writer.writerow([
                entry.country.name,
                entry.city,
                entry.travel_date.strftime("%Y-%m-%d") if entry.travel_date else "",
                entry.rating,
                entry.notes
            ])
    return send_file(csv_file_path, as_attachment=True)

@travel_bp.route("/country/<int:country_id>/edit", methods=["GET", "POST"])
def edit_country(country_id):
    country = Country.query.get_or_404(country_id)
    if request.method == "POST":
        country.name = request.form.get("name")
        country.continent = request.form.get("continent")
        country.travel_status = request.form.get("travel_status")
        db.session.commit()
        flash("Country updated successfully!", "success")
        return redirect(url_for("travel.manage_countries"))
    return render_template("edit_country.html", country=country)

@travel_bp.route("/country/<int:country_id>/delete", methods=["POST"])
def delete_country(country_id):
    country = Country.query.get_or_404(country_id)
    db.session.delete(country)
    db.session.commit()
    flash("Country deleted.", "warning")
    return redirect(url_for("travel.manage_countries"))

# Optional route to add a new country (for admin or testing)
@travel_bp.route("/add_country", methods=["GET", "POST"])
def add_country():
    if request.method == "POST":
        name = request.form.get("name")
        continent = request.form.get("continent")
        travel_status = request.form.get("travel_status")
        # Check if country already exists
        existing = Country.query.filter_by(name=name).first()
        if existing:
            flash("Country already exists!", "danger")
            return redirect(url_for("travel.add_country"))
        new_country = Country(name=name, continent=continent, travel_status=travel_status)
        db.session.add(new_country)
        db.session.commit()
        flash("Country added successfully!", "success")
        return redirect(url_for("travel.index"))
    return render_template("add_country.html")

@travel_bp.route("/manage_countries")
def manage_countries():
    countries = Country.query.order_by(Country.name).all()
    return render_template("manage_countries.html", countries=countries)