from loc_authority_tools import db
from loc_authority_tools import tokenizer

BATCH_SIZE = 10000


def main():
    with db.conn() as conn:
        for i, (uuid, name) in enumerate(db.fetch_all_authorities(conn, batch_size=BATCH_SIZE)):
            if i % BATCH_SIZE == 0:
                print(f"Processing record {i}")
            tokens = tokenizer.tokenize_name(name)
            try:
                db.save_authority_tokens(conn, uuid, tokens)
            except Exception as e:
                print(f"Encountered exception {str(e)}")
                conn.rollback()
            else:
                conn.commit()


if __name__ == "__main__":
    main()
