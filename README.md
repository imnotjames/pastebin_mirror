# pastebin_mirror
Scrape and mirror [Pastebin.com](https://pastebin.com) to a local database.

## Getting Started

### Installing

Install with pip

```bash
pip install pastebin-mirror
```

### Running

After installing with pip, run the module, specifying the SQLite file to write to.

```bash
python -m pastebin_mirror ./pastebin.db
```

### Querying

While you can use `sqlite pastebin.db` to query the file, SQLite will often
emit the error message `Error: database is locked`.

To circumvent this we can enable a timeout and ensure that the database is
opened read only.  To do so, the following command may be used:

```bash
sqlite3 -cmd '.timeout 5000' 'file:pastebin.db?mode=ro'
```

You can at this point query for the values you'd like using SQL.

```SQL
SELECT * FROM paste WHERE paste_key='03bRivg4'
```

To get the content of a paste, you can use the following SQL.

```SQL
SELECT * FROM paste_content WHERE paste_key='03bRivg4'
```
