from sqlalchemy import create_engine, delete, and_
from sqlalchemy.orm import sessionmaker
from .models import CryptCurencys, TrackCurency


class Database:
    def __init__(self, db='sqlite_python.db'):
        self._db = db
        self.engine = create_engine(f'sqlite:///{db}')
        # Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close(self):
        if self.session:
            self.session.commit()
            self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def session(func):
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                self.session.commit()
                return result
            except:
                self.session.rollback()
                raise
            finally:
                self.session.close()
        return wrapper

    @session
    def add_currency(self, currency_name, currency_price):
        existing_currency = self.session.query(
            CryptCurencys).filter_by(name=currency_name).first()

        if existing_currency:
            existing_currency.price = currency_price
        else:
            new_currency = CryptCurencys(name=currency_name,
                                         price=currency_price)
            self.session.add(new_currency)

    @session
    def get_currency(self):
        query = self.session.query(CryptCurencys).limit(5)
        results = query.all()
        currency_data = {}
        for result in results:
            currency_data[result.id] = result.name
        return currency_data

    @session
    def get_track_currency(self, id_tg, name):
        existing_data = self.session.query(
            TrackCurency).filter(TrackCurency.id_user == id_tg,
                                 TrackCurency.name_crypt == name).first()

        if existing_data:
            return [existing_data.name_crypt,
                    existing_data.max_curency,
                    existing_data.min_curency]
        else:
            return False

    @session
    def add_track_currency(self, id_tg, name, min_c, max_c):
        new_data = TrackCurency(id_user=id_tg, name_crypt=name,
                                max_curency=min_c, min_curency=max_c,
                                status=True)
        self.session.add(new_data)

    @session
    def del_track_currency(self, id_tg, name):
        delete_statement = delete(
            TrackCurency).where(and_(TrackCurency.id_user == id_tg,
                                     TrackCurency.name_crypt == name))
        self.session.execute(delete_statement)

    @session
    def track_currency(self):
        tracked_currencies = self.session.query(
            TrackCurency).filter(TrackCurency.status == True).all()
        text = {}

        for tracked_currency in tracked_currencies:
            crypt_currency = self.session.query(
                CryptCurencys).filter(
                    CryptCurencys.name == tracked_currency.name_crypt).first()

            if crypt_currency.price > tracked_currency.max_curency or crypt_currency.price < tracked_currency.min_curency:
                text[tracked_currency.id_user] = f'{tracked_currency.name_crypt}'
        return text
