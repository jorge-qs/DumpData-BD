import pandas as pd
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

# Function to generate usuarios
def gen_usuarios(n):
    usuarios = []
    for i in range(n):
        usuarios.append({
            'user_id': f'U{i:09}',
            'password': fake.password(length=16),
            'name': fake.name(),
            'phone_num': fake.phone_number(),
            'birth': fake.date_of_birth(minimum_age=18, maximum_age=90),
            'email': fake.email()
        })
    return usuarios

# Function to generate guests and hosts from usuarios
def gen_guests_hosts(usuarios, p_guest=0.5):
    guests = []
    hosts = []
    for user in usuarios:
        if random.random() < p_guest:
            guests.append({
                'user_id': user['user_id'],
            })
        else:
            hosts.append({
                'user_id': user['user_id'],
            })
    return guests, hosts

# Function to generate properties
def gen_properties(n, hosts):
    properties = []
    property_types = ['Entire place', 'Private room', 'Shared room']
    for i in range(n):
        properties.append({
            'property_id': f'P{i:09}',
            'n_bathrooms': fake.random_int(min=1, max=5),
            'title': fake.sentence(nb_words=6),
            'n_beds': fake.random_int(min=1, max=10),
            'property_type': random.choice(property_types),
            'n_guests': fake.random_int(min=1, max=20),
            'n_rooms': fake.random_int(min=1, max=10),
            'host_user_id': random.choice(hosts)['user_id'],
            'price': round(fake.random_number(digits=4, fix_len=True) / 100, 2)
        })
    return properties

# Function to generate bookings
def gen_bookings(n, guests, properties):
    bookings = []
    for i in range(n):
        check_in = fake.date_time_this_year()
        duration = timedelta(days=fake.random_int(min=1, max=30))
        check_out = check_in + duration
        bookings.append({
            'booking_id': f'B{i:09}',
            'timestamp': fake.date_time_this_year(),
            'check_in_date': check_in.date(),
            'check_out_date': check_out.date(),
            'guest_user_id': random.choice(guests)['user_id'],
            'property_id': random.choice(properties)['property_id']
        })
    return bookings

# Function to generate promotions
def gen_promotions(n, properties):
    promotions = []
    for i in range(n):
        start_date = fake.date_time_this_year()
        end_date = start_date + timedelta(days=fake.random_int(min=1, max=30))
        promotions.append({
            'promotion_id': f'PR{i:09}',
            'start_date': start_date.date(),
            'end_date': end_date.date(),
            'discount_rate': round(random.uniform(0, 100), 2),
            'prom_description': fake.text(max_nb_chars=200),
            'property_id': random.choice(properties)['property_id']
        })
    return promotions

# Function to generate amenities
def gen_amenities(n, properties):
    amenities = []
    condition_names = ['Available', 'Not Available']
    amenity_names = ['WiFi', 'Pool', 'Gym', 'Air Conditioning', 'Heating', 'Kitchen', 'Free Parking', 'Washer', 'Dryer', 'TV',
                     'Hot Tub', 'Fireplace', 'Breakfast Included', '24-Hour Check-in', 'Pet Friendly', 'Elevator', 'Balcony',
                     'BBQ Grill', 'Laptop-friendly Workspace', 'Smoke Detector', 'Parking', 'Breakfast', 'Laundry', 'Concierge',
                     'Mini Bar', 'Safe', 'Room Service', 'Hair Dryer', 'Coffee Maker', 'Shuttle Service', 'BBQ Area', 'Nearby Attractions',
                     'Nearby Dining', 'Beach', 'Mountain View', 'Forest View', 'Lake View', 'City View', 'Country View', 'River View',
                     'Sea View', 'Garden View', 'Pool View', 'Park View']
    for i in range(n):
        amenities.append({
            'amenity_id': f'A{i:09}',
            'condition': random.choice(condition_names),
            'amenity_name': random.choice(amenity_names),
            'property_id': random.choice(properties)['property_id']
        })
    return amenities

# Function to generate reviews
def gen_reviews(n, bookings):
    reviews = []
    for i in range(n):
        reviews.append({
            'review_id': f'R{i:09}',
            'booking_id': random.choice(bookings)['booking_id'],
            'comment': fake.sentence(nb_words=10),
            'rating': round(random.uniform(0, 5), 2)
        })
    return reviews

# Function to generate select favorites
def gen_select_favorites(guests, properties, density):
    select_favorites = []
    total_guests = len(guests)
    num_favorites = int(total_guests * density)
    generated_favorites = set()
    while len(generated_favorites) < num_favorites:
        guest = random.choice(guests)['user_id']
        property = random.choice(properties)['property_id']
        if (guest, property) not in generated_favorites:
            select_favorites.append({
                'property_id': property,
                'guest_user_id': guest
            })
            generated_favorites.add((guest, property))
    return select_favorites

# Function to generate messages
def gen_messages(n, guests, hosts):
    messages = []
    for i in range(n):
        guest = random.choice(guests)['user_id']
        host = random.choice(hosts)['user_id']
        messages.append({
            'message_id': f'M{i:09}',
            'guest_user_id': guest,
            'host_user_id': host,
            'message_content': fake.text(max_nb_chars=200),
            'time_message': fake.date_time_this_year()
        })
    return messages

if __name__ == "__main__":
    output_path = "/Users/User/BD"
    path = '1000000'
    # Parameters
    x=1000000
    num_usuarios = 10*x
    prob_guest = 0.6
    num_properties = 2*x
    num_bookings = 5*x
    num_promotions = x
    num_amenities = 5*x
    num_reviews = 2*x
    favorite_density = 1
    num_messages = 2*x

    # Generate data
    usuarios = gen_usuarios(num_usuarios)
    guests, hosts = gen_guests_hosts(usuarios, prob_guest)
    properties = gen_properties(num_properties, hosts)
    bookings = gen_bookings(num_bookings, guests, properties)
    promotions = gen_promotions(num_promotions, properties)
    amenities = gen_amenities(num_amenities, properties)
    reviews = gen_reviews(num_reviews, bookings)
    select_favorites = gen_select_favorites(guests, properties, favorite_density)
    messages = gen_messages(num_messages, guests, hosts)

    # Convert to DataFrames
    df_usuarios = pd.DataFrame(usuarios)
    df_guests = pd.DataFrame(guests)
    df_hosts = pd.DataFrame(hosts)
    df_properties = pd.DataFrame(properties)
    df_bookings = pd.DataFrame(bookings)
    df_promotions = pd.DataFrame(promotions)
    df_amenities = pd.DataFrame(amenities)
    df_reviews = pd.DataFrame(reviews)
    df_select_favorites = pd.DataFrame(select_favorites)
    df_messages = pd.DataFrame(messages)

    # Save to CSV
    df_usuarios.to_csv(f'{output_path}/data{path}/usuarios{path}.csv', index=False)
    df_guests.to_csv(f'{output_path}/data{path}/guests{path}.csv', index=False)
    df_hosts.to_csv(f'{output_path}/data{path}/hosts{path}.csv', index=False)
    df_properties.to_csv(f'{output_path}/data{path}/properties{path}.csv', index=False)
    df_bookings.to_csv(f'{output_path}/data{path}/bookings{path}.csv', index=False)
    df_promotions.to_csv(f'{output_path}/data{path}/promotions{path}.csv', index=False)
    df_amenities.to_csv(f'{output_path}/data{path}/amenities{path}.csv', index=False)
    df_reviews.to_csv(f'{output_path}/data{path}/reviews{path}.csv', index=False)
    df_select_favorites.to_csv(f'{output_path}/data{path}/select_favorites{path}.csv', index=False)
    df_messages.to_csv(f'{output_path}/data{path}/messages{path}.csv', index=False)

    print("Data generated and saved to CSV files successfully.")


