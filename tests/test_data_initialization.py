import pytest
import six
import datetime

from jsonmodels import models, fields, errors


def test_initialization():

    class Person(models.Base):

        name = fields.StringField()
        surname = fields.StringField()
        age = fields.IntField()
        cash = fields.FloatField()

    data = dict(
        name='Alan',
        surname='Wake',
        age=24,
        cash=2445.45,
        trash='123qwe',
    )

    alan1 = Person(**data)
    alan2 = Person()
    alan2.populate(**data)
    for alan in [alan1, alan2]:
        assert alan.name == 'Alan'
        assert alan.surname == 'Wake'
        assert alan.age == 24
        assert alan.cash == 2445.45

        assert not hasattr(alan, 'trash')


def test_deep_initialization():

    class Car(models.Base):

        brand = fields.StringField()

    class ParkingPlace(models.Base):

        location = fields.StringField()
        car = fields.EmbeddedField(Car)

    data = {
        'location': 'somewhere',
        'car': {
            'brand': 'awesome brand'
        }
    }

    parking1 = ParkingPlace(**data)
    parking2 = ParkingPlace()
    parking2.populate(**data)
    for parking in [parking1, parking2]:
        assert parking.location == 'somewhere'
        car = parking.car
        assert isinstance(car, Car)
        assert car.brand == 'awesome brand'

        assert parking.location == 'somewhere'
        car = parking.car
        assert isinstance(car, Car)
        assert car.brand == 'awesome brand'


def test_deep_initialization_multiple_1():

    class Car(models.Base):

        brand = fields.StringField()

    class Bus(models.Base):

        brand = fields.StringField()
        seats = fields.IntField()

    class Train(models.Base):

        line = fields.StringField()
        seats = fields.IntField()

    class ParkingPlace(models.Base):

        location = fields.StringField()
        vehicle = fields.EmbeddedField([Car, Bus, Train])

    data1 = {
        'location': 'somewhere',
        'vehicle': {
            'brand': 'awesome brand',
            'seats': 100
        }
    }

    parking1 = ParkingPlace(**data1)
    parking2 = ParkingPlace()
    parking2.populate(**data1)
    for parking in [parking1, parking2]:
        assert parking.location == 'somewhere'
        vehicle = parking.vehicle
        assert isinstance(vehicle, Bus)
        assert vehicle.brand == 'awesome brand'
        assert vehicle.seats == 100

    data2 = {
        'location': 'somewhere',
        'vehicle': {
            'line': 'Uptown',
            'seats': 400
        }
    }

    parking1 = ParkingPlace(**data2)
    parking2 = ParkingPlace()
    parking2.populate(**data2)
    for parking in [parking1, parking2]:
        assert parking.location == 'somewhere'
        vehicle = parking.vehicle
        assert isinstance(vehicle, Train)
        assert vehicle.line == 'Uptown'
        assert vehicle.seats == 400

    data3 = {
        'location': 'somewhere',
        'vehicle': {
        }
    }

    with pytest.raises(errors.ValidationError):
        ParkingPlace(**data3)

    with pytest.raises(errors.ValidationError):
        parking = ParkingPlace()
        parking.populate(**data3)

def test_deep_initialization_multiple_2():

    class Viper(models.Base):

        brand = fields.StringField()

    class Lamborghini(models.Base):

        brand = fields.StringField()

    class ParkingPlace(models.Base):

        location = fields.StringField()
        car = fields.EmbeddedField([Viper, Lamborghini])

    data = {
        'location': 'somewhere',
        'car': {
            'brand': 'awesome brand'
        }
    }

    parking1 = ParkingPlace(**data)
    parking2 = ParkingPlace()
    parking2.populate(**data)
    for parking in [parking1, parking2]:
        assert parking.location == 'somewhere'
        car = parking.car
        assert isinstance(car, Viper)
        assert car.brand == 'awesome brand'


def test_deep_initialization_with_list():

    class Car(models.Base):

        brand = fields.StringField()

    class Parking(models.Base):

        location = fields.StringField()
        cars = fields.ListField(items_types=Car)

    data = {
        'location': 'somewhere',
        'cars': [
            {
                'brand': 'one',
            },
            {
                'brand': 'two',
            },
            {
                'brand': 'three',
            },
        ],
    }

    parking1 = Parking(**data)
    parking2 = Parking()
    parking2.populate(**data)
    for parking in [parking1, parking2]:
        assert parking.location == 'somewhere'
        cars = parking.cars
        assert isinstance(cars, list)
        assert len(cars) == 3

        values = []
        for car in cars:
            assert isinstance(car, Car)
            values.append(car.brand)
        assert 'one' in values
        assert 'two' in values
        assert 'three' in values


def test_deep_initialization_with_list_and_multitypes():

    class Car(models.Base):

        brand = fields.StringField()
        horsepower = fields.IntField()
        owner = fields.StringField()

    class Scooter(models.Base):

        brand = fields.StringField()
        horsepower = fields.IntField()
        speed = fields.IntField()

    class Parking(models.Base):

        location = fields.StringField()
        vehicle = fields.ListField([Car, Scooter])

    data = {
        'location': 'somewhere',
        'vehicle': [
            {
                'brand': 'viper',
                'horsepower': 987,
                'owner': 'Jeff'
            },
            {
                'brand': 'lamborgini',
                'horsepower': 877,
            },
            {
                'brand': 'piaggio',
                'horsepower': 25,
                'speed': 120
            },
        ],
    }

    parking1 = Parking(**data)
    parking2 = Parking()
    parking2.populate(**data)
    for parking in [parking1, parking2]:
        assert parking.location == 'somewhere'
        vehicles = parking.vehicle
        assert isinstance(vehicles, list)
        assert len(vehicles) == 3

        assert isinstance(vehicles[0], Car)
        assert vehicles[0].brand == 'viper'
        assert vehicles[0].horsepower == 987
        assert vehicles[0].owner == 'Jeff'

        assert isinstance(vehicles[1], Car)
        assert vehicles[1].brand == 'lamborgini'
        assert vehicles[1].horsepower == 877
        assert vehicles[1].owner == None

        assert isinstance(vehicles[2], Scooter)
        assert vehicles[2].brand == 'piaggio'
        assert vehicles[2].horsepower == 25


def test_deep_initialization_with_empty_list_and_multitypes():

    class Car(models.Base):

        brand = fields.StringField()
        horsepower = fields.IntField()
        owner = fields.StringField()

    class Scooter(models.Base):

        brand = fields.StringField()
        horsepower = fields.IntField()
        speed = fields.IntField()

    class Parking(models.Base):

        location = fields.StringField()
        vehicle = fields.ListField([Car, Scooter])

    data = {
        'location': 'somewhere',
        'vehicle': []
    }

    parking1 = Parking(**data)
    parking2 = Parking()
    parking2.populate(**data)
    for parking in [parking1, parking2]:
        assert parking.location == 'somewhere'
        vehicles = parking.vehicle
        assert isinstance(vehicles, list)
        assert len(vehicles) == 0


def test_deep_initialization_error_when_result_non_iterable():

    class Viper(models.Base):

        brand = fields.StringField()

    class Lamborghini(models.Base):

        brand = fields.StringField()

    class Parking(models.Base):

        location = fields.StringField()
        cars = fields.ListField([Viper, Lamborghini])

    data = {
        'location': 'somewhere',
        'cars': object(),
    }

    with pytest.raises(errors.ValidationError):
        Parking(**data)

    parking = Parking()
    with pytest.raises(errors.ValidationError):
        parking.populate(**data)


def test_initialization_with_non_models_types():

    class Person(models.Base):

        names = fields.ListField(str)
        surname = fields.StringField()

    data = {
        'names': ['Chuck', 'Testa'],
        'surname': 'Norris'
    }

    person1 = Person(**data)
    person2 = Person()
    person2.populate(**data)

    for person in [person1, person2]:
        assert person.surname == 'Norris'
        assert len(person.names) == 2
        assert 'Chuck' in person.names
        assert 'Testa' in person.names


def test_initialization_with_multi_non_models_types():

    class Person(models.Base):

        name = fields.StringField()
        mix = fields.ListField((str, float))

    data = {
        'name': 'Chuck',
        'mix': ['something', 42.0, 'weird']
    }

    person1 = Person(**data)
    person2 = Person()
    person2.populate(**data)

    for person in [person1, person2]:
        assert person.name == 'Chuck'
        assert len(person.mix) == 3
        assert 'something' in person.mix
        assert 42.0 in person.mix
        assert 'weird' in person.mix


def test_initialization_with_wrong_types():

    class Person(models.Base):

        name = fields.StringField()
        mix = fields.ListField((str, float))

    data = {
        'name': 'Chuck',
        'mix': ['something', 42.0, 'weird']
    }

    Person(**data)


def test_deep_initialization_for_embed_field():

    class Car(models.Base):

        brand = fields.StringField()

    class ParkingPlace(models.Base):

        location = fields.StringField()
        car = fields.EmbeddedField(Car)

    data = {
        'location': 'somewhere',
        'car': Car(brand='awesome brand'),
    }

    parking1 = ParkingPlace(**data)
    parking2 = ParkingPlace()
    parking2.populate(**data)
    for parking in [parking1, parking2]:
        assert parking.location == 'somewhere'
        car = parking.car
        assert isinstance(car, Car)
        assert car.brand == 'awesome brand'

        assert parking.location == 'somewhere'
        car = parking.car
        assert isinstance(car, Car)
        assert car.brand == 'awesome brand'


def test_int_field_parsing():

    class Counter(models.Base):
        value = fields.IntField()

    counter0 = Counter(value=None)
    assert counter0.value is None
    counter1 = Counter(value=1)
    assert isinstance(counter1.value, int)
    assert counter1.value == 1
    counter2 = Counter(value='2')
    assert isinstance(counter2.value, int)
    assert counter2.value == 2
    if not six.PY3:
        counter3 = Counter(value=long(3))  # noqa
        assert isinstance(counter3.value, int)
        assert counter3.value == 3


def test_default_value():

    class Job(models.Base):
        title = fields.StringField()
        company = fields.StringField()

    default_job = Job(tile="Unemployed", company="N/A")
    default_age = 18
    default_name = "John Doe"
    default_height = 1.70
    default_hobbies = ["eating", "reading"]
    default_last_ate = datetime.time()
    default_birthday = datetime.date.today()
    default_time_of_death = datetime.datetime.now()

    class Person(models.Base):
        name = fields.StringField(default=default_name)
        age = fields.IntField(default=default_age)
        height = fields.FloatField(default=default_height)
        job = fields.EmbeddedField(Job, default=default_job)
        hobbies = fields.ListField(items_types=str, default=default_hobbies)
        last_ate = fields.TimeField(default=default_last_ate)
        birthday = fields.DateField(default=default_birthday)
        time_of_death = fields.DateTimeField(default=default_time_of_death)

    p = Person()
    assert p.name == default_name
    assert p.age == default_age
    assert p.height == default_height
    assert p.hobbies == default_hobbies
    assert p.job == default_job
    assert p.last_ate == default_last_ate
    assert p.birthday == default_birthday
    assert p.time_of_death == default_time_of_death
