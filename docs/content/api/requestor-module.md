> Send get requests.

<a name="requestor.requestor"></a>
#### `requestor`

```python
def requestor(url: str, session: Session = None, proxies: Dict[str, str] = None, timeout: int = 5) -> Response
```

> Send get requests.
> 
> **Arguments**:
> 
> - `url` _str_ - The url to send a request to.
> - `session` _Session_ - A Session object to send a request with.
> - `proxies` _dict_ - Dictionary mapping protocol to the URL of the proxy.
> - `timeout` _int_ - How long to wait for the server to send data.

