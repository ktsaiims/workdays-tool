## Docker commands

Run the app.

```bash
docker run -p 8501:8501 workdays-tool
```

Open in browser.

```
http://localhost:8501
```

### Custom ports (Optional)

- Change host port to 4000
- Change container port to 9000

```bash
docker run -e PORT=9000 -p 4000:9000 workdays-tool
```

Open in browser.

```
http://localhost:4000
```
