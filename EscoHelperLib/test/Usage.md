# Usage of EscoTranslator.html

**Requirements to use the Web Tool**
* Serve the Javascript library and the ESCO tables in a HTTP Server.


The URL where ESCO Tables will be fetched is built from three parameters: filesLocation, filePrefix and language:

```
<filesLocation>/<filePrefix>_<language>.json
```

**Example:** 
```
filesLocation = 'https://example.com'
filePrefix = 'esco_labels_expanded'
language = 'en'

https://example.com/esco_labels_expanded_en.json
```

## Development Mode

1. Start the development server.

```
webpack-cli serve --mode=development --port <PORT>
```

2. Modify the first lines of the HTML file accordingly.

```
<script src="http://localhost:<PORT>/esco-helper.js"></script>

<script>
    const filesLocation = 'https://file_server_esco_tables/';
    const filePrefix = 'esco_labels_expanded';
</script>
```


## Test Mode


Instructions to use the Web Tool
1. Modify the first line of the file, replacing the generic url that points in localhost for the url where JS library is served.

```
<script src="http://localhost:8081/esco-helper.js"></script>
```

2. You can open the HTML file (EscoTranslator.html) directly into your browser, or serve it via HTTP Server.