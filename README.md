# OP RETURN REST API

A REST API to query the PostgreSQL database created by the [BitcoinRpcMiner](https://github.com/johannesmols/BitcoinRpcMiner)

## Endpoints

- [Frequency Analysis](#frequency-analysis)

### Frequency Analysis

**URL:** `/frequency-analysis`

**Method:** `GET`

**Authentication required:** No

**Parameters:**
* `min_date`: lower date boundary
    * Format: `YYYY-MM-DD`
    * Example: `2019-01-01`
* `max_date`: upper date boundary
    * Format: `YYYY-MM-DD`
    * Example: `20020-01-01` 
    
**Success Response:**

**Code:** `200 OK`

**Content example:**

```json
[
  {
    "dataday": "2020-01-01",
    "id": 4459,
    "nulldata": 66529,
    "p2ms": 9,
    "p2pk": 2245,
    "p2pkh": 223228,
    "p2sh": 221282,
    "unknowntype": 109618
  }
]
```