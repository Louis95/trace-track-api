"""Seed database"""
import csv

from modules.database.models import Article, ArticlesOnShipment, Carrier, Shipment
from modules.utilities.database import SessionLocal


def seed_database_with_data_from_csv():
    """Seed local database"""
    db_session = SessionLocal()

    with open("data.csv", "r") as data_file:  # noqa: W1514
        reader = csv.reader(data_file)
        next(reader)  # skip header row
        for row in reader:
            # create carrier object
            new_carrier = db_session.query(Carrier).filter_by(name=row[1]).first()
            if new_carrier is None:
                print(f"Add new carrier with name: {row[1]}")
                new_carrier = Carrier(name=row[1])
                db_session.add(new_carrier)
                db_session.flush()

            # create shipment object
            new_shipment = (
                db_session.query(Shipment).filter_by(tracking_number=row[0]).first()
            )
            if new_shipment is None:
                print(f"Add new Shipment with tracking_number: {row[0]}")

                new_shipment = Shipment(
                    tracking_number=row[0],
                    sender_street=row[2],
                    sender_zip=row[3],
                    sender_city=row[4],
                    sender_country=row[5],
                    receiver_street=row[6],
                    receiver_zip=row[7],
                    receiver_city=row[8],
                    receiver_country=row[9],
                    carrier=new_carrier,
                )
                db_session.add(new_shipment)
                db_session.flush()

            new_article = db_session.query(Article).filter_by(sku=row[13]).first()
            if new_article is None:
                print(f"Add new Article with name: {row[10]}")

                new_article = Article(sku=row[13], name=row[10], price=row[11])
                db_session.add(new_article)
                db_session.flush()

            articles_on_shipment = ArticlesOnShipment(
                shipment_id=new_shipment.id,
                article_id=new_article.id,
                quantity=row[12],
            )
            db_session.add(articles_on_shipment)

    # commit changes and close session
    db_session.commit()
    db_session.close()


seed_database_with_data_from_csv()
