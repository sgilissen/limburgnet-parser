# limburgnet-parser
Simple Python parser for Limburg.net

Can be used as an import module for other projects. 

### Usage
```python
# Import the library
from limburgnet import limburgnet

# Create a new parser object
api = limburgnet.APIParser()

# Find a municipality NIS code. For example, Hasselt
api.search_municipality('Hasselt')
>>> [{'nisCode': '71022', 'naam': 'Hasselt'}]

# Find a the ID of a street. For example, the town hall of Hasselt is located at "Groenplein"
api.search_street('Groenplein', 71022)
>>> [{'nummer': '33742', 'naam': 'Groenplein'}]

# Partial search works as well
api.search_street('Thonis', 71022)
>>> [{'nummer': '34206', 'naam': 'Thonissenlaan'}]

# Let's verify if a specific house number exists in this street. If not, we get an empty array
api.search_housenumber(53, 34206)
>>> [{'huisNummer': '53', 'toevoeging': ''}]

# Let's fetch the next collections for this address. We should get a JSON result.
api.fetch_next_collection(71022, 34206, 53)
>>> {'datum': '2022-03-09T18:41:23+01:00', 'fracties': [{'name': 'Huisvuil', 'detailUrl': 'https://limburg.net/fractie/huisvuil'}, {'name': 'Papier & karton', 'detailUrl': 'https://limburg.net/fractie/papier-karton'}, {'name': 'Pmd', 'detailUrl': 'https://limburg.net/fractie/pmd'}, {'name': 'Textiel', 'detailUrl': 'https://limburg.net/fractie/textiel'}, {'name': 'Gft ', 'detailUrl': 'https://limburg.net/fractie/gft'}]}

# We can also do this for the current month
api.fetch_month_calendar(71022, 34206, 53)
>>> {"2022-03-02T18:42:23+01:00": {"category": "Textiel", "detail_url": "https://limburg.net/fractie/textiel"}, "2022-03-09T18:42:23+01:00": {"category": "Gft ", "detail_url": "https://limburg.net/fractie/gft"}, "2022-03-16T18:42:23+01:00": {"category": "Textiel", "detail_url": "https://limburg.net/fractie/textiel"}, "2022-03-23T18:42:23+01:00": {"category": "Gft ", "detail_url": "https://limburg.net/fractie/gft"}, "2022-03-30T18:42:23+02:00": {"category": "Textiel", "detail_url": "https://limburg.net/fractie/textiel"}}

```

