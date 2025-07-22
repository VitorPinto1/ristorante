from config import *
import re

NAME_REGEX = re.compile(r"^[A-Za-zÀ-ÿñÑáéíóúÁÉÍÓÚüÜ]+(?: [A-Za-zÀ-ÿñÑáéíóúÁÉÍÓÚüÜ]+)?$")

def is_valid_name(name):
    return bool(NAME_REGEX.fullmatch(name)) and len(name) <= 50

def is_valid_comment(comment):
    return bool(re.fullmatch(r"[A-Za-zÀ-ÿñÑáéíóúÁÉÍÓÚüÜ0-9\s.,:;!?¡¿'\"()\-]{1,250}", comment))

reviews_bp = Blueprint('reviews', __name__, template_folder='templates')


@reviews_bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        comment = request.form.get('comment', '').strip()
        rating = int(request.form.get('rating', '0'))
        if not is_valid_name(name):
            flash("Please enter only your first and last name, without numbers or special characters.", "danger")
            return redirect(url_for('reviews.reviews'))

        if not is_valid_comment(comment):
            flash("Your review may only contain letters, numbers, spaces, and common punctuation (max 250 characters).", "danger")
            return redirect(url_for('reviews.reviews'))

        if 1 <= rating <= 5:
            mongo.db.reviews.insert_one({
                'name': name,
                'comment': comment,
                'rating': rating,
                'date': datetime.utcnow()
            })
            flash("Thank you for your review!", "success")
            return redirect(url_for('reviews.reviews'))
        else:
            flash("Please fill all fields and choose a rating between 1 and 5.", "danger")


    # Gestion des filtres
    min_rating = int(request.args.get('min_rating', '0'))
    reviews_query = {} if min_rating == 0 else {'rating': {'$gte': min_rating}}
    all_reviews = list(mongo.db.reviews.find(reviews_query).sort('date', -1))

    # Stats
    total = mongo.db.reviews.count_documents({})
    avg = round(sum(r['rating'] for r in all_reviews)/len(all_reviews),2) if all_reviews else 0
    stars_count = [
        mongo.db.reviews.count_documents({'rating': i}) for i in range(5,0,-1)
    ]
    if len(stars_count) != 5:
        stars_count = [0, 0, 0, 0, 0]

    return render_template(
        'reviews.html',
        reviews=all_reviews,
        avg=avg,
        total=total,
        stars_count=stars_count,
        min_rating=min_rating
    )