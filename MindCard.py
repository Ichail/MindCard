from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

Base = declarative_base()


class MindCardTable(Base):
    __tablename__ = 'MindCards'
    id = Column(Integer, primary_key=True)
    eng = Column(String)
    rus = Column(String)


class DataBaseManager:
    def __init__(self, url: str) -> None:
        self.url = url
        self.engine = create_engine(self.url)
        self.Session = sessionmaker(bind=self.engine)

    def select(self, chunk: int = 10) -> None:
        session = self.Session()
        rows = session.query(MindCardTable).limit(chunk).all()
        for row in rows:
            print(row.eng, row.rus)
        session.close()
        return rows

    def select_like(self, like_term: str, chunk: int = 10) -> list:
        session = self.Session()
        result = session.query(MindCardTable).filter(MindCardTable.source.ilike(like_term)).limit(chunk).all()
        for row in result:
            print(row.eng, row.rus)
        session.close()
        return result

    def insert(self, eng: str, rus: str) -> None:
        session = self.Session()
        new_entry = MindCardTable(eng=eng, rus=rus)
        session.add(new_entry)
        session.commit()
        session.close()

    def bulk_insert(self, data: [(str, str)]) -> None:
        session = self.Session()
        entries = [MindCardTable(eng=eng, rus=rus) for eng, rus in data]
        session.bulk_save_objects(entries)
        session.commit()
        session.close()

    def export(self, filename: str):
        with open(filename, encoding='utf-8') as data:
            eng_map = data.readlines()
        for row in eng_map:
            row.encode('utf-8')
            eng_map = row.replace('\n', '').split(' - ')
            self.insert(eng_map[0], eng_map[1])

    def clear_table(self) -> None:
        session = self.Session()
        session.query(MindCardTable).delete()
        session.commit()
        session.close()



