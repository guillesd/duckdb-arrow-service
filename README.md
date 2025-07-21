## API service on top of DuckDB
This project simply aims at building a REST API on top duckDB to explore certain things about building services on top of OLAP systems. Some of the things being explored, for example:
- Performance of using Arrow IPC streams instead of JSON as a serializable/deserializable format for transfer over the network.
- DukcDBs native integration with Arrow
- How easy is to build a service like this in an inmature language like Julia vs a fully estrablished language with a much more robust ecosystem, like Python

And some other things I just wanted to check out of personal curiosity. Blogpost with some takeaways will come soon!