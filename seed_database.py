import csv

from modules.database.models import *
from modules.utilities.database import SessionLocal


def seed_database_with_data_from_csv():
    Session = SessionLocal
    session = Session()

    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            # create carrier object
            new_carrier = session.query(Carrier).filter_by(name=row[1]).first()
            if new_carrier is None:
                print(f"Add new carrier with name: {row[1]}")
                new_carrier = Carrier(name=row[1])
                session.add(new_carrier)
                session.flush()

            # create shipment object
            new_shipment = (
                session.query(Shipment).filter_by(tracking_number=row[0]).first()
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
                session.add(new_shipment)
                session.flush()

            new_article = session.query(Article).filter_by(sku=row[13]).first()
            if new_article is None:
                print(f"Add new Article with name: {row[10]}")

                new_article = Article(sku=row[13], name=row[10], price=row[11])
                session.add(new_article)
                session.flush()

            articles_on_shipment = ArticlesOnShipment(
                shipment_id=new_shipment.id,
                article_id=new_article.id,
                quantity=row[12],
            )
            session.add(articles_on_shipment)

    # commit changes and close session
    session.commit()
    session.close()


seed_database_with_data_from_csv()
