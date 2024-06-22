import psycopg


def main():
    print("Connecting to DB")
    with psycopg.connect("postgresql://postgres:postgres@localhost:5434/loc_authority_tools") as conn:
        print("Opening SQL file")
        with open("loc_authority_tools/database.sql", "r") as f:
            conn.execute(f.read())


if __name__ == "__main__":
    main()
