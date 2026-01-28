# Turkish-agenda-API
A basic Python API that fetches the Turkish agenda from five different Turkish news websites. It can be integrated into applications or web pages.
This project uses FastAPI

API structure:
```json
{
  "success": true,
  "data": [
    {
      "source": "src1",
      "data": [
        {
          "id": "new1",
          "title": "title1",
          "summary": "summary1"
        }
      ]
    }
  ]
}
```

