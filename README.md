# OP RETURN REST API

A REST API to query the PostgreSQL database created by the [BitcoinRpcMiner](https://github.com/johannesmols/BitcoinRpcMiner)

## Endpoints

- [Transaction Outputs](#transaction-outputs)
- [Transaction Outputs Search](#transaction-outputs-search)
- [Transaction Output by Hash](#transaction-output-by-hash)
- [Transaction Outputs by Block](#transaction-outputs-by-block)
- [Frequency Analysis](#frequency-analysis)
- [Size Analysis](#size-analysis)
- [Protocol Analysis](#protocol-analysis)

## Transaction Outputs

Retrieves the latest transaction outputs.

**URL:** `/tx-outputs`

**Method:** `GET`

**Authentication required:** No

**Optional Parameters:**
* `page`: page in search results. Default page size is 50.
    * Example: `1`

**Success Code:** `200 OK`

**Content example:**

```json
[
  {
    "blockhash": "0000000000000000000ba0fad6ab30a88b393cc265c49e077000c0cac24962ca",
    "blocktime": 1584834040,
    "fileheader": "",
    "id": 46928414,
    "outasm": "OP_RETURN 000f1f1000029782de2858f3937b64997510e50aef08555a0b74b4402102f4fbae3e4387bf8d199709918501ee50f16aa448b4945e76a5e00704dde1d3add631032bd571504526035ab1e48b5b5dd229",
    "outhex": "6a4c50000f1f1000029782de2858f3937b64997510e50aef08555a0b74b4402102f4fbae3e4387bf8d199709918501ee50f16aa448b4945e76a5e00704dde1d3add631032bd571504526035ab1e48b5b5dd229",
    "outtype": "nulldata",
    "outvalue": 0.0,
    "protocol": "veriblock",
    "txhash": "7269250bdca88935639b2d04e2948f17cce0a79ae8626eff0bc84859915eddd8"
  }
]
```

## Transaction Outputs Search

Retrieves transaction outputs based on search parameters.

**URL:** `/tx-outputs/search`

**Method:** `GET`

**Authentication required:** No

**Optional Parameters:**
* `search`: search term that can be found in the OP_RETURN data field
    * Format: at least 3 characters long
    * Example: `marry%20me`
* `format`: the search term can either be encoded (ASCII, UTF8) or in hex format
    * Format: `hex` or `encoded`
* `min_time`: lower time boundary
    * Format: Unix timestamp
    * Example: `1584890350`
* `max_time`: upper time boundary
    * Format: Unix timestamp
    * Example: `1584890350`
* `protocol`: protocol of the transaction output
    * Format: [identifier](https://github.com/johannesmols/BitcoinRpcMiner/blob/master/protocols.py) of protocol
    * Example: `veriblock`
* `fileheader`: file header contained in the data
    * Format: [identifier](https://github.com/johannesmols/BitcoinRpcMiner/blob/master/fileheaders.py) of file header
    * Example: `png`
* `sort`: sort the results by the primary key (ascending by default)
    * Format: `desc`
* `page`: page in search results. Default page size is 50.
    * Example: `1`

**Success Code:** `200 OK`

**Content example:**

```json
[
  {
    "blockhash": "0000000000000000000ba0fad6ab30a88b393cc265c49e077000c0cac24962ca",
    "blocktime": 1584834040,
    "fileheader": "",
    "id": 46928414,
    "outasm": "OP_RETURN 000f1f1000029782de2858f3937b64997510e50aef08555a0b74b4402102f4fbae3e4387bf8d199709918501ee50f16aa448b4945e76a5e00704dde1d3add631032bd571504526035ab1e48b5b5dd229",
    "outhex": "6a4c50000f1f1000029782de2858f3937b64997510e50aef08555a0b74b4402102f4fbae3e4387bf8d199709918501ee50f16aa448b4945e76a5e00704dde1d3add631032bd571504526035ab1e48b5b5dd229",
    "outtype": "nulldata",
    "outvalue": 0.0,
    "protocol": "veriblock",
    "txhash": "7269250bdca88935639b2d04e2948f17cce0a79ae8626eff0bc84859915eddd8"
  }
]
```

## Transaction Output by Hash

**URL:** `/tx-outputs/txhash`

**Method:** `GET`

**Authentication required:** No

**Required Parameters:**
* `hash`: transaction hash
    * Example: `7269250bdca88935639b2d04e2948f17cce0a79ae8626eff0bc84859915eddd8`

**Success Code:** `200 OK`

**Content example:**

```json
{
  "blockhash": "0000000000000000000ba0fad6ab30a88b393cc265c49e077000c0cac24962ca",
  "blocktime": 1584834040,
  "fileheader": "",
  "id": 46928414,
  "outasm": "OP_RETURN 000f1f1000029782de2858f3937b64997510e50aef08555a0b74b4402102f4fbae3e4387bf8d199709918501ee50f16aa448b4945e76a5e00704dde1d3add631032bd571504526035ab1e48b5b5dd229",
  "outhex": "6a4c50000f1f1000029782de2858f3937b64997510e50aef08555a0b74b4402102f4fbae3e4387bf8d199709918501ee50f16aa448b4945e76a5e00704dde1d3add631032bd571504526035ab1e48b5b5dd229",
  "outtype": "nulldata",
  "outvalue": 0.0,
  "protocol": "veriblock",
  "txhash": "7269250bdca88935639b2d04e2948f17cce0a79ae8626eff0bc84859915eddd8"
}
```

## Transaction Outputs by Block

**URL:** `/tx-outputs/blockhash`

**Method:** `GET`

**Authentication required:** No

**Required Parameters:**
* `hash`: block hash
    * Example: `0000000000000000000ba0fad6ab30a88b393cc265c49e077000c0cac24962ca`

**Success Code:** `200 OK`

**Content example:**

```json
[
  {
    "blockhash": "0000000000000000000ba0fad6ab30a88b393cc265c49e077000c0cac24962ca",
    "blocktime": 1584834040,
    "fileheader": "",
    "id": 46928407,
    "outasm": "OP_RETURN aa21a9ed4d3eca66aaff042540c34b448adc73474c06dd5e2cc8c93b9e47f86bb801d916",
    "outhex": "6a24aa21a9ed4d3eca66aaff042540c34b448adc73474c06dd5e2cc8c93b9e47f86bb801d916",
    "outtype": "nulldata",
    "outvalue": 0.0,
    "protocol": "unknownprotocol",
    "txhash": "a7dc1a5949d0bcbbf6a5a461dc970f1c3764ee083c0ed2fd592a6e981c6b2dad"
  }
]
```

## Frequency Analysis

**URL:** `/frequency-analysis`

**Method:** `GET`

**Authentication required:** No

**Optional Parameters:**
* `min_date`: lower date boundary
    * Format: `YYYY-MM-DD`
    * Example: `2019-01-01`
* `max_date`: upper date boundary
    * Format: `YYYY-MM-DD`
    * Example: `20020-01-01` 

**Success Code:** `200 OK`

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

## Size Analysis

**URL:** `/size-analysis`

**Method:** `GET`

**Authentication required:** No

**Optional Parameters:**
* `min_date`: lower date boundary
    * Format: `YYYY-MM-DD`
    * Example: `2019-01-01`
* `max_date`: upper date boundary
    * Format: `YYYY-MM-DD`
    * Example: `20020-01-01` 

**Success Code:** `200 OK`

**Content example:**

```json
[
  {
    "avgsize": 4847020,
    "dataday": "2020-01-01",
    "id": 4458,
    "outputs": 66529
  },
  {
    "avgsize": 3379207,
    "dataday": "2020-01-02",
    "id": 4459,
    "outputs": 64634
  }
]
```

## Protocol Analysis

**URL:** `/protocol-analysis`

**Method:** `GET`

**Authentication required:** No

**Optional Parameters:**
* `min_date`: lower date boundary
    * Format: `YYYY-MM-DD`
    * Example: `2019-01-01`
* `max_date`: upper date boundary
    * Format: `YYYY-MM-DD`
    * Example: `20020-01-01` 

**Success Code:** `200 OK`

**Content example:**

```json
[
  {
  "id": 4456,
    "dataday": "2020-01-01",
    "ascribe": 0,
    "...": "...",
    "veriblock": 55028
  }
]
```